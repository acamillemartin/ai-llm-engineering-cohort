"""
Schema Generator Module

This module handles the generation of JSON-LD schema markup for FAQs.
It creates valid FAQPage structured data that can be used for SEO optimization.
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SchemaGenerator:
    """
    Generator for JSON-LD FAQPage schema markup.
    
    This class creates valid structured data that can be embedded in web pages
    to help search engines understand and display FAQ content in rich snippets.
    """
    
    def __init__(self):
        """Initialize the schema generator."""
        self.schema_template = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": []
        }
    
    def generate_schema(self, faqs: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Generate JSON-LD schema for a list of FAQs.
        
        Args:
            faqs: List of FAQ dictionaries with question, answer, and optional category
            **kwargs: Additional metadata (title, description, url, etc.)
            
        Returns:
            Complete JSON-LD schema dictionary
        """
        try:
            if not faqs:
                raise ValueError("No FAQs provided for schema generation")
            
            # Create base schema
            schema = self.schema_template.copy()
            
            # Add main entity items
            main_entities = []
            for faq in faqs:
                entity = self._create_question_entity(faq)
                main_entities.append(entity)
            
            schema["mainEntity"] = main_entities
            
            # Add optional metadata
            if kwargs.get("title"):
                schema["name"] = kwargs["title"]
            
            if kwargs.get("description"):
                schema["description"] = kwargs["description"]
            
            if kwargs.get("url"):
                schema["url"] = kwargs["url"]
            
            # Add generation timestamp
            schema["dateCreated"] = datetime.now().isoformat()
            
            logger.info(f"Generated schema for {len(faqs)} FAQs")
            return schema
            
        except Exception as e:
            logger.error(f"Error generating schema: {str(e)}")
            raise
    
    def _create_question_entity(self, faq: Dict[str, str]) -> Dict[str, str]:
        """
        Create a Question entity for a single FAQ.
        
        Args:
            faq: FAQ dictionary with question, answer, and optional category
            
        Returns:
            Question entity dictionary
        """
        entity = {
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        }
        
        # Add category if available
        if faq.get("category"):
            entity["about"] = {
                "@type": "Thing",
                "name": faq["category"]
            }
        
        # Add keywords if available
        if faq.get("keywords"):
            entity["keywords"] = ", ".join(faq["keywords"])
        
        return entity
    
    def validate_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the generated schema structure.
        
        Args:
            schema: JSON-LD schema dictionary
            
        Returns:
            Validation results dictionary
        """
        results = {
            'valid': True,
            'issues': [],
            'warnings': []
        }
        
        try:
            # Check required fields
            if "@context" not in schema:
                results['issues'].append("Missing @context field")
                results['valid'] = False
            
            if "@type" not in schema:
                results['issues'].append("Missing @type field")
                results['valid'] = False
            
            if schema.get("@type") != "FAQPage":
                results['issues'].append("Invalid @type, should be 'FAQPage'")
                results['valid'] = False
            
            if "mainEntity" not in schema:
                results['issues'].append("Missing mainEntity field")
                results['valid'] = False
            
            # Validate mainEntity structure
            main_entities = schema.get("mainEntity", [])
            if not isinstance(main_entities, list):
                results['issues'].append("mainEntity must be a list")
                results['valid'] = False
            
            # Validate each question entity
            for i, entity in enumerate(main_entities):
                if not isinstance(entity, dict):
                    results['issues'].append(f"Entity {i} is not a dictionary")
                    results['valid'] = False
                    continue
                
                if entity.get("@type") != "Question":
                    results['issues'].append(f"Entity {i} has invalid @type")
                    results['valid'] = False
                
                if "name" not in entity:
                    results['issues'].append(f"Entity {i} missing 'name' field")
                    results['valid'] = False
                
                if "acceptedAnswer" not in entity:
                    results['issues'].append(f"Entity {i} missing 'acceptedAnswer' field")
                    results['valid'] = False
                else:
                    answer = entity["acceptedAnswer"]
                    if not isinstance(answer, dict):
                        results['issues'].append(f"Entity {i} acceptedAnswer is not a dictionary")
                        results['valid'] = False
                    elif answer.get("@type") != "Answer":
                        results['issues'].append(f"Entity {i} acceptedAnswer has invalid @type")
                        results['valid'] = False
                    elif "text" not in answer:
                        results['issues'].append(f"Entity {i} acceptedAnswer missing 'text' field")
                        results['valid'] = False
            
            # Check for warnings
            if len(main_entities) < 3:
                results['warnings'].append("Schema has fewer than 3 questions")
            
            if len(main_entities) > 10:
                results['warnings'].append("Schema has more than 10 questions (may be too long)")
            
            return results
            
        except Exception as e:
            logger.error(f"Schema validation error: {str(e)}")
            results['valid'] = False
            results['issues'].append(f"Validation error: {str(e)}")
            return results
    
    def format_schema(self, schema: Dict[str, Any], indent: int = 2) -> str:
        """
        Format schema as pretty-printed JSON string.
        
        Args:
            schema: JSON-LD schema dictionary
            indent: Number of spaces for indentation
            
        Returns:
            Formatted JSON string
        """
        try:
            return json.dumps(schema, indent=indent, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error formatting schema: {str(e)}")
            raise
    
    def add_metadata(self, schema: Dict[str, Any], **metadata) -> Dict[str, Any]:
        """
        Add additional metadata to the schema.
        
        Args:
            schema: Base schema dictionary
            **metadata: Additional metadata fields
            
        Returns:
            Updated schema with metadata
        """
        try:
            # Add common metadata fields
            if "title" in metadata:
                schema["name"] = metadata["title"]
            
            if "description" in metadata:
                schema["description"] = metadata["description"]
            
            if "url" in metadata:
                schema["url"] = metadata["url"]
            
            if "author" in metadata:
                schema["author"] = {
                    "@type": "Person",
                    "name": metadata["author"]
                }
            
            if "publisher" in metadata:
                schema["publisher"] = {
                    "@type": "Organization",
                    "name": metadata["publisher"]
                }
            
            if "dateModified" in metadata:
                schema["dateModified"] = metadata["dateModified"]
            
            logger.info("Added metadata to schema")
            return schema
            
        except Exception as e:
            logger.error(f"Error adding metadata: {str(e)}")
            raise
    
    def create_embedded_schema(self, schema: Dict[str, Any]) -> str:
        """
        Create HTML script tag with embedded schema.
        
        Args:
            schema: JSON-LD schema dictionary
            
        Returns:
            HTML script tag with embedded schema
        """
        try:
            schema_json = self.format_schema(schema)
            return f'<script type="application/ld+json">\n{schema_json}\n</script>'
        except Exception as e:
            logger.error(f"Error creating embedded schema: {str(e)}")
            raise

