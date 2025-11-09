"""
Tests for FAQ Generator module.

This module contains unit tests for the FAQGenerator class,
including API integration, response parsing, and validation.
"""

import pytest
import json
from unittest.mock import Mock, patch
from src.faq_generator import FAQGenerator, FAQ


class TestFAQGenerator:
    """Test cases for FAQGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.api_key = "test-api-key"
        self.generator = FAQGenerator(api_key=self.api_key)
        self.sample_business_info = "We are a local dental practice specializing in cosmetic dentistry and orthodontics."
    
    def test_initialization(self):
        """Test FAQGenerator initialization."""
        generator = FAQGenerator(api_key="test-key")
        assert generator.client is not None
        assert generator.model == "gpt-4o"
        assert "friendly" in generator.prompts
        assert "formal" in generator.prompts
        assert "expert" in generator.prompts
    
    def test_initialization_with_custom_model(self):
        """Test FAQGenerator initialization with custom model."""
        generator = FAQGenerator(api_key="test-key", model="gpt-3.5-turbo")
        assert generator.model == "gpt-3.5-turbo"
    
    @patch('src.faq_generator.OpenAI')
    def test_openai_client_initialization(self, mock_openai):
        """Test OpenAI client initialization."""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        generator = FAQGenerator(api_key="test-key")
        mock_openai.assert_called_once_with(api_key="test-key")
        assert generator.client == mock_client
    
    def test_load_prompts(self):
        """Test prompt loading."""
        prompts = self.generator._load_prompts()
        
        assert isinstance(prompts, dict)
        assert "friendly" in prompts
        assert "formal" in prompts
        assert "expert" in prompts
        
        # Check prompt structure
        for tone, prompt in prompts.items():
            assert "{business_info}" in prompt
            assert "{num_faqs}" in prompt
            assert "JSON" in prompt
    
    @patch('src.faq_generator.OpenAI')
    def test_generate_faqs_success(self, mock_openai):
        """Test successful FAQ generation."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps([
            {
                "question": "What services do you offer?",
                "answer": "We provide comprehensive dental care including cosmetic dentistry and orthodontics.",
                "category": "Services"
            },
            {
                "question": "How do I schedule an appointment?",
                "answer": "You can schedule an appointment by calling our office or using our online booking system.",
                "category": "Appointments"
            }
        ])
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        generator = FAQGenerator(api_key="test-key")
        faqs = generator.generate_faqs(
            business_info=self.sample_business_info,
            tone="friendly",
            num_faqs=2
        )
        
        assert len(faqs) == 2
        assert faqs[0]["question"] == "What services do you offer?"
        assert faqs[0]["answer"] == "We provide comprehensive dental care including cosmetic dentistry and orthodontics."
        assert faqs[0]["category"] == "Services"
        assert "keywords" in faqs[0]
    
    def test_generate_faqs_invalid_inputs(self):
        """Test FAQ generation with invalid inputs."""
        # Empty business info
        with pytest.raises(ValueError, match="Business information cannot be empty"):
            self.generator.generate_faqs(business_info="", tone="friendly")
        
        # Invalid tone
        with pytest.raises(ValueError, match="Invalid tone"):
            self.generator.generate_faqs(business_info=self.sample_business_info, tone="invalid")
        
        # Invalid number of FAQs
        with pytest.raises(ValueError, match="Number of FAQs must be between 3 and 5"):
            self.generator.generate_faqs(business_info=self.sample_business_info, tone="friendly", num_faqs=2)
        
        with pytest.raises(ValueError, match="Number of FAQs must be between 3 and 5"):
            self.generator.generate_faqs(business_info=self.sample_business_info, tone="friendly", num_faqs=6)
    
    def test_parse_response_valid_json(self):
        """Test parsing valid JSON response."""
        response = json.dumps([
            {
                "question": "What services do you offer?",
                "answer": "We provide comprehensive dental care.",
                "category": "Services"
            }
        ])
        
        faqs = self.generator._parse_response(response)
        
        assert len(faqs) == 1
        assert faqs[0]["question"] == "What services do you offer?"
        assert faqs[0]["answer"] == "We provide comprehensive dental care."
        assert faqs[0]["category"] == "Services"
    
    def test_parse_response_invalid_json(self):
        """Test parsing invalid JSON response."""
        response = "This is not valid JSON"
        
        with pytest.raises(ValueError, match="Failed to parse FAQ response as JSON"):
            self.generator._parse_response(response)
    
    def test_parse_response_missing_fields(self):
        """Test parsing response with missing required fields."""
        response = json.dumps([
            {
                "question": "What services do you offer?"
                # Missing answer field
            }
        ])
        
        with pytest.raises(ValueError, match="FAQ 0 missing required field: answer"):
            self.generator._parse_response(response)
    
    def test_extract_keywords(self):
        """Test keyword extraction."""
        question = "What services do you offer for dental care?"
        answer = "We provide comprehensive dental services including cleanings, fillings, and cosmetic procedures."
        
        keywords = self.generator._extract_keywords(question, answer)
        
        assert isinstance(keywords, list)
        assert len(keywords) <= 5
        assert "services" in keywords
        assert "dental" in keywords
    
    def test_validate_faqs_valid(self):
        """Test validation of valid FAQs."""
        faqs = [
            {
                "question": "What services do you offer?",
                "answer": "We provide comprehensive dental care including cleanings, fillings, and cosmetic procedures.",
                "category": "Services"
            },
            {
                "question": "How do I schedule an appointment?",
                "answer": "You can schedule an appointment by calling our office or using our online booking system.",
                "category": "Appointments"
            },
            {
                "question": "What are your office hours?",
                "answer": "Our office is open Monday through Friday from 8 AM to 5 PM.",
                "category": "Hours"
            }
        ]
        
        results = self.generator.validate_faqs(faqs)
        
        assert results["valid"] is True
        assert len(results["issues"]) == 0
        assert "avg_answer_length" in results["metrics"]
    
    def test_validate_faqs_invalid(self):
        """Test validation of invalid FAQs."""
        # Too few FAQs
        faqs = [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"}
        ]
        
        results = self.generator.validate_faqs(faqs)
        assert results["valid"] is False
        assert "Too few FAQs generated" in results["issues"]
        
        # Duplicate questions
        faqs = [
            {"question": "Same question", "answer": "A1"},
            {"question": "Same question", "answer": "A2"},
            {"question": "Different question", "answer": "A3"}
        ]
        
        results = self.generator.validate_faqs(faqs)
        assert results["valid"] is False
        assert "Duplicate questions found" in results["issues"]
        
        # Missing required fields
        faqs = [
            {"question": "Q1", "answer": ""},  # Empty answer
            {"question": "", "answer": "A2"},  # Empty question
            {"question": "Q3", "answer": "A3"}
        ]
        
        results = self.generator.validate_faqs(faqs)
        assert results["valid"] is False
        assert len(results["issues"]) > 0


class TestFAQ:
    """Test cases for FAQ dataclass."""
    
    def test_faq_creation(self):
        """Test FAQ dataclass creation."""
        faq = FAQ(
            question="What services do you offer?",
            answer="We provide comprehensive dental care.",
            category="Services",
            keywords=["dental", "services"]
        )
        
        assert faq.question == "What services do you offer?"
        assert faq.answer == "We provide comprehensive dental care."
        assert faq.category == "Services"
        assert faq.keywords == ["dental", "services"]
    
    def test_faq_optional_fields(self):
        """Test FAQ with optional fields."""
        faq = FAQ(
            question="What services do you offer?",
            answer="We provide comprehensive dental care."
        )
        
        assert faq.question == "What services do you offer?"
        assert faq.answer == "We provide comprehensive dental care."
        assert faq.category is None
        assert faq.keywords is None









