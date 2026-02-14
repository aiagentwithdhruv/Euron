# Euron - Euri API Toolkit

**Free AI API gateway with 200,000 tokens/day.** Access 24 models from 6 providers (Google, OpenAI, Meta, Groq, Alibaba, Together) through a single OpenAI-compatible endpoint.

> Sign up free at [euron.one/euri](https://euron.one/euri)

## Quick Start

```bash
curl -X POST https://api.euron.one/api/v1/euri/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{
    "messages": [{"role": "user", "content": "Hello!"}],
    "model": "gemini-2.5-flash"
  }'
```

**Python:**
```bash
pip install euriai
```
```python
from euriai import EuriaiClient
client = EuriaiClient(api_key="your-key", model="gemini-2.5-flash")
response = client.generate_completion(prompt="Hello!", temperature=0.7, max_tokens=500)
print(response["choices"][0]["message"]["content"])
```

**OpenAI SDK (drop-in replacement):**
```python
from openai import OpenAI
client = OpenAI(api_key="your-euri-key", base_url="https://api.euron.one/api/v1/euri")
response = client.chat.completions.create(model="gemini-2.5-flash", messages=[{"role": "user", "content": "Hello!"}])
```

## What's in this repo

| File | Description |
|------|-------------|
| `test.html` | Interactive API tester — open in browser, test all 3 endpoints |
| `euri-client.ts` | TypeScript client for Next.js / Node.js projects |
| `euri-models.ts` | All 24 model definitions with types and metadata |
| `examples/basic-chat.ts` | TypeScript usage examples (chat, embeddings, images) |
| `examples/nextjs-api-route.ts` | Drop-in Next.js API route template |
| `examples/n8n-http-request.md` | n8n workflow integration guide |
| `examples/python-sdk.py` | Python examples (SDK + raw HTTP + LangChain) |

## API Reference

**Base URL:** `https://api.euron.one/api/v1/euri`
**Auth:** `Authorization: Bearer <YOUR_API_KEY>`

### Endpoints

#### 1. Chat Completions
```
POST /chat/completions
```

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `messages` | yes | array | `[{role: "user", content: "..."}]` |
| `model` | yes | string | Model ID from table below |
| `max_tokens` | no | integer | Max tokens to generate |
| `temperature` | no | number | 0 = deterministic, 1.0 = creative (default: 0.7) |

> **Note:** Response `content` can be a string OR an array `[{type:"text", text:"..."}]`. Handle both formats.

#### 2. Embeddings
```
POST /embeddings
```

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `input` | yes | string | Text to embed |
| `model` | yes | string | e.g. `text-embedding-3-small` |

#### 3. Image Generation
```
POST /images/generations
```

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `prompt` | yes | string | Text description of image |
| `model` | yes | string | e.g. `gemini-3-pro-image-preview` |
| `n` | no | number | Number of images (default: 4) |

## Available Models (24 models, 6 providers)

### Text Generation (20 models)

| Provider | Model | ID | Context | Speed | Cost |
|----------|-------|----|---------|-------|------|
| Alibaba | Qwen 3 32B | `qwen/qwen3-32b` | 128K | Fast | Medium |
| Google | Gemini 2.0 Flash | `gemini-2.0-flash` | 1M | Very fast | Low |
| Google | Gemini 2.5 Pro | `gemini-2.5-pro` | 2M | Fast | Medium |
| Google | Gemini 2.5 Flash | `gemini-2.5-flash` | 1M | Very fast | Low |
| Google | Gemini 2.5 Pro Preview | `gemini-2.5-pro-preview-06-05` | 2M | Fast | Medium |
| Google | Gemini 2.5 Flash Preview | `gemini-2.5-flash-preview-05-20` | 1M | Very fast | Low |
| Google | Gemini 2.5 Flash Lite | `gemini-2.5-flash-lite-preview-06-17` | 128K | Ultra-fast | Very low |
| Groq | Groq Compound | `groq/compound` | 131K | Fast | Medium |
| Groq | Groq Compound Mini | `groq/compound-mini` | 131K | Fast | Medium |
| Meta | Llama 4 Scout | `llama-4-scout-17b-16e-instruct` | 128K | Fast | Medium |
| Meta | Llama 4 Maverick | `llama-4-maverick-17b-128e-instruct` | 128K | Medium | Medium |
| Meta | Llama 3.3 70B | `llama-3.3-70b-versatile` | 128K | Medium | High |
| Meta | Llama 3.1 8B Instant | `llama-3.1-8b-instant` | 128K | Very fast | Low |
| Meta | Llama Guard 4 12B | `llama-guard-4-12b` | 128K | Fast | Low |
| OpenAI | GPT-5 Nano | `gpt-5-nano-2025-08-07` | 128K | Ultra-fast | Very low |
| OpenAI | GPT-5 Mini | `gpt-5-mini-2025-08-07` | 128K | Fast | Low |
| OpenAI | GPT-4.1 Nano | `gpt-4.1-nano` | 128K | Ultra-fast | Very low |
| OpenAI | GPT-4.1 Mini | `gpt-4.1-mini` | 128K | Fast | Low |
| OpenAI | GPT-OSS 20B | `openai/gpt-oss-20b` | 128K | Fast | Medium |
| OpenAI | GPT-OSS 120B | `openai/gpt-oss-120b` | 128K | Medium | High |

### Embedding Models (3 models)

| Provider | Model | ID | Dimensions |
|----------|-------|----|------------|
| Google | Gemini Embedding 001 | `gemini-embedding-001` | 1536 |
| OpenAI | Text Embedding 3 Small | `text-embedding-3-small` | 1536 |
| Together | M2 BERT 80M 32K | `togethercomputer/m2-bert-80M-32k-retrieval` | 1536 |

### Image Generation (1 model)

| Provider | Model | ID |
|----------|-------|----|
| Google | Gemini 3 Pro Image Preview | `gemini-3-pro-image-preview` |

## Recommended Models

| Use Case | Model | Why |
|----------|-------|-----|
| General purpose | `gemini-2.5-flash` | Best balance of speed + quality |
| Complex reasoning | `gemini-2.5-pro` | 2M context, best reasoning |
| Fast & cheap | `gpt-4.1-nano` or `gpt-5-nano-2025-08-07` | Cheapest tokens |
| Code generation | `gpt-4.1-mini` or `gemini-2.5-flash` | Good at code |
| Web search | `groq/compound` | Built-in web search |
| Embeddings (RAG) | `gemini-embedding-001` | Best quality embeddings |
| Image generation | `gemini-3-pro-image-preview` | Only image model |

## Token Limits

- **Daily limit**: 200,000 tokens (input + output combined)
- **Reset**: Midnight UTC
- **Tip**: Use shorter prompts and lower max_tokens for efficiency

## n8n Integration

Since Euri is OpenAI-compatible, use n8n's built-in OpenAI credential:
1. Create "OpenAI" credential in n8n
2. Set API Key → your Euri API key
3. Set Base URL → `https://api.euron.one/api/v1/euri`
4. Use any OpenAI node — it routes through Euri automatically

See [examples/n8n-http-request.md](examples/n8n-http-request.md) for HTTP Request node configs.

## License

MIT
