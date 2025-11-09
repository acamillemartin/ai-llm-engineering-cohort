"""
Schema Validation Module

This module handles validation of JSON-LD schema markup using various methods
including Google's Rich Results Test API and local validation.
"""

import json
import requests
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SchemaValidator:
    """
    Validator for JSON-LD schema markup.
    
    This class provides validation methods for FAQPage schema including
    structure validation, Google Rich Results Test integration, and
    SEO best practices checking.
    """
    
    def __init__(self):
        """Initialize the schema validator."""
        self.google_test_url = "https://search.google.com/test/rich-results"
        self.schema_org_url = "https://schema.org/FAQPage"
    
    def validate_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive schema validation.
        
        Args:
            schema: JSON-LD schema dictionary to validate
            
        Returns:
            Validation results with validity status and issues
        """
        results = {
            'valid': True,
            'issues': [],
            'warnings': [],
            'suggestions': [],
            'google_validation': None
        }
        
        try:
            # Basic structure validation
            structure_results = self._validate_structure(schema)
            results.update(structure_results)
            
            # Content validation
            content_results = self._validate_content(schema)
            results['issues'].extend(content_results.get('issues', []))
            results['warnings'].extend(content_results.get('warnings', []))
            results['suggestions'].extend(content_results.get('suggestions', []))
            
            # SEO validation
            seo_results = self._validate_seo_practices(schema)
            results['warnings'].extend(seo_results.get('warnings', []))
            results['suggestions'].extend(seo_results.get('suggestions', []))
            
            # Update overall validity
            if results['issues']:
                results['valid'] = False
            
            logger.info(f"Schema validation completed. Valid: {results['valid']}")
            return results
            
        except Exception as e:
            logger.error(f"Schema validation error: {str(e)}")
            results['valid'] = False
            results['issues'].append(f"Validation error: {str(e)}")
            return results
    
    def _validate_structure(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the basic structure of the schema."""
        results = {
            'valid': True,
            'issues': [],
            'warnings': []
        }
        
        # Check required top-level fields
        required_fields = ['@context', '@type', 'mainEntity']
        for field in required_fields:
            if field not in schema:
                results['issues'].append(f"Missing required field: {field}")
                results['valid'] = False
        
        # Validate @context
        if '@context' in schema and schema['@context'] != 'https://schema.org':
            results['warnings'].append("@context should be 'https://schema.org'")
        
        # Validate @type
        if '@type' in schema and schema['@type'] != 'FAQPage':
            results['issues'].append("@type must be 'FAQPage'")
            results['valid'] = False
        
        # Validate mainEntity
        if 'mainEntity' in schema:
            main_entity = schema['mainEntity']
            if not isinstance(main_entity, list):
                results['issues'].append("mainEntity must be a list")
                results['valid'] = False
            elif len(main_entity) == 0:
                results['issues'].append("mainEntity cannot be empty")
                results['valid'] = False
            else:
                # Validate each question entity
                for i, entity in enumerate(main_entity):
                    entity_results = self._validate_question_entity(entity, i)
                    results['issues'].extend(entity_results.get('issues', []))
                    results['warnings'].extend(entity_results.get('warnings', []))
        
        return results
    
    def _validate_question_entity(self, entity: Dict[str, Any], index: int) -> Dict[str, List[str]]:
        """Validate a single question entity."""
        results = {'issues': [], 'warnings': []}
        
        # Check required fields
        required_fields = ['@type', 'name', 'acceptedAnswer']
        for field in required_fields:
            if field not in entity:
                results['issues'].append(f"Question {index}: Missing required field '{field}'")
        
        # Validate @type
        if entity.get('@type') != 'Question':
            results['issues'].append(f"Question {index}: @type must be 'Question'")
        
        # Validate name (question)
        if 'name' in entity:
            name = entity['name']
            if not isinstance(name, str) or not name.strip():
                results['issues'].append(f"Question {index}: 'name' must be a non-empty string")
            elif len(name) < 10:
                results['warnings'].append(f"Question {index}: Question is very short")
            elif len(name) > 200:
                results['warnings'].append(f"Question {index}: Question is very long")
        
        # Validate acceptedAnswer
        if 'acceptedAnswer' in entity:
            answer = entity['acceptedAnswer']
            if not isinstance(answer, dict):
                results['issues'].append(f"Question {index}: acceptedAnswer must be a dictionary")
            else:
                if answer.get('@type') != 'Answer':
                    results['issues'].append(f"Question {index}: acceptedAnswer @type must be 'Answer'")
                
                if 'text' not in answer:
                    results['issues'].append(f"Question {index}: acceptedAnswer missing 'text' field")
                else:
                    text = answer['text']
                    if not isinstance(text, str) or not text.strip():
                        results['issues'].append(f"Question {index}: acceptedAnswer text must be non-empty")
                    elif len(text) < 20:
                        results['warnings'].append(f"Question {index}: Answer is very short")
                    elif len(text) > 1000:
                        results['warnings'].append(f"Question {index}: Answer is very long")
        
        return results
    
    def _validate_content(self, schema: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate content quality and relevance."""
        results = {'issues': [], 'warnings': [], 'suggestions': []}
        
        main_entity = schema.get('mainEntity', [])
        
        # Check for duplicate questions
        questions = [entity.get('name', '') for entity in main_entity if isinstance(entity, dict)]
        if len(questions) != len(set(questions)):
            results['warnings'].append("Duplicate questions found")
        
        # Check question diversity
        if len(main_entity) >= 3:
            question_words = []
            for entity in main_entity:
                if isinstance(entity, dict) and 'name' in entity:
                    words = entity['name'].lower().split()
                    question_words.extend(words)
            
            # Check for repetitive question starters
            starters = [words[0] for words in [q.split() for q in questions if q.split()]]
            if len(set(starters)) < len(starters) * 0.7:
                results['suggestions'].append("Consider varying question starters for better diversity")
        
        # Check answer quality
        for i, entity in enumerate(main_entity):
            if isinstance(entity, dict) and 'acceptedAnswer' in entity:
                answer = entity['acceptedAnswer']
                if isinstance(answer, dict) and 'text' in answer:
                    text = answer['text']
                    if len(text) < 50:
                        results['suggestions'].append(f"Question {i+1}: Consider expanding the answer for better value")
        
        return results
    
    def _validate_seo_practices(self, schema: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate SEO best practices."""
        results = {'warnings': [], 'suggestions': []}
        
        # Check for metadata
        if 'name' not in schema:
            results['suggestions'].append("Consider adding a 'name' field for the FAQ page")
        
        if 'description' not in schema:
            results['suggestions'].append("Consider adding a 'description' field for better SEO")
        
        # Check question count
        main_entity = schema.get('mainEntity', [])
        if len(main_entity) < 3:
            results['warnings'].append("FAQ pages should have at least 3 questions for best SEO results")
        elif len(main_entity) > 10:
            results['warnings'].append("Consider limiting to 10 questions to avoid overwhelming users")
        
        # Check for keyword optimization
        questions = [entity.get('name', '') for entity in main_entity if isinstance(entity, dict)]
        if questions:
            # Check for common question patterns
            common_patterns = ['what', 'how', 'when', 'where', 'why', 'who']
            pattern_count = sum(1 for q in questions for pattern in common_patterns if q.lower().startswith(pattern))
            if pattern_count < len(questions) * 0.5:
                results['suggestions'].append("Consider using more common question patterns (What, How, When, etc.)")
        
        return results
    
    def validate_with_google(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate schema using Google's Rich Results Test (simulated).
        
        Note: This is a simulated validation. In production, you would integrate
        with Google's actual Rich Results Test API.
        
        Args:
            schema: JSON-LD schema to validate
            
        Returns:
            Google validation results
        """
        results = {
            'valid': True,
            'issues': [],
            'warnings': [],
            'rich_results': True
        }
        
        try:
            # Simulate Google validation
            # In a real implementation, you would make an API call to Google's service
            
            # Check for FAQPage support
            if schema.get('@type') != 'FAQPage':
                results['valid'] = False
                results['issues'].append("Schema type not supported for rich results")
                return results
            
            # Check minimum requirements
            main_entity = schema.get('mainEntity', [])
            if len(main_entity) < 1:
                results['valid'] = False
                results['issues'].append("No questions found")
                return results
            
            # Validate each question for Google requirements
            for i, entity in enumerate(main_entity):
                if not isinstance(entity, dict):
                    results['valid'] = False
                    results['issues'].append(f"Question {i+1} is not properly formatted")
                    continue
                
                if entity.get('@type') != 'Question':
                    results['valid'] = False
                    results['issues'].append(f"Question {i+1} has invalid type")
                
                if not entity.get('name'):
                    results['valid'] = False
                    results['issues'].append(f"Question {i+1} missing question text")
                
                answer = entity.get('acceptedAnswer', {})
                if not isinstance(answer, dict) or answer.get('@type') != 'Answer':
                    results['valid'] = False
                    results['issues'].append(f"Question {i+1} has invalid answer format")
                
                if not answer.get('text'):
                    results['valid'] = False
                    results['issues'].append(f"Question {i+1} missing answer text")
            
            # Check for rich results eligibility
            if results['valid'] and len(main_entity) >= 3:
                results['rich_results'] = True
                results['warnings'].append("Schema is eligible for rich results")
            else:
                results['rich_results'] = False
                results['warnings'].append("Schema may not be eligible for rich results")
            
            logger.info(f"Google validation completed. Valid: {results['valid']}")
            return results
            
        except Exception as e:
            logger.error(f"Google validation error: {str(e)}")
            results['valid'] = False
            results['issues'].append(f"Validation error: {str(e)}")
            return results
    
    def get_validation_summary(self, validation_results: Dict[str, Any]) -> str:
        """
        Generate a human-readable validation summary.
        
        Args:
            validation_results: Results from validate_schema method
            
        Returns:
            Formatted summary string
        """
        summary_parts = []
        
        if validation_results['valid']:
            summary_parts.append("✅ Schema is valid and ready for use!")
        else:
            summary_parts.append("❌ Schema has validation errors")
        
        if validation_results['issues']:
            summary_parts.append("\n🚨 Issues found:")
            for issue in validation_results['issues']:
                summary_parts.append(f"  • {issue}")
        
        if validation_results['warnings']:
            summary_parts.append("\n⚠️ Warnings:")
            for warning in validation_results['warnings']:
                summary_parts.append(f"  • {warning}")
        
        if validation_results['suggestions']:
            summary_parts.append("\n💡 Suggestions:")
            for suggestion in validation_results['suggestions']:
                summary_parts.append(f"  • {suggestion}")
        
        return "\n".join(summary_parts)

