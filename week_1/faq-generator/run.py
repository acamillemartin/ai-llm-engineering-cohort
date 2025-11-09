#!/usr/bin/env python3
"""
Main entry point for the AI FAQ Generator application.

This script provides a command-line interface for running the FAQ generator
and can be used for both development and production deployments.
"""

import os
import sys
import argparse
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.app import main as streamlit_main
from src.faq_generator import FAQGenerator
from src.schema_generator import SchemaGenerator
from src.validators import SchemaValidator


def run_streamlit():
    """Run the Streamlit web application."""
    print("🚀 Starting AI FAQ Generator web application...")
    print("📱 Open your browser and navigate to the URL shown below")
    print("🔧 Press Ctrl+C to stop the application")
    print("-" * 50)
    
    # Set Streamlit configuration
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_SERVER_PORT"] = "8501"
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    
    try:
        streamlit_main()
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)


def run_cli():
    """Run the command-line interface."""
    parser = argparse.ArgumentParser(description="AI FAQ Generator CLI")
    parser.add_argument("--business-info", required=True, help="Business information for FAQ generation")
    parser.add_argument("--tone", choices=["friendly", "formal", "expert"], default="friendly", help="Tone for FAQs")
    parser.add_argument("--num-faqs", type=int, default=5, help="Number of FAQs to generate (3-5)")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model to use")
    parser.add_argument("--output", help="Output file for results")
    parser.add_argument("--format", choices=["json", "html", "markdown"], default="json", help="Output format")
    parser.add_argument("--validate", action="store_true", help="Validate generated schema")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OpenAI API key is required")
        print("   Set OPENAI_API_KEY environment variable or use --api-key")
        sys.exit(1)
    
    try:
        print("🤖 Generating FAQs...")
        
        # Initialize components
        faq_generator = FAQGenerator(api_key=api_key, model=args.model)
        schema_generator = SchemaGenerator()
        validator = SchemaValidator()
        
        # Generate FAQs
        faqs = faq_generator.generate_faqs(
            business_info=args.business_info,
            tone=args.tone,
            num_faqs=args.num_faqs,
            model=args.model
        )
        
        print(f"✅ Generated {len(faqs)} FAQs")
        
        # Generate schema
        schema = schema_generator.generate_schema(faqs)
        print("✅ Generated JSON-LD schema")
        
        # Validate if requested
        if args.validate:
            print("🔍 Validating schema...")
            validation_results = validator.validate_schema(schema)
            if validation_results["valid"]:
                print("✅ Schema is valid")
            else:
                print("❌ Schema validation failed:")
                for issue in validation_results["issues"]:
                    print(f"   - {issue}")
        
        # Format output
        if args.format == "json":
            output = {
                "faqs": faqs,
                "schema": schema,
                "validation": validator.validate_schema(schema) if args.validate else None
            }
            content = str(output)
        elif args.format == "html":
            content = generate_html_output(faqs, schema)
        elif args.format == "markdown":
            content = generate_markdown_output(faqs, schema)
        
        # Save or display output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"💾 Results saved to {args.output}")
        else:
            print("\n" + "="*50)
            print("RESULTS")
            print("="*50)
            print(content)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def generate_html_output(faqs, schema):
    """Generate HTML output for FAQs and schema."""
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Generated FAQs</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .faq {{ margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .question {{ font-weight: bold; color: #333; margin-bottom: 10px; }}
        .answer {{ color: #666; line-height: 1.5; }}
        .schema {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin-top: 20px; }}
        pre {{ white-space: pre-wrap; word-wrap: break-word; }}
    </style>
</head>
<body>
    <h1>Generated FAQs</h1>
"""
    
    for i, faq in enumerate(faqs, 1):
        html += f"""
    <div class="faq">
        <div class="question">Q{i}: {faq['question']}</div>
        <div class="answer">{faq['answer']}</div>
    </div>
"""
    
    html += f"""
    <div class="schema">
        <h2>JSON-LD Schema</h2>
        <pre>{schema}</pre>
    </div>
</body>
</html>
"""
    return html


def generate_markdown_output(faqs, schema):
    """Generate Markdown output for FAQs and schema."""
    markdown = "# Generated FAQs\n\n"
    
    for i, faq in enumerate(faqs, 1):
        markdown += f"## Q{i}: {faq['question']}\n\n"
        markdown += f"{faq['answer']}\n\n"
    
    markdown += "## JSON-LD Schema\n\n"
    markdown += "```json\n"
    markdown += str(schema)
    markdown += "\n```\n"
    
    return markdown


def main():
    """Main entry point."""
    if len(sys.argv) == 1:
        # No arguments, run Streamlit
        run_streamlit()
    else:
        # Arguments provided, run CLI
        run_cli()


if __name__ == "__main__":
    main()









