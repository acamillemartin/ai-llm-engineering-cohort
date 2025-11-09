"""
Main Streamlit application for AI FAQ Generator.

This module contains the Streamlit interface for the FAQ generator,
including input handling, FAQ generation, schema creation, and validation.
"""

import os
import json
import streamlit as st
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

from .faq_generator import FAQGenerator
from .schema_generator import SchemaGenerator
from .validators import SchemaValidator
from .utils.text_processing import clean_text, extract_keywords
from .utils.url_extractor import URLContentExtractor

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI FAQ Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "faqs" not in st.session_state:
    st.session_state.faqs = []
if "schema" not in st.session_state:
    st.session_state.schema = {}
if "validation_results" not in st.session_state:
    st.session_state.validation_results = {}


def initialize_components() -> Tuple[FAQGenerator, SchemaGenerator, SchemaValidator]:
    """Initialize the core components with API keys."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your environment.")
        st.stop()
    
    return (
        FAQGenerator(api_key=api_key),
        SchemaGenerator(),
        SchemaValidator()
    )


def render_sidebar() -> Dict[str, str]:
    """Render the sidebar with configuration options."""
    st.sidebar.header("⚙️ Configuration")
    
    # Tone selection
    tone = st.sidebar.selectbox(
        "Select Tone",
        ["friendly", "formal", "expert"],
        index=0,
        help="Choose the tone for generated FAQs"
    )
    
    # Number of FAQs
    num_faqs = st.sidebar.slider(
        "Number of FAQs",
        min_value=3,
        max_value=5,
        value=5,
        help="Number of FAQs to generate"
    )
    
    # Model selection
    model = st.sidebar.selectbox(
        "AI Model",
        ["gpt-4o", "gpt-4", "gpt-3.5-turbo"],
        index=0,
        help="Choose the OpenAI model for generation"
    )
    
    return {
        "tone": tone,
        "num_faqs": str(num_faqs),
        "model": model
    }


def render_input_section() -> Tuple[str, str, bool]:
    """Render the input section for business information."""
    st.header("📝 Input Business Information")
    
    # Input method selection
    input_method = st.radio(
        "Choose input method:",
        ["Business Description", "Website URL"],
        horizontal=True
    )
    
    business_input = ""
    is_url = False
    
    if input_method == "Business Description":
        business_input = st.text_area(
            "Describe your business, products, or services:",
            placeholder="e.g., We are a local dental practice specializing in cosmetic dentistry and orthodontics...",
            height=100,
            help="Provide a detailed description of your business to generate relevant FAQs"
        )
    else:
        business_input = st.text_input(
            "Enter your website URL:",
            placeholder="https://example.com",
            help="We'll extract business information from your website"
        )
        is_url = True
    
    return business_input, input_method, is_url


def extract_business_info(business_input: str, is_url: bool) -> str:
    """Extract business information from input or URL."""
    if is_url and business_input:
        try:
            extractor = URLContentExtractor()
            content = extractor.extract_content(business_input)
            if content:
                st.success("✅ Successfully extracted content from URL")
                return content
            else:
                st.warning("⚠️ Could not extract content from URL. Please try a different URL or use business description.")
                return ""
        except Exception as e:
            st.error(f"❌ Error extracting content: {str(e)}")
            return ""
    
    return business_input


def generate_faqs(faq_generator: FAQGenerator, business_info: str, config: Dict[str, str]) -> List[Dict[str, str]]:
    """Generate FAQs using the FAQ generator."""
    try:
        with st.spinner("🤖 Generating FAQs..."):
            faqs = faq_generator.generate_faqs(
                business_info=business_info,
                tone=config["tone"],
                num_faqs=int(config["num_faqs"]),
                model=config["model"]
            )
        return faqs
    except Exception as e:
        st.error(f"❌ Error generating FAQs: {str(e)}")
        return []


def display_faqs(faqs: List[Dict[str, str]]) -> None:
    """Display generated FAQs in an organized format."""
    if not faqs:
        return
    
    st.header("❓ Generated FAQs")
    
    for i, faq in enumerate(faqs, 1):
        with st.expander(f"FAQ {i}: {faq['question']}", expanded=True):
            st.write(f"**Answer:** {faq['answer']}")
            
            # Feedback buttons
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("👍", key=f"helpful_{i}"):
                    st.success("Thank you for your feedback!")
            with col2:
                if st.button("👎", key=f"not_helpful_{i}"):
                    st.info("We'll use your feedback to improve future generations.")


def display_schema(schema: Dict) -> None:
    """Display the generated JSON-LD schema."""
    if not schema:
        return
    
    st.header("📋 JSON-LD Schema")
    
    # Pretty print the JSON
    schema_json = json.dumps(schema, indent=2)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.code(schema_json, language="json")
    
    with col2:
        if st.button("📋 Copy Schema"):
            st.code(schema_json)
            st.success("Schema copied to clipboard!")
        
        if st.button("💾 Download Schema"):
            st.download_button(
                label="Download JSON-LD",
                data=schema_json,
                file_name="faq-schema.json",
                mime="application/json"
            )


def validate_schema(validator: SchemaValidator, schema: Dict) -> None:
    """Validate the generated schema."""
    if not schema:
        return
    
    st.header("✅ Schema Validation")
    
    if st.button("🔍 Validate Schema"):
        with st.spinner("Validating schema..."):
            try:
                validation_result = validator.validate_schema(schema)
                st.session_state.validation_results = validation_result
                
                if validation_result.get("valid", False):
                    st.success("✅ Schema is valid and ready for use!")
                else:
                    st.error("❌ Schema validation failed")
                    st.write("**Issues found:**")
                    for issue in validation_result.get("issues", []):
                        st.error(f"- {issue}")
                        
            except Exception as e:
                st.error(f"❌ Validation error: {str(e)}")


def main():
    """Main application function."""
    # Header
    st.title("🧠 AI FAQ Generator")
    st.markdown("Generate SEO-optimized FAQs with JSON-LD schema markup for your business")
    
    # Initialize components
    try:
        faq_generator, schema_generator, validator = initialize_components()
    except Exception as e:
        st.error(f"Failed to initialize components: {str(e)}")
        return
    
    # Sidebar configuration
    config = render_sidebar()
    
    # Main content
    business_input, input_method, is_url = render_input_section()
    
    if business_input:
        # Extract business information
        business_info = extract_business_info(business_input, is_url)
        
        if business_info:
            # Generate FAQs
            if st.button("🚀 Generate FAQs", type="primary"):
                faqs = generate_faqs(faq_generator, business_info, config)
                
                if faqs:
                    st.session_state.faqs = faqs
                    
                    # Generate schema
                    schema = schema_generator.generate_schema(faqs)
                    st.session_state.schema = schema
                    
                    # Display results
                    display_faqs(faqs)
                    display_schema(schema)
                    validate_schema(validator, schema)
    
    # Display previous results if available
    if st.session_state.faqs:
        st.divider()
        st.subheader("📊 Previous Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Generate New FAQs"):
                st.session_state.faqs = []
                st.session_state.schema = {}
                st.session_state.validation_results = {}
                st.rerun()
        
        with col2:
            if st.button("📊 View Analytics"):
                st.info("Analytics feature coming soon!")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ for SEO professionals and business owners</p>
        <p>Powered by OpenAI GPT models</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

