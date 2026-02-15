# AI Model Arena

**Universal AI model comparison tool.** Test any model from any provider side-by-side. Compare speed, quality, and cost across 50+ models from 9 providers.

## Supported Providers

| Provider | Format | Models | Notes |
|----------|--------|--------|-------|
| **Euri** | OpenAI-compatible | 9 | Free 200K tokens/day |
| **OpenAI** | Native | 7 | GPT-4o, GPT-4.1, o3/o4-mini |
| **Anthropic** | Messages API | 3 | Claude Opus 4.6, Sonnet 4.5, Haiku 4.5 |
| **Google** | Gemini API | 3 | Gemini 2.5 Pro/Flash |
| **Groq** | OpenAI-compatible | 6 | Ultra-fast inference, free tier |
| **OpenRouter** | OpenAI-compatible | 12+ | 400+ models with one key |
| **DeepSeek** | OpenAI-compatible | 2 | DeepSeek Chat V3, Reasoner R1 |
| **xAI** | OpenAI-compatible | 2 | Grok 3, Grok 3 Mini |
| **Mistral** | OpenAI-compatible | 2 | Mistral Large, Small |

Plus **custom model input** — type any model ID for any provider.

## How to Use

1. Open `arena.html` in any browser
2. Click **API Keys** to add keys for providers you want to test
3. Pick a benchmark category (or write a custom prompt)
4. Select 2-4 models from any provider mix
5. Click **Run Arena** — all models fire in parallel
6. Watch results stream in, vote on the best
7. Check **Leaderboard** for aggregate rankings

## Features

- **9 providers, 50+ pre-loaded models** — add any custom model ID too
- **Cross-provider comparison** — pit Claude vs GPT vs Gemini vs Llama in one click
- **5 benchmark categories** with 25 test prompts (chat, code, reasoning, creative, instructions)
- **Parallel API calls** — fastest model visually appears first
- **Real-time metrics** — latency, tokens/sec, token counts
- **Voting + Leaderboard** — track win rates across all runs
- **History** — exportable as JSON
- **Zero dependencies** — single HTML file, no build step
- **Keys stored locally** — never sent anywhere except the provider's own API

## Tips

- **OpenRouter** is the easiest way to test 400+ models with a single key
- **Euri** is free (200K tokens/day) — great for quick tests
- **Groq** has a free tier with the fastest inference speeds
- Use the **custom model input** to add any model not in the pre-loaded list
