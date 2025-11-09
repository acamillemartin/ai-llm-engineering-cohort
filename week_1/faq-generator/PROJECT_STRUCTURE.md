# AI FAQ Generator - Project Structure

## 📁 Complete Project Structure

```
faq-generator/
├── 📄 README.md                           # Main project documentation
├── 📄 PRD.md                             # Product Requirements Document
├── 📄 PROJECT_STRUCTURE.md               # This file - project overview
├── 📄 pyproject.toml                     # Python project configuration
├── 📄 run.py                             # Main entry point script
├── 📄 env.example                        # Environment variables template
├── 📄 .gitignore                         # Git ignore rules
│
├── 📁 src/                               # Source code
│   ├── 📄 __init__.py                    # Package initialization
│   ├── 📄 app.py                         # Main Streamlit application
│   ├── 📄 faq_generator.py              # Core FAQ generation logic
│   ├── 📄 schema_generator.py           # JSON-LD schema generation
│   ├── 📄 validators.py                 # Schema validation utilities
│   └── 📁 utils/                         # Utility modules
│       ├── 📄 __init__.py
│       ├── 📄 text_processing.py       # Text analysis and cleaning
│       └── 📄 url_extractor.py         # URL content extraction
│
├── 📁 tests/                            # Test suite
│   ├── 📄 __init__.py
│   ├── 📄 test_faq_generator.py         # FAQ generator tests
│   ├── 📄 test_schema_generator.py      # Schema generator tests
│   └── 📄 test_validators.py            # Validator tests
│
├── 📁 config/                           # Configuration files
│   └── 📄 prompts.py                    # AI prompt templates
│
├── 📁 data/                             # Data and examples
│   └── 📁 examples/
│       └── 📄 sample_businesses.json    # Sample business data
│
├── 📁 docs/                             # Documentation
│   └── 📄 api.md                        # API documentation
│
└── 📁 logs/                             # Log files (created at runtime)
```

## 🚀 Quick Start Guide

### 1. Installation
```bash
# Clone the repository
git clone <repository-url>
cd faq-generator

# Install dependencies
pip install -e .

# Set up environment
cp env.example .env
# Edit .env with your OpenAI API key
```

### 2. Run the Application

#### Option A: Web Interface (Streamlit)
```bash
python run.py
# or
streamlit run src/app.py
```

#### Option B: Command Line Interface
```bash
python run.py --business-info "We are a dental practice..." --tone friendly --num-faqs 5
```

### 3. Development Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 🏗️ Architecture Overview

### Core Components

1. **FAQ Generator** (`src/faq_generator.py`)
   - OpenAI API integration
   - Prompt engineering for different tones
   - Response parsing and validation
   - Keyword extraction

2. **Schema Generator** (`src/schema_generator.py`)
   - JSON-LD FAQPage schema creation
   - Metadata handling
   - Schema formatting and validation

3. **Validators** (`src/validators.py`)
   - Schema structure validation
   - Google Rich Results Test integration
   - SEO best practices checking

4. **Web Application** (`src/app.py`)
   - Streamlit interface
   - User input handling
   - Results display and export

5. **Utilities** (`src/utils/`)
   - Text processing and cleaning
   - URL content extraction
   - Business information parsing

### Data Flow

```
User Input → Business Info Extraction → FAQ Generation → Schema Creation → Validation → Output
     ↓              ↓                      ↓                ↓              ↓         ↓
  Text/URL → Content Processing → OpenAI API → JSON-LD → Validation → Display/Export
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: Model to use (gpt-4o, gpt-4, gpt-3.5-turbo)
- `MAX_FAQS`: Maximum number of FAQs (3-5)
- `DEFAULT_TONE`: Default tone (friendly, formal, expert)

### Prompt Templates
- Located in `config/prompts.py`
- Tone-specific prompts (friendly, formal, expert)
- Business-type specific prompts (ecommerce, local, service)
- SEO optimization keywords

## 🧪 Testing

### Test Coverage
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Validation Tests**: Schema and content validation

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_faq_generator.py

# Run with coverage
pytest --cov=src --cov-report=html tests/
```

## 📊 Features Implemented

### ✅ Core Features (High Priority)
- [x] Business input field (text and URL)
- [x] FAQ generation (3-5 FAQs)
- [x] JSON-LD schema generation
- [x] Tone selection (friendly, formal, expert)
- [x] Copy/export functionality
- [x] Schema validation

### ✅ Advanced Features (Medium Priority)
- [x] URL content extraction
- [x] Multiple input methods
- [x] Comprehensive validation
- [x] Error handling and logging
- [x] CLI interface

### 🔮 Future Enhancements (Low Priority)
- [ ] Multi-language support
- [ ] CMS integrations
- [ ] Bulk FAQ generation
- [ ] Analytics dashboard
- [ ] RAG-based contextual generation

## 🚀 Deployment Options

### Local Development
```bash
python run.py
```

### Production Deployment
```bash
# Using Docker
docker build -t faq-generator .
docker run -p 8501:8501 faq-generator

# Using cloud platforms
# Deploy to Streamlit Cloud, Heroku, or AWS
```

### API Integration
```python
from src.faq_generator import FAQGenerator
from src.schema_generator import SchemaGenerator

# Initialize components
generator = FAQGenerator(api_key="your-key")
schema_gen = SchemaGenerator()

# Generate FAQs
faqs = generator.generate_faqs("We are a dental practice...")
schema = schema_gen.generate_schema(faqs)
```

## 📈 Performance Metrics

- **FAQ Generation Time**: < 30 seconds
- **Schema Validation Success**: > 95%
- **API Response Time**: 2-5 seconds
- **Memory Usage**: < 100MB
- **Concurrent Users**: 10+ (depending on OpenAI rate limits)

## 🔒 Security Considerations

- API key protection
- Input validation and sanitization
- Rate limiting
- Error handling without exposing sensitive data
- Secure environment variable handling

## 📝 Documentation

- **README.md**: Main project documentation
- **API.md**: API reference and examples
- **PRD.md**: Product requirements document
- **Inline Documentation**: Comprehensive docstrings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

- **Documentation**: Check the docs/ folder
- **Issues**: Create GitHub issues for bugs
- **Questions**: Contact the development team

---

**Built with ❤️ for SEO professionals and business owners**









