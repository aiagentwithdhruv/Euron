---
name: euron-euri-api
version: 1.0.0
description: AI testing toolkit + Euri API gateway — 24 models, 6 providers, free 200K tokens/day
author: AiwithDhruv
license: MIT
tier: free
last_verified: 2026-02-23
refresh_cadence: monthly
dependencies: []
platforms: [claude-code, cursor]
---

# Euron (Euri API) — Agent Loadout

> AI testing toolkit and free API gateway. OpenAI-compatible format, 24 models across 6 providers, 200K free tokens/day. Works as drop-in replacement for any OpenAI SDK.

---

## What's Included

| File | Type | Purpose |
|------|------|---------|
| `README.md` | Context | Full API reference, all 24 models, endpoints, examples |
| `HOW-WE-BUILT-THIS.md` | Knowledge | Architecture decisions, build story |
| `MAIL-MCP-SETUP.md` | Runbook | MCP integration setup |
| `euri-client.ts` | Skill | TypeScript client for Next.js/Node.js |
| `euri-models.ts` | Skill | All 24 model definitions with metadata |
| `examples/` | Skill | Usage examples (TypeScript, Python, n8n, Next.js) |
| `model-arena/` | Tool | Compare 50+ models side-by-side (HTML) |
| `euri-tester/` | Tool | Test Euri API in browser (HTML) |

---

## Quick Reference

**Base URL:** `https://api.euron.one/api/v1/euri`
**Auth:** `Authorization: Bearer <EURI_API_KEY>`
**Daily limit:** 200,000 tokens (input+output, resets midnight UTC)
**Portal:** https://euron.one/euri

### Endpoints
- `POST /chat/completions` — Text generation (20 models)
- `POST /embeddings` — Vector embeddings (3 models)
- `POST /images/generations` — Image generation (1 model)

### Best Defaults
| Use Case | Model |
|----------|-------|
| General | `gemini-2.5-flash` |
| Smart/reasoning | `gemini-2.5-pro` |
| Fast/cheap | `gpt-4.1-nano` or `gpt-5-nano-2025-08-07` |
| Embeddings | `gemini-embedding-001` |
| Images | `gemini-3-pro-image-preview` |
| Web search | `groq/compound` |

### n8n Integration Trick
Use n8n's built-in OpenAI credential with Euri base URL — works with all OpenAI nodes:
1. Create "OpenAI" credential → API Key = Euri key
2. Set Base URL = `https://api.euron.one/api/v1/euri`
3. All OpenAI nodes now route through Euri

---

## Self-Update Rules

| Event | Update | File |
|-------|--------|------|
| New model added to Euri | Add to models table | `README.md` + `euri-models.ts` |
| Model deprecated | Mark as deprecated | `README.md` |
| Token limit changed | Update limit | `README.md` + this file |
| New endpoint added | Add to endpoints | `README.md` |
| Python SDK updated | Update examples | `examples/` |

---

## Changelog

### v1.0.0 (2026-02-23)
- Initial loadout with full API reference
- 24 models across 6 providers documented
- TypeScript + Python clients included
