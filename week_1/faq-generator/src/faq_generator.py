"""
FAQ Generator Module

This module handles the core FAQ generation logic using OpenAI's API.
It includes prompt engineering, response parsing, and quality validation.
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from openai import OpenAI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FAQ:
    """Data class representing a single FAQ item."""
    question: str
    answer: str
    category: Optional[str] = None
    keywords: Optional[List[str]] = None


class FAQGenerator:
    """
    Main class for generating FAQs using OpenAI's API.
    
    This class handles the complete FAQ generation pipeline including
    prompt construction, API calls, response parsing, and quality validation.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """
        Initialize the FAQ generator.
        
        Args:
            api_key: OpenAI API key
            model: OpenAI model to use for generation
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, str]:
        """Load prompt templates for different tones and scenarios."""
        return {
            "friendly": """
You are a helpful assistant that creates engaging, friendly FAQs for businesses. 
Generate {num_faqs} frequently asked questions and answers based on the business information provided.

Business Information: {business_info}

Requirements:
- Questions should be natural and conversational
- Answers should be helpful and easy to understand
- Use a friendly, approachable tone
- Focus on customer concerns and benefits
- Keep answers concise but informative (2-3 sentences)
- Make questions specific to the business type

Format your response as a JSON array with this structure:
[
  {{
    "question": "What services do you offer?",
    "answer": "We provide comprehensive dental care including...",
    "category": "Services"
  }}
]

Generate exactly {num_faqs} FAQs.
""",
            
            "formal": """
You are a professional assistant that creates formal, business-appropriate FAQs. 
Generate {num_faqs} frequently asked questions and answers based on the business information provided.

Business Information: {business_info}

Requirements:
- Questions should be professional and direct
- Answers should be authoritative and comprehensive
- Use formal business language
- Focus on technical details and processes
- Keep answers detailed and informative (3-4 sentences)
- Make questions specific to the business type

Format your response as a JSON array with this structure:
[
  {{
    "question": "What services do you offer?",
    "answer": "Our organization provides comprehensive dental care services including...",
    "category": "Services"
  }}
]

Generate exactly {num_faqs} FAQs.
""",
            
            "expert": """
You are an expert consultant that creates technical, detailed FAQs for businesses. 
Generate {num_faqs} frequently asked questions and answers based on the business information provided.

Business Information: {business_info}

Requirements:
- Questions should be specific and technical
- Answers should be detailed and expert-level
- Use professional terminology and industry jargon
- Focus on technical processes and methodologies
- Keep answers comprehensive (4-5 sentences)
- Make questions specific to the business type and industry

Format your response as a JSON array with this structure:
[
  {{
    "question": "What services do you offer?",
    "answer": "Our practice specializes in advanced dental procedures including...",
    "category": "Services"
  }}
]

Generate exactly {num_faqs} FAQs.
"""
        }
    
    def generate_faqs(
        self, 
        business_info: str, 
        tone: str = "friendly", 
        num_faqs: int = 5,
        model: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Generate FAQs based on business information.
        
        Args:
            business_info: Description of the business, products, or services
            tone: Tone for the FAQs (friendly, formal, expert)
            num_faqs: Number of FAQs to generate (3-5)
            model: OpenAI model to use (overrides default)
            
        Returns:
            List of FAQ dictionaries with question, answer, and category
        """
        try:
            # Validate inputs
            if not business_info.strip():
                raise ValueError("Business information cannot be empty")
            
            if tone not in self.prompts:
                raise ValueError(f"Invalid tone: {tone}. Must be one of {list(self.prompts.keys())}")
            
            if not 3 <= num_faqs <= 5:
                raise ValueError("Number of FAQs must be between 3 and 5")
            
            # Prepare prompt
            prompt = self.prompts[tone].format(
                business_info=business_info,
                num_faqs=num_faqs
            )
            
            # Generate response
            response = self._call_openai_api(prompt, model or self.model)
            
            # Parse and validate response
            faqs = self._parse_response(response)
            
            # Validate FAQ count
            if len(faqs) != num_faqs:
                logger.warning(f"Generated {len(faqs)} FAQs, expected {num_faqs}")
            
            # Add keywords to each FAQ
            for faq in faqs:
                faq['keywords'] = self._extract_keywords(faq['question'], faq['answer'])
            
            logger.info(f"Successfully generated {len(faqs)} FAQs with tone: {tone}")
            return faqs
            
        except Exception as e:
            logger.error(f"Error generating FAQs: {str(e)}")
            raise
    
    def _call_openai_api(self, prompt: str, model: str) -> str:
        """Make API call to OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert FAQ generator that creates high-quality, SEO-optimized FAQs for businesses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                top_p=0.9
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    def _parse_response(self, response: str) -> List[Dict[str, str]]:
        """Parse OpenAI response and extract FAQs."""
        try:
            # Clean the response
            response = response.strip()
            
            # Try to extract JSON from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                # If no JSON array found, try to parse the entire response
                json_str = response
            
            # Parse JSON
            faqs = json.loads(json_str)
            
            # Validate structure
            if not isinstance(faqs, list):
                raise ValueError("Response is not a list")
            
            # Validate each FAQ
            for i, faq in enumerate(faqs):
                if not isinstance(faq, dict):
                    raise ValueError(f"FAQ {i} is not a dictionary")
                
                required_fields = ['question', 'answer']
                for field in required_fields:
                    if field not in faq or not faq[field]:
                        raise ValueError(f"FAQ {i} missing required field: {field}")
                
                # Clean text
                faq['question'] = faq['question'].strip()
                faq['answer'] = faq['answer'].strip()
                
                # Add category if missing
                if 'category' not in faq:
                    faq['category'] = 'General'
            
            return faqs
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            raise ValueError("Failed to parse FAQ response as JSON")
        except Exception as e:
            logger.error(f"Response parsing error: {str(e)}")
            raise
    
    def _extract_keywords(self, question: str, answer: str) -> List[str]:
        """Extract relevant keywords from question and answer."""
        # Simple keyword extraction (can be enhanced with NLP libraries)
        text = f"{question} {answer}".lower()
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
        keywords = [word for word in words if word not in stop_words]
        
        # Return top 5 unique keywords
        return list(dict.fromkeys(keywords))[:5]
    
    def validate_faqs(self, faqs: List[Dict[str, str]]) -> Dict[str, any]:
        """
        Validate the quality of generated FAQs.
        
        Args:
            faqs: List of FAQ dictionaries
            
        Returns:
            Validation results dictionary
        """
        results = {
            'valid': True,
            'issues': [],
            'metrics': {}
        }
        
        try:
            # Check FAQ count
            if len(faqs) < 3:
                results['issues'].append("Too few FAQs generated")
                results['valid'] = False
            
            # Check for duplicates
            questions = [faq['question'].lower() for faq in faqs]
            if len(questions) != len(set(questions)):
                results['issues'].append("Duplicate questions found")
                results['valid'] = False
            
            # Check answer lengths
            answer_lengths = [len(faq['answer']) for faq in faqs]
            avg_length = sum(answer_lengths) / len(answer_lengths)
            results['metrics']['avg_answer_length'] = avg_length
            
            if avg_length < 50:
                results['issues'].append("Answers are too short")
                results['valid'] = False
            
            # Check for required fields
            for i, faq in enumerate(faqs):
                if not faq.get('question') or not faq.get('answer'):
                    results['issues'].append(f"FAQ {i+1} missing required fields")
                    results['valid'] = False
            
            return results
            
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            results['valid'] = False
            results['issues'].append(f"Validation error: {str(e)}")
            return results

