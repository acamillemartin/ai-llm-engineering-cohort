"""
Prompt Templates for AI FAQ Generator

This module contains all the prompt templates used for generating FAQs
with different tones and styles. Templates are designed to produce
high-quality, SEO-optimized FAQs.
"""

from typing import Dict, List


class PromptTemplates:
    """Container for all prompt templates."""
    
    # Base system prompt for all FAQ generation
    SYSTEM_PROMPT = """You are an expert FAQ generator that creates high-quality, SEO-optimized FAQs for businesses. 
Your task is to generate relevant, helpful, and well-structured frequently asked questions and answers 
that will improve user experience and search engine visibility.

Guidelines:
- Questions should be natural and conversational
- Answers should be comprehensive but concise
- Focus on customer pain points and common concerns
- Use clear, accessible language
- Ensure questions are specific to the business type
- Make answers actionable and valuable
- Include relevant keywords naturally
- Structure answers with proper formatting when helpful"""

    # Tone-specific prompts
    FRIENDLY_PROMPT = """
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
- Use "you" and "your" to address customers directly
- Include reassuring language when appropriate

Format your response as a JSON array with this structure:
[
  {{
    "question": "What services do you offer?",
    "answer": "We provide comprehensive dental care including...",
    "category": "Services"
  }}
]

Generate exactly {num_faqs} FAQs."""

    FORMAL_PROMPT = """
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
- Use third-person perspective when appropriate
- Include specific details and procedures

Format your response as a JSON array with this structure:
[
  {{
    "question": "What services do you offer?",
    "answer": "Our organization provides comprehensive dental care services including...",
    "category": "Services"
  }}
]

Generate exactly {num_faqs} FAQs."""

    EXPERT_PROMPT = """
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
- Include technical specifications when relevant
- Address complex customer concerns

Format your response as a JSON array with this structure:
[
  {{
    "question": "What services do you offer?",
    "answer": "Our practice specializes in advanced dental procedures including...",
    "category": "Services"
  }}
]

Generate exactly {num_faqs} FAQs."""

    # Specialized prompts for different business types
    ECOMMERCE_PROMPT = """
You are an e-commerce expert that creates FAQs for online stores. 
Generate {num_faqs} frequently asked questions and answers based on the business information provided.

Business Information: {business_info}

Requirements:
- Focus on shipping, returns, payments, and product information
- Address common e-commerce concerns
- Include practical information about ordering process
- Cover customer service and support topics
- Use e-commerce terminology appropriately
- Address security and privacy concerns

Format your response as a JSON array with this structure:
[
  {{
    "question": "What is your return policy?",
    "answer": "We offer a 30-day return policy for all items...",
    "category": "Returns"
  }}
]

Generate exactly {num_faqs} FAQs."""

    LOCAL_BUSINESS_PROMPT = """
You are a local business expert that creates FAQs for brick-and-mortar businesses. 
Generate {num_faqs} frequently asked questions and answers based on the business information provided.

Business Information: {business_info}

Requirements:
- Focus on location, hours, and local services
- Address accessibility and parking concerns
- Include information about local community involvement
- Cover appointment scheduling and walk-in policies
- Address local competition and unique value propositions
- Include information about local partnerships

Format your response as a JSON array with this structure:
[
  {{
    "question": "What are your business hours?",
    "answer": "We are open Monday through Friday from 8 AM to 6 PM...",
    "category": "Hours"
  }}
]

Generate exactly {num_faqs} FAQs."""

    SERVICE_BUSINESS_PROMPT = """
You are a service business expert that creates FAQs for service-based businesses. 
Generate {num_faqs} frequently asked questions and answers based on the business information provided.

Business Information: {business_info}

Requirements:
- Focus on service delivery and process
- Address pricing and consultation information
- Include information about expertise and qualifications
- Cover project timelines and deliverables
- Address client communication and feedback processes
- Include information about guarantees and warranties

Format your response as a JSON array with this structure:
[
  {{
    "question": "How long does a typical project take?",
    "answer": "Most projects are completed within 2-4 weeks depending on complexity...",
    "category": "Timeline"
  }}
]

Generate exactly {num_faqs} FAQs."""

    # Category-specific prompts
    CATEGORY_PROMPTS = {
        "services": "Focus on the specific services offered, their benefits, and how they work.",
        "pricing": "Address cost, value, payment options, and what's included in pricing.",
        "process": "Explain how the service works, what to expect, and the steps involved.",
        "qualifications": "Cover expertise, credentials, experience, and what makes you qualified.",
        "location": "Address physical location, accessibility, parking, and local area information.",
        "contact": "Include contact methods, response times, and how to reach the right person.",
        "guarantees": "Cover warranties, guarantees, satisfaction policies, and risk mitigation.",
        "preparation": "Explain what clients need to do before, during, and after service.",
        "emergency": "Address urgent situations, after-hours support, and emergency procedures.",
        "general": "Cover general business information, policies, and common concerns."
    }

    # Question pattern templates
    QUESTION_PATTERNS = {
        "what": [
            "What services do you offer?",
            "What is included in your service?",
            "What makes you different?",
            "What should I expect?",
            "What are your qualifications?"
        ],
        "how": [
            "How does the process work?",
            "How long does it take?",
            "How much does it cost?",
            "How do I get started?",
            "How do you ensure quality?"
        ],
        "when": [
            "When are you available?",
            "When should I contact you?",
            "When will I see results?",
            "When do you need payment?"
        ],
        "where": [
            "Where are you located?",
            "Where do you provide services?",
            "Where can I find more information?"
        ],
        "why": [
            "Why should I choose you?",
            "Why is this important?",
            "Why do you recommend this approach?"
        ],
        "who": [
            "Who will be working on my project?",
            "Who should I contact?",
            "Who is your ideal client?"
        ]
    }

    # Answer enhancement templates
    ANSWER_ENHANCEMENTS = {
        "benefits": "This approach provides several key benefits:",
        "process": "Here's how the process works:",
        "timeline": "The typical timeline is:",
        "cost": "Pricing is based on:",
        "guarantee": "We stand behind our work with:",
        "next_steps": "To get started:",
        "contact": "For more information:"
    }

    # SEO optimization keywords
    SEO_KEYWORDS = {
        "dental": ["dental care", "dentist", "oral health", "dental services", "dental practice"],
        "legal": ["lawyer", "attorney", "legal services", "legal advice", "law firm"],
        "medical": ["medical care", "doctor", "healthcare", "medical services", "clinic"],
        "fitness": ["fitness", "gym", "personal training", "workout", "exercise"],
        "beauty": ["beauty", "salon", "spa", "cosmetic", "aesthetic"],
        "automotive": ["auto repair", "car service", "automotive", "vehicle", "mechanic"],
        "home": ["home improvement", "contractor", "renovation", "repair", "maintenance"],
        "technology": ["IT services", "tech support", "software", "technology", "digital"],
        "education": ["education", "training", "learning", "courses", "instruction"],
        "finance": ["financial", "accounting", "tax", "investment", "financial planning"]
    }

    @classmethod
    def get_prompt(cls, tone: str, business_type: str = None) -> str:
        """
        Get the appropriate prompt template based on tone and business type.
        
        Args:
            tone: The tone for the FAQ (friendly, formal, expert)
            business_type: The type of business (ecommerce, local, service)
            
        Returns:
            The appropriate prompt template
        """
        # Base tone prompts
        tone_prompts = {
            "friendly": cls.FRIENDLY_PROMPT,
            "formal": cls.FORMAL_PROMPT,
            "expert": cls.EXPERT_PROMPT
        }
        
        # Business type specific prompts
        business_prompts = {
            "ecommerce": cls.ECOMMERCE_PROMPT,
            "local": cls.LOCAL_BUSINESS_PROMPT,
            "service": cls.SERVICE_BUSINESS_PROMPT
        }
        
        # Return business-specific prompt if available, otherwise use tone prompt
        if business_type and business_type in business_prompts:
            return business_prompts[business_type]
        
        return tone_prompts.get(tone, cls.FRIENDLY_PROMPT)
    
    @classmethod
    def get_system_prompt(cls) -> str:
        """Get the system prompt for FAQ generation."""
        return cls.SYSTEM_PROMPT
    
    @classmethod
    def get_category_guidance(cls, category: str) -> str:
        """Get guidance for a specific FAQ category."""
        return cls.CATEGORY_PROMPTS.get(category, "Focus on providing helpful, relevant information.")
    
    @classmethod
    def get_question_patterns(cls, question_type: str) -> List[str]:
        """Get question patterns for a specific type."""
        return cls.QUESTION_PATTERNS.get(question_type, [])
    
    @classmethod
    def get_seo_keywords(cls, business_type: str) -> List[str]:
        """Get SEO keywords for a specific business type."""
        return cls.SEO_KEYWORDS.get(business_type, [])
    
    @classmethod
    def enhance_answer(cls, answer: str, enhancement_type: str) -> str:
        """Enhance an answer with specific formatting."""
        enhancement = cls.ANSWER_ENHANCEMENTS.get(enhancement_type, "")
        if enhancement:
            return f"{enhancement} {answer}"
        return answer









