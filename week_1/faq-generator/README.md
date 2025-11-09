# AI FAQ Generator

An intelligent web-based tool that automatically generates semantically relevant FAQs and JSON-LD schema markup for SEO optimization.

## 🚀 Features

- **Smart FAQ Generation**: Creates 3-5 contextually relevant FAQs using AI
- **JSON-LD Schema Output**: Automatically generates valid FAQPage structured data
- **Multiple Input Types**: Supports business descriptions or URLs
- **Tone Customization**: Choose between formal, friendly, or expert tones
- **Schema Validation**: Built-in validation using Google Rich Results Test
- **Easy Export**: Copy or download FAQs and schema markup

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd faq-generator
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

4. Run the application:
```bash
streamlit run src/app.py
```

## 📁 Project Structure

```
faq-generator/
├── src/
│   ├── app.py                 # Main Streamlit application
│   ├── faq_generator.py      # Core FAQ generation logic
│   ├── schema_generator.py   # JSON-LD schema generation
│   ├── validators.py         # Schema validation utilities
│   └── utils/
│       ├── __init__.py
│       ├── text_processing.py
│       └── url_extractor.py
├── tests/
│   ├── __init__.py
│   ├── test_faq_generator.py
│   ├── test_schema_generator.py
│   └── test_validators.py
├── config/
│   └── prompts.py            # AI prompt templates
├── data/
│   └── examples/             # Sample data for testing
├── docs/
│   └── api.md               # API documentation
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
MAX_FAQS=5
DEFAULT_TONE=friendly
```

### API Configuration

The application uses OpenAI's GPT models for FAQ generation. Configure your preferred model in the environment variables.

## 📖 Usage

### Basic Usage

1. **Input**: Enter your business type and description
2. **Generate**: Click "Generate FAQs" to create relevant questions
3. **Review**: Check the generated FAQs and JSON-LD schema
4. **Export**: Copy or download the results

### Advanced Features

- **URL Input**: Paste a URL to extract business information automatically
- **Tone Selection**: Choose the appropriate tone for your audience
- **Schema Validation**: Validate generated schema before use

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

## 📊 Performance Metrics

- FAQ generation time: < 30 seconds
- Schema validation success rate: > 95%
- User satisfaction tracking
- API usage monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please open an issue in the GitHub repository or contact the development team.

## 🔮 Future Enhancements

- Multi-language support
- CMS integrations (WordPress, Shopify)
- Bulk FAQ generation
- Analytics dashboard
- RAG-based contextual generation

