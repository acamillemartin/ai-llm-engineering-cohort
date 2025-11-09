"""
URL Content Extractor

This module provides functionality to extract content from URLs
for use in FAQ generation. It handles web scraping and content
processing for various website types.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from typing import Dict, List, Optional, Tuple
import logging
import time
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLContentExtractor:
    """
    Extracts content from URLs for FAQ generation.
    
    This class handles web scraping, content cleaning, and text extraction
    from various website types to provide business information for FAQ generation.
    """
    
    def __init__(self, timeout: int = 10, max_retries: int = 3):
        """
        Initialize the URL content extractor.
        
        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_content(self, url: str) -> Optional[str]:
        """
        Extract main content from a URL.
        
        Args:
            url: URL to extract content from
            
        Returns:
            Extracted text content or None if extraction fails
        """
        try:
            # Validate URL
            if not self._is_valid_url(url):
                logger.error(f"Invalid URL: {url}")
                return None
            
            # Fetch page content
            content = self._fetch_page(url)
            if not content:
                return None
            
            # Parse and extract text
            text = self._extract_text(content)
            if not text:
                return None
            
            # Clean and process text
            cleaned_text = self._clean_extracted_text(text)
            
            logger.info(f"Successfully extracted {len(cleaned_text)} characters from {url}")
            return cleaned_text
            
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")
            return None
    
    def extract_structured_data(self, url: str) -> Dict[str, any]:
        """
        Extract structured data from a URL.
        
        Args:
            url: URL to extract structured data from
            
        Returns:
            Dictionary with extracted structured data
        """
        try:
            content = self._fetch_page(url)
            if not content:
                return {}
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract JSON-LD structured data
            json_ld_data = self._extract_json_ld(soup)
            
            # Extract meta tags
            meta_data = self._extract_meta_tags(soup)
            
            # Extract business information
            business_info = self._extract_business_info(soup)
            
            return {
                'json_ld': json_ld_data,
                'meta': meta_data,
                'business': business_info,
                'url': url
            }
            
        except Exception as e:
            logger.error(f"Error extracting structured data from {url}: {str(e)}")
            return {}
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and accessible."""
        try:
            parsed = urlparse(url)
            return bool(parsed.scheme and parsed.netloc)
        except Exception:
            return False
    
    def _fetch_page(self, url: str) -> Optional[str]:
        """Fetch page content with retries."""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"All attempts failed for {url}")
                    return None
        return None
    
    def _extract_text(self, html_content: str) -> str:
        """Extract main text content from HTML."""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract text from main content areas
            main_content = self._find_main_content(soup)
            if main_content:
                return main_content.get_text(separator=' ', strip=True)
            
            # Fallback to body text
            body = soup.find('body')
            if body:
                return body.get_text(separator=' ', strip=True)
            
            return soup.get_text(separator=' ', strip=True)
            
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            return ""
    
    def _find_main_content(self, soup: BeautifulSoup) -> Optional[BeautifulSoup]:
        """Find the main content area of the page."""
        # Common selectors for main content
        main_selectors = [
            'main',
            '[role="main"]',
            '.main-content',
            '.content',
            '.post-content',
            '.entry-content',
            '.article-content',
            '#main',
            '#content',
            '#primary'
        ]
        
        for selector in main_selectors:
            element = soup.select_one(selector)
            if element:
                return element
        
        # Fallback to article tag
        article = soup.find('article')
        if article:
            return article
        
        return None
    
    def _clean_extracted_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common web artifacts
        text = re.sub(r'Cookie Policy|Privacy Policy|Terms of Service', '', text)
        text = re.sub(r'Skip to content|Skip to navigation', '', text)
        
        # Remove email addresses and phone numbers (optional)
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '', text)
        
        # Limit text length for processing
        if len(text) > 5000:
            text = text[:5000] + "..."
        
        return text.strip()
    
    def _extract_json_ld(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract JSON-LD structured data."""
        json_ld_data = []
        
        try:
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                if script.string:
                    import json
                    try:
                        data = json.loads(script.string)
                        json_ld_data.append(data)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            logger.warning(f"Error extracting JSON-LD: {str(e)}")
        
        return json_ld_data
    
    def _extract_meta_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract meta tags from the page."""
        meta_data = {}
        
        try:
            # Title
            title = soup.find('title')
            if title:
                meta_data['title'] = title.get_text(strip=True)
            
            # Meta description
            description = soup.find('meta', attrs={'name': 'description'})
            if description:
                meta_data['description'] = description.get('content', '')
            
            # Meta keywords
            keywords = soup.find('meta', attrs={'name': 'keywords'})
            if keywords:
                meta_data['keywords'] = keywords.get('content', '')
            
            # Open Graph tags
            og_title = soup.find('meta', property='og:title')
            if og_title:
                meta_data['og_title'] = og_title.get('content', '')
            
            og_description = soup.find('meta', property='og:description')
            if og_description:
                meta_data['og_description'] = og_description.get('content', '')
            
        except Exception as e:
            logger.warning(f"Error extracting meta tags: {str(e)}")
        
        return meta_data
    
    def _extract_business_info(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract business-specific information."""
        business_info = {}
        
        try:
            # Look for business name in various places
            business_name_selectors = [
                'h1',
                '.business-name',
                '.company-name',
                '[itemprop="name"]'
            ]
            
            for selector in business_name_selectors:
                element = soup.select_one(selector)
                if element:
                    business_info['name'] = element.get_text(strip=True)
                    break
            
            # Look for business description
            description_selectors = [
                '.business-description',
                '.company-description',
                '.about-us',
                '[itemprop="description"]'
            ]
            
            for selector in description_selectors:
                element = soup.select_one(selector)
                if element:
                    business_info['description'] = element.get_text(strip=True)
                    break
            
            # Look for services/products
            services_selectors = [
                '.services',
                '.products',
                '.offerings',
                '[itemprop="offers"]'
            ]
            
            for selector in services_selectors:
                element = soup.select_one(selector)
                if element:
                    business_info['services'] = element.get_text(strip=True)
                    break
            
        except Exception as e:
            logger.warning(f"Error extracting business info: {str(e)}")
        
        return business_info
    
    def get_page_summary(self, url: str) -> Dict[str, any]:
        """
        Get a comprehensive summary of the page content.
        
        Args:
            url: URL to analyze
            
        Returns:
            Dictionary with page summary information
        """
        try:
            content = self._fetch_page(url)
            if not content:
                return {}
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract basic information
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else ""
            
            description = soup.find('meta', attrs={'name': 'description'})
            description_text = description.get('content', '') if description else ""
            
            # Extract main content
            main_text = self._extract_text(content)
            
            # Extract structured data
            structured_data = self._extract_structured_data(url)
            
            return {
                'url': url,
                'title': title_text,
                'description': description_text,
                'content': main_text,
                'structured_data': structured_data,
                'content_length': len(main_text),
                'extraction_success': True
            }
            
        except Exception as e:
            logger.error(f"Error getting page summary for {url}: {str(e)}")
            return {
                'url': url,
                'extraction_success': False,
                'error': str(e)
            }









