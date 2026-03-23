# Skill: euri-api

> Use the Euri API gateway to call 50 AI models from 8 providers (27 free + 23 premium). OpenAI-compatible, 100K free tokens/day.

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
| `POST /chat/completions` | Text generation | 41 models (21 free + 20 premium) |
| `POST /embeddings` | Vector embeddings | 4 models |
| `POST /images/generations` | Image generation | 1 model |
| `POST /audio/transcriptions` | Speech to text | 3 models (1 free + 2 premium) |
| `POST /audio/speech` | Text to speech | 1 model (premium) |

### Model Picker
| Need | Use This Model | Why |
|------|---------------|-----|
| General purpose | `gemini-2.5-flash` | Best speed + quality |
| Complex reasoning | `gemini-2.5-pro` | 2M context, best reasoning |
| Fast & cheap | `gpt-4.1-nano` | Cheapest tokens |
| Code generation | `gpt-4.1-mini` | Good at code |
| Frontier code | `claude-sonnet-4-5` | 77.2% SWE-bench |
| Autonomous agents | `claude-opus-4-5` | 80.9% SWE-bench, long-horizon |
| Fast Claude | `claude-haiku-4-5` | Sonnet 4 quality at Haiku price |
| Web search | `groq/compound` | Built-in web search |
| Indian languages | `sarvam-m` | 11 Indian languages, 24B params |
| Frontier OpenAI | `gpt-5.4` | Best reasoning across STEM |
| Conversational | `gpt-5.3-instant` | 26.8% fewer hallucinations |
| Embeddings (RAG) | `gemini-embedding-001` | Best quality |
| Multimodal embed | `gemini-embedding-2-preview` | Text+image+video+audio+PDF |
| Image generation | `gemini-3-pro-image-preview` | Only image model |
| High throughput | `gemini-3.1-flash-lite` | Fastest, cheapest Google |

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
- Free tier: 100,000 tokens/day (27 models)
- Premium tier: Paid (23 models — Claude, GPT-5.x, o3, o4-mini, Gemini 3.x, Whisper)
- No credit card required for free tier

### Providers (8)
| Provider | Free | Premium |
|----------|------|---------|
| Alibaba | 1 (Qwen 3 32B) | — |
| Anthropic | — | 7 (Claude Sonnet/Opus 4, 4.5, 4.6 + Haiku 4.5) |
| Google | 8 (Gemini 2.0-3 Pro + embeddings + image) | 3 (Gemini 3 Flash, 3.1 Pro, 3.1 Flash-Lite) |
| Groq | 2 (Compound, Compound Mini) | — |
| Meta | 4 (Llama 4 Scout, 3.3 70B, 3.1 8B, Guard 4) | — |
| OpenAI | 7 (GPT-5 Nano/Mini dated, 4.1 Nano/Mini, OSS 20B/120B, embed) | 12 (GPT-4.1/5/5.1/5.2/5.3/5.4, o3, o4-mini, Whisper x2) |
| Sarvam | 1 (Sarvam M) + 1 STT | 1 TTS (Bulbul v3) |
| Together | 1 (M2 BERT embedding) | — |

## Files
| File | Purpose |
|------|---------|
| `../../euri-client.ts` | TypeScript client |
| `../../euri-models.ts` | All 50 model definitions with pricing |
| `../../euri-tester/` | Interactive browser tester (4 tabs) |
| `../../model-arena/` | Multi-provider comparison arena |
| `../../examples/` | Usage examples |
| `../../README.md` | Full API reference |
