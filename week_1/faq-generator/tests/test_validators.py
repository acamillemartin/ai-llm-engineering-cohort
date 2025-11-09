"""
Tests for Schema Validators module.

This module contains unit tests for the SchemaValidator class,
including validation logic, Google Rich Results Test integration, and error handling.
"""

import pytest
from unittest.mock import Mock, patch
from src.validators import SchemaValidator


class TestSchemaValidator:
    """Test cases for SchemaValidator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = SchemaValidator()
        self.valid_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "What services do you offer?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "We provide comprehensive dental care including cleanings, fillings, and cosmetic procedures."
                    }
                },
                {
                    "@type": "Question",
                    "name": "How do I schedule an appointment?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "You can schedule an appointment by calling our office or using our online booking system."
                    }
                },
                {
                    "@type": "Question",
                    "name": "What are your office hours?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Our office is open Monday through Friday from 8 AM to 5 PM."
                    }
                }
            ]
        }
    
    def test_initialization(self):
        """Test SchemaValidator initialization."""
        validator = SchemaValidator()
        assert validator.google_test_url == "https://search.google.com/test/rich-results"
        assert validator.schema_org_url == "https://schema.org/FAQPage"
    
    def test_validate_schema_valid(self):
        """Test validation of valid schema."""
        results = self.validator.validate_schema(self.valid_schema)
        
        assert results["valid"] is True
        assert len(results["issues"]) == 0
        assert len(results["warnings"]) == 0
        assert len(results["suggestions"]) == 0
    
    def test_validate_schema_missing_required_fields(self):
        """Test validation with missing required fields."""
        invalid_schema = {
            "@type": "FAQPage"
            # Missing @context and mainEntity
        }
        
        results = self.validator.validate_schema(invalid_schema)
        
        assert results["valid"] is False
        assert "Missing required field: @context" in results["issues"]
        assert "Missing required field: mainEntity" in results["issues"]
    
    def test_validate_schema_invalid_context(self):
        """Test validation with invalid @context."""
        invalid_schema = self.valid_schema.copy()
        invalid_schema["@context"] = "https://example.com"
        
        results = self.validator.validate_schema(invalid_schema)
        
        assert results["valid"] is True  # Still valid, just a warning
        assert "@context should be 'https://schema.org'" in results["warnings"]
    
    def test_validate_schema_invalid_type(self):
        """Test validation with invalid @type."""
        invalid_schema = self.valid_schema.copy()
        invalid_schema["@type"] = "Article"
        
        results = self.validator.validate_schema(invalid_schema)
        
        assert results["valid"] is False
        assert "@type must be 'FAQPage'" in results["issues"]
    
    def test_validate_schema_empty_main_entity(self):
        """Test validation with empty mainEntity."""
        invalid_schema = self.valid_schema.copy()
        invalid_schema["mainEntity"] = []
        
        results = self.validator.validate_schema(invalid_schema)
        
        assert results["valid"] is False
        assert "mainEntity cannot be empty" in results["issues"]
    
    def test_validate_schema_invalid_main_entity_type(self):
        """Test validation with invalid mainEntity type."""
        invalid_schema = self.valid_schema.copy()
        invalid_schema["mainEntity"] = "not a list"
        
        results = self.validator.validate_schema(invalid_schema)
        
        assert results["valid"] is False
        assert "mainEntity must be a list" in results["issues"]
    
    def test_validate_question_entity_valid(self):
        """Test validation of valid question entity."""
        entity = {
            "@type": "Question",
            "name": "What services do you offer?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "We provide comprehensive dental care."
            }
        }
        
        results = self.validator._validate_question_entity(entity, 0)
        
        assert len(results["issues"]) == 0
        assert len(results["warnings"]) == 0
    
    def test_validate_question_entity_missing_fields(self):
        """Test validation of question entity with missing fields."""
        entity = {
            "@type": "Question"
            # Missing name and acceptedAnswer
        }
        
        results = self.validator._validate_question_entity(entity, 0)
        
        assert "Missing required field 'name'" in results["issues"]
        assert "Missing required field 'acceptedAnswer'" in results["issues"]
    
    def test_validate_question_entity_invalid_type(self):
        """Test validation of question entity with invalid @type."""
        entity = {
            "@type": "Article",  # Should be Question
            "name": "What services do you offer?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "We provide comprehensive dental care."
            }
        }
        
        results = self.validator._validate_question_entity(entity, 0)
        
        assert "@type must be 'Question'" in results["issues"]
    
    def test_validate_question_entity_invalid_answer(self):
        """Test validation of question entity with invalid answer."""
        entity = {
            "@type": "Question",
            "name": "What services do you offer?",
            "acceptedAnswer": {
                "@type": "Article",  # Should be Answer
                "text": "We provide comprehensive dental care."
            }
        }
        
        results = self.validator._validate_question_entity(entity, 0)
        
        assert "acceptedAnswer @type must be 'Answer'" in results["issues"]
    
    def test_validate_question_entity_missing_answer_text(self):
        """Test validation of question entity with missing answer text."""
        entity = {
            "@type": "Question",
            "name": "What services do you offer?",
            "acceptedAnswer": {
                "@type": "Answer"
                # Missing text field
            }
        }
        
        results = self.validator._validate_question_entity(entity, 0)
        
        assert "acceptedAnswer missing 'text' field" in results["issues"]
    
    def test_validate_question_entity_short_question(self):
        """Test validation of question entity with very short question."""
        entity = {
            "@type": "Question",
            "name": "What?",  # Very short
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "We provide comprehensive dental care."
            }
        }
        
        results = self.validator._validate_question_entity(entity, 0)
        
        assert "Question is very short" in results["warnings"]
    
    def test_validate_question_entity_long_question(self):
        """Test validation of question entity with very long question."""
        entity = {
            "@type": "Question",
            "name": "What services do you offer and how do they work and what are the benefits and costs and how long do they take and what should I expect during the process and what are the risks and complications and how do I prepare and what should I bring and what happens after the procedure and how do I care for myself and when should I call you and what are your office hours and how do I schedule an appointment and what insurance do you accept and what payment methods do you take and do you offer financing and what are your cancellation policies and what should I do if I have an emergency and how do I contact you and what are your credentials and experience and what makes you different from other providers and what do your patients say about you and how can I learn more about your services and what resources do you provide and how do I get started and what is the next step?",  # Very long
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "We provide comprehensive dental care."
            }
        }
        
        results = self.validator._validate_question_entity(entity, 0)
        
        assert "Question is very long" in results["warnings"]
    
    def test_validate_question_entity_short_answer(self):
        """Test validation of question entity with very short answer."""
        entity = {
            "@type": "Question",
            "name": "What services do you offer?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Dental care."  # Very short
            }
        }
        
        results = self.validator._validate_question_entity(entity, 0)
        
        assert "Answer is very short" in results["warnings"]
    
    def test_validate_question_entity_long_answer(self):
        """Test validation of question entity with very long answer."""
        entity = {
            "@type": "Question",
            "name": "What services do you offer?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "We provide comprehensive dental care including but not limited to routine cleanings, fillings, crowns, bridges, implants, root canals, extractions, cosmetic procedures, orthodontics, periodontics, endodontics, oral surgery, emergency care, preventive care, diagnostic services, treatment planning, patient education, follow-up care, maintenance, and ongoing support to ensure optimal oral health and patient satisfaction."  # Very long
            }
        }
        
        results = self.validator._validate_question_entity(entity, 0)
        
        assert "Answer is very long" in results["warnings"]
    
    def test_validate_content_duplicate_questions(self):
        """Test content validation with duplicate questions."""
        schema = self.valid_schema.copy()
        schema["mainEntity"] = [
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
                "name": "What services do you offer?",  # Duplicate
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "We provide comprehensive dental care."
                }
            }
        ]
        
        results = self.validator._validate_content(schema)
        
        assert "Duplicate questions found" in results["warnings"]
    
    def test_validate_content_question_diversity(self):
        """Test content validation for question diversity."""
        schema = self.valid_schema.copy()
        schema["mainEntity"] = [
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
                "name": "What services do you provide?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "We provide comprehensive dental care."
                }
            },
            {
                "@type": "Question",
                "name": "What services do you have?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "We provide comprehensive dental care."
                }
            }
        ]
        
        results = self.validator._validate_content(schema)
        
        assert "Consider varying question starters" in results["suggestions"]
    
    def test_validate_seo_practices_missing_metadata(self):
        """Test SEO validation with missing metadata."""
        results = self.validator._validate_seo_practices(self.valid_schema)
        
        assert "Consider adding a 'name' field" in results["suggestions"]
        assert "Consider adding a 'description' field" in results["suggestions"]
    
    def test_validate_seo_practices_too_few_questions(self):
        """Test SEO validation with too few questions."""
        schema = self.valid_schema.copy()
        schema["mainEntity"] = schema["mainEntity"][:2]  # Only 2 questions
        
        results = self.validator._validate_seo_practices(schema)
        
        assert "FAQ pages should have at least 3 questions" in results["warnings"]
    
    def test_validate_seo_practices_too_many_questions(self):
        """Test SEO validation with too many questions."""
        schema = self.valid_schema.copy()
        # Create 15 questions
        schema["mainEntity"] = [
            {
                "@type": "Question",
                "name": f"What is question {i}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"This is answer {i}."
                }
            }
            for i in range(15)
        ]
        
        results = self.validator._validate_seo_practices(schema)
        
        assert "Consider limiting to 10 questions" in results["warnings"]
    
    def test_validate_seo_practices_question_patterns(self):
        """Test SEO validation for question patterns."""
        schema = self.valid_schema.copy()
        schema["mainEntity"] = [
            {
                "@type": "Question",
                "name": "Is this a good question?",  # Not a common pattern
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes, this is a good question."
                }
            },
            {
                "@type": "Question",
                "name": "Are you open today?",  # Not a common pattern
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes, we are open today."
                }
            }
        ]
        
        results = self.validator._validate_seo_practices(schema)
        
        assert "Consider using more common question patterns" in results["suggestions"]
    
    def test_validate_with_google_valid(self):
        """Test Google validation with valid schema."""
        results = self.validator.validate_with_google(self.valid_schema)
        
        assert results["valid"] is True
        assert results["rich_results"] is True
        assert len(results["issues"]) == 0
    
    def test_validate_with_google_invalid_type(self):
        """Test Google validation with invalid schema type."""
        invalid_schema = self.valid_schema.copy()
        invalid_schema["@type"] = "Article"
        
        results = self.validator.validate_with_google(invalid_schema)
        
        assert results["valid"] is False
        assert "Schema type not supported" in results["issues"]
    
    def test_validate_with_google_no_questions(self):
        """Test Google validation with no questions."""
        invalid_schema = self.valid_schema.copy()
        invalid_schema["mainEntity"] = []
        
        results = self.validator.validate_with_google(invalid_schema)
        
        assert results["valid"] is False
        assert "No questions found" in results["issues"]
    
    def test_validate_with_google_invalid_question(self):
        """Test Google validation with invalid question format."""
        invalid_schema = self.valid_schema.copy()
        invalid_schema["mainEntity"] = [
            "not a dictionary"  # Invalid format
        ]
        
        results = self.validator.validate_with_google(invalid_schema)
        
        assert results["valid"] is False
        assert "Question 1 is not properly formatted" in results["issues"]
    
    def test_validate_with_google_few_questions(self):
        """Test Google validation with few questions."""
        schema = self.valid_schema.copy()
        schema["mainEntity"] = schema["mainEntity"][:2]  # Only 2 questions
        
        results = self.validator.validate_with_google(schema)
        
        assert results["valid"] is True
        assert results["rich_results"] is False
        assert "Schema may not be eligible for rich results" in results["warnings"]
    
    def test_get_validation_summary_valid(self):
        """Test validation summary for valid schema."""
        results = {
            "valid": True,
            "issues": [],
            "warnings": [],
            "suggestions": []
        }
        
        summary = self.validator.get_validation_summary(results)
        
        assert "✅ Schema is valid and ready for use!" in summary
        assert "🚨 Issues found:" not in summary
        assert "⚠️ Warnings:" not in summary
        assert "💡 Suggestions:" not in summary
    
    def test_get_validation_summary_with_issues(self):
        """Test validation summary with issues."""
        results = {
            "valid": False,
            "issues": ["Missing required field: @context"],
            "warnings": [],
            "suggestions": []
        }
        
        summary = self.validator.get_validation_summary(results)
        
        assert "❌ Schema has validation errors" in summary
        assert "🚨 Issues found:" in summary
        assert "Missing required field: @context" in summary
    
    def test_get_validation_summary_with_warnings(self):
        """Test validation summary with warnings."""
        results = {
            "valid": True,
            "issues": [],
            "warnings": ["Question is very short"],
            "suggestions": []
        }
        
        summary = self.validator.get_validation_summary(results)
        
        assert "✅ Schema is valid and ready for use!" in summary
        assert "⚠️ Warnings:" in summary
        assert "Question is very short" in summary
    
    def test_get_validation_summary_with_suggestions(self):
        """Test validation summary with suggestions."""
        results = {
            "valid": True,
            "issues": [],
            "warnings": [],
            "suggestions": ["Consider adding a 'name' field"]
        }
        
        summary = self.validator.get_validation_summary(results)
        
        assert "✅ Schema is valid and ready for use!" in summary
        assert "💡 Suggestions:" in summary
        assert "Consider adding a 'name' field" in summary









