# Euri Model Arena

**Side-by-side AI model comparison tool.** Test 2-4 models simultaneously with the same prompt, compare speed and quality, vote on the best, and track results over time.

## How to Use

1. Open `arena.html` in any browser
2. Enter your [Euri API key](https://euron.one/euri)
3. Pick a benchmark category (or write a custom prompt)
4. Select 2-4 models to compare
5. Click **Run Arena** (or Cmd/Ctrl+Enter)
6. Watch results stream in — fastest model appears first
7. Vote on the best response
8. Check the **Leaderboard** tab for aggregate rankings

## Features

- **19 text models** from 5 providers (Google, OpenAI, Meta, Groq, Alibaba)
- **5 benchmark categories** with 25 pre-built test prompts:
  - Quick Chat — general knowledge
  - Code Gen — write functions and queries
  - Reasoning — logic puzzles and math
  - Creative — stories and analogies
  - Instructions — strict format compliance
- **Parallel API calls** — all models called simultaneously via `Promise.allSettled`
- **Real-time metrics** — latency (ms), tokens/sec, token counts. Best highlighted green.
- **Voting system** — vote on the best response per run
- **Leaderboard** — aggregate win rates, avg latency, avg tok/sec across all runs
- **History** — all runs saved to localStorage (max 100), exportable as JSON
- **Zero dependencies** — single HTML file, no build step

## Keyboard Shortcuts

- `Cmd/Ctrl + Enter` — Run Arena
