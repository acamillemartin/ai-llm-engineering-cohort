# AI FAQ Generator API Documentation

## Overview

The AI FAQ Generator provides a comprehensive API for generating SEO-optimized FAQs and JSON-LD schema markup. This documentation covers all available endpoints, parameters, and response formats.

## Base URL

```
https://api.faq-generator.com/v1
```

## Authentication

All API requests require authentication using an API key. Include your API key in the request header:

```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### 1. Generate FAQs

Generate FAQs based on business information.

**Endpoint:** `POST /faqs/generate`

**Request Body:**
```json
{
  "business_info": "We are a local dental practice specializing in cosmetic dentistry and orthodontics.",
  "tone": "friendly",
  "num_faqs": 5,
  "model": "gpt-4o",
  "business_type": "dental",
  "metadata": {
    "title": "Dental Practice FAQs",
    "description": "Frequently asked questions about our dental services",
    "url": "https://example.com/faqs"
  }
}
```

**Parameters:**
- `business_info` (string, required): Description of the business, products, or services
- `tone` (string, optional): Tone for FAQs ("friendly", "formal", "expert"). Default: "friendly"
- `num_faqs` (integer, optional): Number of FAQs to generate (3-5). Default: 5
- `model` (string, optional): OpenAI model to use. Default: "gpt-4o"
- `business_type` (string, optional): Type of business for specialized prompts
- `metadata` (object, optional): Additional metadata for schema generation

**Response:**
```json
{
  "success": true,
  "faqs": [
    {
      "question": "What services do you offer?",
      "answer": "We provide comprehensive dental care including cleanings, fillings, crowns, and cosmetic procedures.",
      "category": "Services",
      "keywords": ["dental", "services", "care"]
    }
  ],
  "schema": {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [...]
  },
  "validation": {
    "valid": true,
    "issues": [],
    "warnings": [],
    "suggestions": []
  },
  "usage": {
    "tokens_used": 1250,
    "cost": 0.025
  }
}
```

### 2. Generate Schema

Generate JSON-LD schema from existing FAQs.

**Endpoint:** `POST /schema/generate`

**Request Body:**
```json
{
  "faqs": [
    {
      "question": "What services do you offer?",
      "answer": "We provide comprehensive dental care.",
      "category": "Services"
    }
  ],
  "metadata": {
    "title": "Dental Practice FAQs",
    "description": "Frequently asked questions about our dental services",
    "url": "https://example.com/faqs"
  }
}
```

**Response:**
```json
{
  "success": true,
  "schema": {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [...]
  },
  "validation": {
    "valid": true,
    "issues": [],
    "warnings": [],
    "suggestions": []
  }
}
```

### 3. Validate Schema

Validate JSON-LD schema markup.

**Endpoint:** `POST /schema/validate`

**Request Body:**
```json
{
  "schema": {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [...]
  }
}
```

**Response:**
```json
{
  "success": true,
  "validation": {
    "valid": true,
    "issues": [],
    "warnings": [],
    "suggestions": [],
    "google_validation": {
      "valid": true,
      "rich_results": true,
      "issues": []
    }
  }
}
```

### 4. Extract Content from URL

Extract business information from a website URL.

**Endpoint:** `POST /content/extract`

**Request Body:**
```json
{
  "url": "https://example.com",
  "extract_structured_data": true
}
```

**Response:**
```json
{
  "success": true,
  "content": "Extracted text content from the website...",
  "structured_data": {
    "json_ld": [...],
    "meta": {...},
    "business": {...}
  },
  "summary": {
    "title": "Website Title",
    "description": "Website description",
    "content_length": 1500
  }
}
```

### 5. Get Business Examples

Retrieve sample business data for testing.

**Endpoint:** `GET /examples/businesses`

**Query Parameters:**
- `type` (string, optional): Filter by business type
- `limit` (integer, optional): Number of examples to return (default: 10)

**Response:**
```json
{
  "success": true,
  "businesses": [
    {
      "name": "Smile Bright Dental",
      "type": "dental",
      "description": "We are a family dental practice...",
      "services": ["General Dentistry", "Cosmetic Dentistry"],
      "location": "Downtown Medical District"
    }
  ]
}
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": {
      "field": "business_info",
      "issue": "Cannot be empty"
    }
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| `VALIDATION_ERROR` | Invalid input parameters |
| `API_KEY_INVALID` | Invalid or missing API key |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `OPENAI_ERROR` | OpenAI API error |
| `SCHEMA_ERROR` | Schema validation error |
| `CONTENT_EXTRACTION_ERROR` | URL content extraction failed |
| `INTERNAL_ERROR` | Internal server error |

## Rate Limits

- **Free Tier:** 100 requests per day
- **Pro Tier:** 1,000 requests per day
- **Enterprise:** Custom limits

## Response Times

- **FAQ Generation:** 2-5 seconds
- **Schema Generation:** < 1 second
- **Content Extraction:** 3-10 seconds
- **Validation:** < 1 second

## SDKs and Libraries

### Python
```python
from faq_generator import FAQGenerator

generator = FAQGenerator(api_key="your-api-key")
faqs = generator.generate_faqs(
    business_info="We are a dental practice...",
    tone="friendly",
    num_faqs=5
)
```

### JavaScript
```javascript
const FAQGenerator = require('faq-generator');

const generator = new FAQGenerator('your-api-key');
const faqs = await generator.generateFAQs({
  businessInfo: 'We are a dental practice...',
  tone: 'friendly',
  numFaqs: 5
});
```

### cURL Examples

**Generate FAQs:**
```bash
curl -X POST https://api.faq-generator.com/v1/faqs/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "business_info": "We are a dental practice...",
    "tone": "friendly",
    "num_faqs": 5
  }'
```

**Validate Schema:**
```bash
curl -X POST https://api.faq-generator.com/v1/schema/validate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "schema": {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [...]
    }
  }'
```

## Webhooks

Configure webhooks to receive notifications about completed tasks:

```json
{
  "url": "https://your-domain.com/webhook",
  "events": ["faq_generated", "schema_validated"],
  "secret": "your-webhook-secret"
}
```

## Support

For API support and questions:
- **Email:** api-support@faq-generator.com
- **Documentation:** https://docs.faq-generator.com
- **Status Page:** https://status.faq-generator.com









