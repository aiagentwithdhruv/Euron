# Skill: euri-api

> Use the Euri API gateway to call 39 AI models from 7 providers (24 free + 15 premium). OpenAI-compatible, 100K free tokens/day.

## When to Use
- User needs to call an AI model via Euri
- User wants to integrate Euri into a project (Node.js, Python, n8n)
- User asks about Euri models, pricing, or endpoints
- Any project needing AI API calls where Euri is available

## Quick Reference

**Base URL:** `https://api.euron.one/api/v1/euri`
**Auth:** `Authorization: Bearer <EURI_API_KEY>`
**Daily limit:** 100,000 tokens (resets midnight UTC)

### Endpoints
| Endpoint | Purpose | Models |
|----------|---------|--------|
| `POST /chat/completions` | Text generation | 33 models (20 free + 13 premium) |
| `POST /embeddings` | Vector embeddings | 3 models |
| `POST /images/generations` | Image generation | 1 model |
| `POST /audio/transcriptions` | Speech to text | 2 models (premium) |

### Model Picker
| Need | Use This Model | Why |
|------|---------------|-----|
| General purpose | `gemini-2.5-flash` | Best speed + quality |
| Complex reasoning | `gemini-2.5-pro` | 2M context, best reasoning |
| Fast & cheap | `gpt-4.1-nano` | Cheapest tokens |
| Code generation | `gpt-4.1-mini` | Good at code |
| Web search | `groq/compound` | Built-in web search |
| Embeddings (RAG) | `gemini-embedding-001` | Best quality |
| Image generation | `gemini-3-pro-image-preview` | Only image model |

## Recipes

### Python (euriai SDK)
```python
from euriai import EuriaiClient
client = EuriaiClient(api_key="your-key", model="gemini-2.5-flash")
response = client.generate_completion(prompt="Hello!", temperature=0.7, max_tokens=500)
print(response["choices"][0]["message"]["content"])
```

### Python (OpenAI SDK drop-in)
```python
from openai import OpenAI
client = OpenAI(api_key="your-euri-key", base_url="https://api.euron.one/api/v1/euri")
response = client.chat.completions.create(model="gemini-2.5-flash", messages=[{"role": "user", "content": "Hello!"}])
```

### TypeScript/Node.js
```typescript
// Use euri-client.ts from Euron/euri-client.ts
import { euriChat } from './euri-client';
const reply = await euriChat("Hello!", "gemini-2.5-flash");
```

### cURL
```bash
curl -X POST https://api.euron.one/api/v1/euri/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"messages": [{"role": "user", "content": "Hello!"}], "model": "gemini-2.5-flash"}'
```

### n8n Integration
1. Create "OpenAI" credential → API Key = Euri key
2. Set Base URL = `https://api.euron.one/api/v1/euri`
3. All OpenAI nodes now route through Euri automatically

## Common Pitfalls
- **Wrong API key:** Students use OpenAI key instead of Euri key → "incorrect API key" error
- **Wrong base URL:** Must point to `https://api.euron.one/api/v1/euri`, not OpenAI
- **Wrong model ID:** Use IDs from Euri dashboard, not OpenAI model names
- **Response format:** `content` can be a string OR array `[{type:"text", text:"..."}]` — handle both

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| api_key | string | yes | Euri API key from portal |
| model | string | yes | Model ID from Euri dashboard |
| messages | array | yes | Chat messages array |
| max_tokens | integer | no | Max tokens to generate |
| temperature | number | no | 0-1.0 (default 0.7) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| choices | array | Response choices with message content |
| usage | object | Token usage (prompt + completion) |

### Credentials
| Name | Source | Description |
|------|--------|-------------|
| EURI_API_KEY | https://euron.one/euri | Free API key, 100K tokens/day |

### Cost
- Free tier: 100,000 tokens/day (24 models)
- Premium tier: Paid (15 models — Claude, GPT-5, o3, Gemini 3.1, Whisper)
- No credit card required for free tier

### Providers (7)
| Provider | Free | Premium |
|----------|------|---------|
| Alibaba | 1 (Qwen 3 32B) | — |
| Anthropic | — | 4 (Claude Sonnet/Opus 4 & 4.6) |
| Google | 8 (Gemini 2.0-3 Pro + embedding + image) | 2 (Gemini 3 Flash, 3.1 Pro) |
| Groq | 2 (Compound, Compound Mini) | — |
| Meta | 4 (Llama 4 Scout, 3.3 70B, 3.1 8B, Guard 4) | — |
| OpenAI | 7 (GPT-5 Nano/Mini dated, 4.1 Nano/Mini, OSS 20B/120B, embed) | 9 (GPT-4.1/5/5.1, o3, o4-mini, Whisper) |
| Together | 1 (M2 BERT embedding) | — |

## Files
| File | Purpose |
|------|---------|
| `../../euri-client.ts` | TypeScript client |
| `../../euri-models.ts` | All 39 model definitions with pricing |
| `../../euri-tester/` | Interactive browser tester (4 tabs) |
| `../../model-arena/` | Multi-provider comparison arena |
| `../../examples/` | Usage examples |
| `../../README.md` | Full API reference |
