"""
AI FAQ Generator Package

A comprehensive tool for generating SEO-optimized FAQs with JSON-LD schema markup.
"""

__version__ = "0.1.0"
__author__ = "Camille Martin"
__email__ = "camille@example.com"

from .faq_generator import FAQGenerator
from .schema_generator import SchemaGenerator
from .validators import SchemaValidator

__all__ = ["FAQGenerator", "SchemaGenerator", "SchemaValidator"]

