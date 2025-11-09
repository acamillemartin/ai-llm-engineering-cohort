"""
Tests for Schema Generator module.

This module contains unit tests for the SchemaGenerator class,
including schema generation, validation, and formatting.
"""

import pytest
import json
from datetime import datetime
from src.schema_generator import SchemaGenerator


class TestSchemaGenerator:
    """Test cases for SchemaGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = SchemaGenerator()
        self.sample_faqs = [
            {
                "question": "What services do you offer?",
                "answer": "We provide comprehensive dental care including cleanings, fillings, and cosmetic procedures.",
                "category": "Services",
                "keywords": ["dental", "services", "care"]
            },
            {
                "question": "How do I schedule an appointment?",
                "answer": "You can schedule an appointment by calling our office or using our online booking system.",
                "category": "Appointments",
                "keywords": ["appointment", "schedule", "booking"]
            },
            {
                "question": "What are your office hours?",
                "answer": "Our office is open Monday through Friday from 8 AM to 5 PM.",
                "category": "Hours",
                "keywords": ["hours", "office", "schedule"]
            }
        ]
    
    def test_initialization(self):
        """Test SchemaGenerator initialization."""
        generator = SchemaGenerator()
        assert generator.schema_template is not None
        assert generator.schema_template["@context"] == "https://schema.org"
        assert generator.schema_template["@type"] == "FAQPage"
        assert generator.schema_template["mainEntity"] == []
    
    def test_generate_schema_basic(self):
        """Test basic schema generation."""
        schema = self.generator.generate_schema(self.sample_faqs)
        
        # Check required fields
        assert "@context" in schema
        assert "@type" in schema
        assert "mainEntity" in schema
        
        # Check values
        assert schema["@context"] == "https://schema.org"
        assert schema["@type"] == "FAQPage"
        assert isinstance(schema["mainEntity"], list)
        assert len(schema["mainEntity"]) == 3
        
        # Check timestamp
        assert "dateCreated" in schema
        assert isinstance(schema["dateCreated"], str)
    
    def test_generate_schema_with_metadata(self):
        """Test schema generation with additional metadata."""
        metadata = {
            "title": "Dental Practice FAQs",
            "description": "Frequently asked questions about our dental services",
            "url": "https://example.com/faqs",
            "author": "Dr. Smith"
        }
        
        schema = self.generator.generate_schema(self.sample_faqs, **metadata)
        
        assert schema["name"] == "Dental Practice FAQs"
        assert schema["description"] == "Frequently asked questions about our dental services"
        assert schema["url"] == "https://example.com/faqs"
        assert "author" in schema
        assert schema["author"]["@type"] == "Person"
        assert schema["author"]["name"] == "Dr. Smith"
    
    def test_generate_schema_empty_faqs(self):
        """Test schema generation with empty FAQ list."""
        with pytest.raises(ValueError, match="No FAQs provided for schema generation"):
            self.generator.generate_schema([])
    
    def test_create_question_entity(self):
        """Test creation of individual question entities."""
        faq = self.sample_faqs[0]
        entity = self.generator._create_question_entity(faq)
        
        # Check required fields
        assert entity["@type"] == "Question"
        assert entity["name"] == faq["question"]
        assert "acceptedAnswer" in entity
        
        # Check answer structure
        answer = entity["acceptedAnswer"]
        assert answer["@type"] == "Answer"
        assert answer["text"] == faq["answer"]
        
        # Check optional fields
        assert "about" in entity
        assert entity["about"]["@type"] == "Thing"
        assert entity["about"]["name"] == faq["category"]
        
        assert "keywords" in entity
        assert entity["keywords"] == ", ".join(faq["keywords"])
    
    def test_create_question_entity_minimal(self):
        """Test creation of question entity with minimal data."""
        faq = {
            "question": "What services do you offer?",
            "answer": "We provide comprehensive dental care."
        }
        
        entity = self.generator._create_question_entity(faq)
        
        assert entity["@type"] == "Question"
        assert entity["name"] == faq["question"]
        assert entity["acceptedAnswer"]["text"] == faq["answer"]
        assert "about" not in entity
        assert "keywords" not in entity
    
    def test_validate_schema_valid(self):
        """Test validation of valid schema."""
        schema = self.generator.generate_schema(self.sample_faqs)
        results = self.generator.validate_schema(schema)
        
        assert results["valid"] is True
        assert len(results["issues"]) == 0
        assert len(results["warnings"]) == 0
    
    def test_validate_schema_invalid(self):
        """Test validation of invalid schema."""
        # Missing required fields
        invalid_schema = {
            "@type": "FAQPage"
            # Missing @context and mainEntity
        }
        
        results = self.generator.validate_schema(invalid_schema)
        
        assert results["valid"] is False
        assert "Missing required field: @context" in results["issues"]
        assert "Missing required field: mainEntity" in results["issues"]
        
        # Invalid @type
        invalid_schema = {
            "@context": "https://schema.org",
            "@type": "Article",  # Should be FAQPage
            "mainEntity": []
        }
        
        results = self.generator.validate_schema(invalid_schema)
        assert results["valid"] is False
        assert "@type must be 'FAQPage'" in results["issues"]
        
        # Invalid mainEntity
        invalid_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": "not a list"
        }
        
        results = self.generator.validate_schema(invalid_schema)
        assert results["valid"] is False
        assert "mainEntity must be a list" in results["issues"]
    
    def test_validate_schema_question_entities(self):
        """Test validation of question entities."""
        schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "What services do you offer?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "We provide comprehensive dental care."
                    }
                },
                {
                    "@type": "Question",
                    # Missing name field
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "We provide comprehensive dental care."
                    }
                }
            ]
        }
        
        results = self.generator.validate_schema(schema)
        
        assert results["valid"] is False
        assert "Question 1: Missing required field 'name'" in results["issues"]
    
    def test_format_schema(self):
        """Test schema formatting."""
        schema = self.generator.generate_schema(self.sample_faqs)
        formatted = self.generator.format_schema(schema)
        
        assert isinstance(formatted, str)
        
        # Should be valid JSON
        parsed = json.loads(formatted)
        assert parsed["@type"] == "FAQPage"
        assert len(parsed["mainEntity"]) == 3
    
    def test_format_schema_custom_indent(self):
        """Test schema formatting with custom indentation."""
        schema = self.generator.generate_schema(self.sample_faqs)
        formatted = self.generator.format_schema(schema, indent=4)
        
        # Check that indentation is 4 spaces
        lines = formatted.split('\n')
        for line in lines[1:]:  # Skip first line
            if line.strip():  # Non-empty line
                assert line.startswith('    ') or line.startswith('  ')  # 4 or 2 spaces
    
    def test_add_metadata(self):
        """Test adding metadata to schema."""
        schema = self.generator.generate_schema(self.sample_faqs)
        
        metadata = {
            "title": "Dental FAQs",
            "description": "Frequently asked questions",
            "url": "https://example.com",
            "author": "Dr. Smith",
            "publisher": "Dental Practice",
            "dateModified": "2024-01-01"
        }
        
        updated_schema = self.generator.add_metadata(schema, **metadata)
        
        assert updated_schema["name"] == "Dental FAQs"
        assert updated_schema["description"] == "Frequently asked questions"
        assert updated_schema["url"] == "https://example.com"
        assert updated_schema["author"]["name"] == "Dr. Smith"
        assert updated_schema["publisher"]["name"] == "Dental Practice"
        assert updated_schema["dateModified"] == "2024-01-01"
    
    def test_create_embedded_schema(self):
        """Test creation of embedded HTML schema."""
        schema = self.generator.generate_schema(self.sample_faqs)
        embedded = self.generator.create_embedded_schema(schema)
        
        assert isinstance(embedded, str)
        assert embedded.startswith('<script type="application/ld+json">')
        assert embedded.endswith('</script>')
        assert 'FAQPage' in embedded
        assert 'Question' in embedded
    
    def test_schema_structure_completeness(self):
        """Test that generated schema has complete structure."""
        schema = self.generator.generate_schema(self.sample_faqs)
        
        # Check top-level structure
        assert "@context" in schema
        assert "@type" in schema
        assert "mainEntity" in schema
        assert "dateCreated" in schema
        
        # Check mainEntity structure
        main_entity = schema["mainEntity"]
        assert isinstance(main_entity, list)
        assert len(main_entity) == 3
        
        for entity in main_entity:
            assert "@type" in entity
            assert entity["@type"] == "Question"
            assert "name" in entity
            assert "acceptedAnswer" in entity
            
            answer = entity["acceptedAnswer"]
            assert answer["@type"] == "Answer"
            assert "text" in answer
    
    def test_schema_with_different_faq_counts(self):
        """Test schema generation with different FAQ counts."""
        # Test with minimum FAQs
        min_faqs = self.sample_faqs[:3]
        schema = self.generator.generate_schema(min_faqs)
        assert len(schema["mainEntity"]) == 3
        
        # Test with maximum FAQs
        max_faqs = self.sample_faqs * 2  # 6 FAQs
        schema = self.generator.generate_schema(max_faqs)
        assert len(schema["mainEntity"]) == 6









