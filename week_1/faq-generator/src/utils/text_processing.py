"""
Text Processing Utilities

This module provides text processing functions for cleaning,
analyzing, and extracting information from text content.
"""

import re
import string
from typing import List, Dict, Set, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_text(text: str, remove_html: bool = True, normalize_whitespace: bool = True) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Input text to clean
        remove_html: Whether to remove HTML tags
        normalize_whitespace: Whether to normalize whitespace
        
    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    
    try:
        # Remove HTML tags if requested
        if remove_html:
            text = re.sub(r'<[^>]+>', '', text)
        
        # Normalize whitespace
        if normalize_whitespace:
            text = re.sub(r'\s+', ' ', text)
        
        # Remove extra whitespace
        text = text.strip()
        
        return text
        
    except Exception as e:
        logger.error(f"Error cleaning text: {str(e)}")
        return text


def extract_keywords(text: str, min_length: int = 3, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text using simple frequency analysis.
    
    Args:
        text: Input text to analyze
        min_length: Minimum word length for keywords
        max_keywords: Maximum number of keywords to return
        
    Returns:
        List of extracted keywords
    """
    if not text:
        return []
    
    try:
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Split into words
        words = text.split()
        
        # Filter words by length
        words = [word for word in words if len(word) >= min_length]
        
        # Remove common stop words
        stop_words = get_stop_words()
        words = [word for word in words if word not in stop_words]
        
        # Count word frequency
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        keywords = [word for word, freq in sorted_words[:max_keywords]]
        
        return keywords
        
    except Exception as e:
        logger.error(f"Error extracting keywords: {str(e)}")
        return []


def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract named entities from text (simplified version).
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with entity types and lists of entities
    """
    if not text:
        return {}
    
    try:
        entities = {
            'organizations': [],
            'locations': [],
            'people': [],
            'products': [],
            'services': []
        }
        
        # Simple pattern matching for common entities
        # Organizations (capitalized words that might be companies)
        org_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        potential_orgs = re.findall(org_pattern, text)
        
        # Filter out common words that aren't organizations
        common_words = {'The', 'This', 'That', 'These', 'Those', 'We', 'Our', 'Your'}
        for org in potential_orgs:
            if org not in common_words and len(org) > 3:
                entities['organizations'].append(org)
        
        # Locations (words that might be places)
        location_indicators = ['in', 'at', 'near', 'located', 'address']
        for indicator in location_indicators:
            pattern = rf'{indicator}\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
            matches = re.findall(pattern, text)
            entities['locations'].extend(matches)
        
        # Products/Services (words that might be offerings)
        service_indicators = ['service', 'product', 'offering', 'solution']
        for indicator in service_indicators:
            pattern = rf'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+{indicator}'
            matches = re.findall(pattern, text)
            entities['products'].extend(matches)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
        
    except Exception as e:
        logger.error(f"Error extracting entities: {str(e)}")
        return {}


def get_stop_words() -> Set[str]:
    """Get a set of common English stop words."""
    return {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
        'to', 'was', 'will', 'with', 'you', 'your', 'we', 'our', 'us',
        'they', 'them', 'their', 'this', 'these', 'those', 'i', 'me',
        'my', 'mine', 'can', 'could', 'should', 'would', 'may', 'might',
        'must', 'shall', 'do', 'does', 'did', 'have', 'has', 'had',
        'am', 'is', 'are', 'was', 'were', 'been', 'being', 'get', 'got',
        'make', 'made', 'take', 'took', 'come', 'came', 'go', 'went',
        'see', 'saw', 'know', 'knew', 'think', 'thought', 'say', 'said',
        'tell', 'told', 'give', 'gave', 'find', 'found', 'look', 'looked',
        'use', 'used', 'work', 'worked', 'call', 'called', 'try', 'tried',
        'ask', 'asked', 'need', 'needed', 'feel', 'felt', 'become', 'became',
        'leave', 'left', 'put', 'put', 'mean', 'meant', 'keep', 'kept',
        'let', 'let', 'begin', 'began', 'seem', 'seemed', 'help', 'helped',
        'talk', 'talked', 'turn', 'turned', 'start', 'started', 'show', 'showed',
        'hear', 'heard', 'play', 'played', 'run', 'ran', 'move', 'moved',
        'live', 'lived', 'believe', 'believed', 'hold', 'held', 'bring', 'brought',
        'happen', 'happened', 'write', 'wrote', 'provide', 'provided', 'sit', 'sat',
        'stand', 'stood', 'lose', 'lost', 'pay', 'paid', 'meet', 'met',
        'include', 'included', 'continue', 'continued', 'set', 'set', 'learn', 'learned',
        'change', 'changed', 'lead', 'led', 'understand', 'understood', 'watch', 'watched',
        'follow', 'followed', 'stop', 'stopped', 'create', 'created', 'speak', 'spoke',
        'read', 'read', 'allow', 'allowed', 'add', 'added', 'spend', 'spent',
        'grow', 'grew', 'open', 'opened', 'walk', 'walked', 'win', 'won',
        'offer', 'offered', 'remember', 'remembered', 'love', 'loved', 'consider', 'considered',
        'appear', 'appeared', 'buy', 'bought', 'wait', 'waited', 'serve', 'served',
        'die', 'died', 'send', 'sent', 'expect', 'expected', 'build', 'built',
        'stay', 'stayed', 'fall', 'fell', 'cut', 'cut', 'reach', 'reached',
        'kill', 'killed', 'remain', 'remained', 'suggest', 'suggested', 'raise', 'raised',
        'pass', 'passed', 'sell', 'sold', 'require', 'required', 'report', 'reported',
        'decide', 'decided', 'pull', 'pulled'
    }


def calculate_readability_score(text: str) -> Dict[str, float]:
    """
    Calculate basic readability metrics for text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with readability metrics
    """
    if not text:
        return {'score': 0, 'level': 'Unknown'}
    
    try:
        # Basic metrics
        sentences = len(re.findall(r'[.!?]+', text))
        words = len(text.split())
        characters = len(text)
        
        if sentences == 0 or words == 0:
            return {'score': 0, 'level': 'Unknown'}
        
        # Average words per sentence
        avg_words_per_sentence = words / sentences
        
        # Average characters per word
        avg_chars_per_word = characters / words
        
        # Simple readability score (simplified Flesch Reading Ease)
        score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_chars_per_word)
        
        # Determine reading level
        if score >= 90:
            level = 'Very Easy'
        elif score >= 80:
            level = 'Easy'
        elif score >= 70:
            level = 'Fairly Easy'
        elif score >= 60:
            level = 'Standard'
        elif score >= 50:
            level = 'Fairly Difficult'
        elif score >= 30:
            level = 'Difficult'
        else:
            level = 'Very Difficult'
        
        return {
            'score': round(score, 2),
            'level': level,
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'avg_chars_per_word': round(avg_chars_per_word, 2),
            'total_sentences': sentences,
            'total_words': words
        }
        
    except Exception as e:
        logger.error(f"Error calculating readability: {str(e)}")
        return {'score': 0, 'level': 'Unknown'}


def extract_question_patterns(text: str) -> List[str]:
    """
    Extract potential question patterns from text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        List of question patterns found
    """
    if not text:
        return []
    
    try:
        # Common question patterns
        patterns = [
            r'what\s+is\s+([^?]+)',
            r'how\s+do\s+([^?]+)',
            r'when\s+do\s+([^?]+)',
            r'where\s+can\s+([^?]+)',
            r'why\s+do\s+([^?]+)',
            r'who\s+can\s+([^?]+)',
            r'which\s+([^?]+)',
            r'how\s+much\s+([^?]+)',
            r'how\s+long\s+([^?]+)',
            r'how\s+often\s+([^?]+)'
        ]
        
        found_patterns = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            found_patterns.extend(matches)
        
        return found_patterns
        
    except Exception as e:
        logger.error(f"Error extracting question patterns: {str(e)}")
        return []









