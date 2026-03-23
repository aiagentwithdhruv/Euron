# Skill: student-support

> Answer Euron student doubts about Euri API, SDKs, models, and common errors. Uses pre-built reply templates.

## When to Use
- A student has a doubt about Euri API
- Someone gets an API key error
- Someone is confused about OpenAI vs Euri
- Need to reply to community questions (Discord, Skool, email)
- Dhruv needs a quick reply template for student messages

## Context

### What is Euri
- Unified AI gateway on the Euron platform
- OpenAI-compatible access, RESTful API, JSON responses, real-time streaming, agentic tooling
- Python SDK: `euriai` on PyPI
- Portal: https://euron.one/euri

### Common Student Confusions
1. **Using OpenAI key with Euri** → "incorrect API key" or "authorization failed"
2. **Using OpenAI model names** → Need Euri dashboard model IDs
3. **Not setting base URL** → Requests go to OpenAI instead of Euri
4. **Response format surprise** → `content` can be string OR array

## Reply Templates

### 1. OpenAI Key Error
> If your code asks for an OpenAI key, you are probably using the OpenAI client defaults.
> For Euri:
> 1) Use **Euri API key** (not OpenAI key)
> 2) Set **base URL** to `https://api.euron.one/api/v1/euri`
> 3) Use **model IDs from Euri dashboard**
> If it still says "incorrect key", re-check key status, copy/paste without spaces, and project access.

### 2. Which SDK?
> - Fastest: use the `euriai` Python SDK / CLI from PyPI (`pip install euriai`)
> - If your codebase already uses OpenAI SDK, just change base URL + model IDs

### 3. One-Line Reply (Short)
> Use Euri key + Euri model ID, and point your OpenAI client to `https://api.euron.one/api/v1/euri` as base URL.

### 4. Model Not Found
> Check the model ID matches exactly what's in the Euri dashboard. Common models:
> - `gemini-2.5-flash` (general purpose)
> - `gemini-2.5-pro` (reasoning)
> - `gpt-4.1-nano` (fast/cheap)
> Model IDs are case-sensitive and include provider prefix for some (e.g., `groq/compound`).

### 5. Rate Limit / Token Exhaustion
> The free tier gives 200K tokens/day (input + output combined). Resets at midnight UTC.
> Tips: Use shorter prompts, lower max_tokens, and pick cheaper models (`gpt-4.1-nano`).

## Recipe: Answer a Student Doubt

1. **Identify the issue** — read the student's message
2. **Match to a template** above (1-5)
3. **Customize** with their specific error/code if provided
4. **Add code example** if they shared code (fix the base_url, api_key, model)
5. **Keep it friendly** — these are learners

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| student_message | string | yes | The student's question/doubt |
| platform | string | no | Where the doubt came from (Discord, email, Skool) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| reply | string | Ready-to-send reply |
| template_used | string | Which template was matched |

## Files
| File | Purpose |
|------|---------|
| `../../Students-Doubts-Answers/CONTEXT.md` | Full Euri context for answering |
| `../../Students-Doubts-Answers/REPLIES.md` | Reply templates |

## Self-Update Rules
| Event | Update |
|-------|--------|
| New common doubt pattern | Add template to REPLIES.md + this file |
| API change affects students | Update CONTEXT.md |
| New platform for support | Add platform-specific formatting |
