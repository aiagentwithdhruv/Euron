# How We Built Euron Model Arena with AI (In One Session)

**A step-by-step case study on AI-assisted development.**

By [@aiagentwithdhruv](https://github.com/aiagentwithdhruv) — Built in 3 hours using Claude Code

---

## The Vision

**Initial ask:**
> "I want to test and compare AI models side-by-side. Keep the Euri chat, but add a new tool where I can benchmark any model from any provider. Start simple, then add complexity — chat first, then video rendering, dashboard, memory. Make it deployable."

**Why this prompt worked:**
- Clear outcome ("compare models side-by-side")
- Scope flexibility ("start simple, add complexity")
- Technical constraints ("any provider, deployable")

---

## Build Process: Think → Build → Test → Fix → Ship

### Step 1: Research Before Building (10 min)

**Prompt:**
> "Research existing AI model comparison tools — what exists, what's missing, how do they work?"

**AI did:**
- Found Chatbot Arena, OpenRouter Rankings, Artificial Analysis
- Identified gaps: most are closed-source, backend-heavy, slow
- Recommended: single HTML file, browser-based, multi-provider

**Key lesson:** Let AI research competitive landscape BEFORE coding. Saves reinventing wheels.

---

### Step 2: v1 - Single Provider (30 min)

**Prompt:**
> "Build v1 with Euri models only. 2-4 models, side-by-side cards, benchmark prompts, voting, leaderboard. Single HTML file."

**AI delivered:**
- 19 Euri models
- 5 benchmark categories (chat, code, reasoning, creative, instructions)
- Parallel API calls with `Promise.allSettled`
- Real-time metrics (latency, tokens/sec)
- localStorage for voting + history

**Tested:**
- Opened HTML → worked
- Selected 3 models → fired in parallel → results appeared
- ✅ v1 complete

**Key lesson:** Start with ONE provider. Validate core UX before scaling.

---

### Step 3: Multi-Provider Expansion (45 min)

**Prompt:**
> "Add ALL major providers — OpenAI, Anthropic, Google, Groq, OpenRouter, DeepSeek, xAI, Mistral. Purpose: test ANY model, not just Euri."

**AI did:**
- Added 9 providers, 50+ models
- Built multi-API routing (3 formats: OpenAI-compatible, Anthropic Messages API, Google Gemini API)
- API key management with localStorage
- Custom model input (type any model ID)

**Tested:**
- Added OpenAI key → GPT models unlocked ✅
- Added Anthropic key → Claude models unlocked ✅
- Ran cross-provider comparison (Claude vs GPT vs Gemini) → worked ✅

**Key lesson:** Test incrementally. One provider at a time. Don't trust AI output — RUN IT.

---

### Step 4: Bug Fixing — The API Keys Issue (15 min)

**User reported (with screenshot):**
> "Can't see where to add API keys. Models are locked."

**Root cause:** Settings panel hidden behind toggle, no visual cue for first-time users.

**Prompt:**
> "Fix this — settings panel not visible. Auto-open when no keys saved, add visual indicator."

**AI fixed:**
- Auto-open settings panel if `localStorage` is empty
- Pulsing purple animation on "API Keys" button
- Key count badge in button label

**Tested:**
- Cleared localStorage → refreshed → settings auto-opened ✅
- Added keys → badge showed "5 keys" ✅

**Key lesson:** Screenshots are gold. AI can't guess UI bugs — SHOW it.

---

### Step 5: Bug Fixing — Cards Stuck on "Generating..." (20 min)

**User reported (with screenshot):**
> "Results table shows data, but cards stuck on 'Generating...'. Why?"

**Root cause found by AI:**
```javascript
// BROKEN CODE:
function cssId(m) {
  return "card-" + (m.provider + "_" + m.id).replace(/[\/\.\:]/g, "_");
}
// Result objects have m.modelId, not m.id → all cards got same DOM ID
```

**Fix:**
```javascript
function cssId(m) {
  return "card-" + (m.provider + "_" + (m.modelId || m.id)).replace(/[\/\.\:]/g, "_");
}
```

**Tested:**
- Ran 4 models → all cards updated in real-time ✅

**Key lesson:** When AI writes code, TEST edge cases. DOM lookups fail silently.

---

### Step 6: Deployment — GitHub Pages (30 min)

**Prompt:**
> "Deploy this. People should access it live, OR run locally, OR download single HTML file. Free hosting."

**AI did:**
- Created GitHub Actions workflow for Pages deployment
- Organized repo structure:
  ```
  index.html          ← Landing page
  model-arena/        ← 50+ models tool
  euri-tester/        ← Euri-only chat tool
  ```
- Updated READMEs with 3 access methods (live link, clone, download)

**Tested:**
- Pushed to GitHub → Action ran in 19 seconds ✅
- Opened live link → both tools loaded ✅
- Downloaded `arena.html` → opened locally → worked offline ✅

**Key lesson:** AI knows deployment patterns. Ask for "free, easy, no server" — it'll route you right.

---

## The Iterative Testing Loop (Critical)

```
Prompt → AI builds → YOU test → Find bug → Show AI (screenshot) → AI fixes → Test again
```

**Why this matters:**
- AI writes 90% correct code
- That last 10% (edge cases, UX bugs, DOM issues) only appears when YOU test
- Screenshots > descriptions. Show the bug, don't describe it.

**Examples from this project:**
1. Settings panel hidden → screenshot → fixed in 1 iteration
2. Cards stuck loading → screenshot → root cause found in 2 minutes
3. All bugs caught because WE TESTED, not because we trusted AI output

---

## Key Principles for AI-Assisted Development

### 1. **Research First, Code Second**
- Ask AI: "What exists? What's missing? Best approach?"
- Saves hours of rebuilding known patterns

### 2. **Start Small, Scale Fast**
- v1: Single provider, core UX
- v2: Multi-provider, 50+ models
- Built in 3 hours because v1 validated the approach

### 3. **Test Everything**
- Open the file. Click the buttons. Add bad inputs.
- AI can't test for you — it's a code generator, not a QA engineer

### 4. **Screenshots Are Your Best Tool**
- "This is broken" → AI guesses
- [Screenshot] → AI sees the exact issue → fixes in 1 try

### 5. **Iterate on Bugs, Don't Rebuild**
- Don't say "rewrite this"
- Say "here's the bug [screenshot], fix the root cause"

### 6. **Deployment Should Be Trivial**
- GitHub Pages for static sites (free, auto-deploy)
- Vercel/Netlify for Next.js (free tier)
- Modal for APIs (free tier)
- Ask AI: "Deploy this free and fast" — it knows the patterns

---

## Technical Highlights

### Multi-Provider API Routing (9 providers, 3 formats)

**Challenge:** Each provider has different API format.

**Solution:** Single `callModel()` function routes to correct format:

```javascript
if (provider === 'anthropic') {
  // Anthropic Messages API
  headers['x-api-key'] = apiKey;
  headers['anthropic-dangerous-direct-browser-access'] = 'true';
  endpoint = '/messages';
} else if (provider === 'google') {
  // Google Gemini API (key in query param)
  endpoint = `/models/${model.id}:generateContent?key=${apiKey}`;
} else {
  // OpenAI-compatible (6 providers)
  headers['Authorization'] = `Bearer ${apiKey}`;
  endpoint = '/chat/completions';
}
```

**Why this works:** Centralized routing. Add new provider = 3 lines of code.

---

### Parallel Benchmarking with Progressive Rendering

**Challenge:** Running 4 models sequentially takes 20+ seconds.

**Solution:** `Promise.allSettled` + progressive card updates:

```javascript
const promises = selectedModels.map(m => callModel(m, prompt));
const results = await Promise.allSettled(promises);

results.forEach((result, i) => {
  if (result.status === 'fulfilled') {
    renderSingleCard(result.value); // Update card instantly
  }
});
```

**Impact:** Fastest model appears in 1-2 seconds. User sees progress, not a spinner.

---

### Zero-Dependency Architecture

**Decision:** Single HTML file. No npm, no build step, no framework.

**Why:**
- ✅ Works offline (download + double-click)
- ✅ Easy to audit (view source = entire codebase)
- ✅ Fast to deploy (GitHub Pages = drag & drop)
- ✅ Future-proof (no dependencies to break)

**Tradeoff:** No TypeScript, no hot reload. Worth it for simplicity.

---

## What We Shipped

**Live:** https://aiagentwithdhruv.github.io/Euron/

**Features:**
- 9 providers, 50+ models
- Cross-provider comparison (Claude vs GPT vs Gemini)
- 5 benchmark categories, 25 test prompts
- Real-time metrics, voting, leaderboard
- API keys stored locally (never sent to our server)
- Single HTML file, works offline

**Time to build:** 3 hours
**Bugs found:** 2 (both caught by user testing)
**Iterations:** 6 prompts from idea → deployment
**Cost:** $0 (GitHub Pages free)

---

## Lessons for Your AI Journey

1. **AI is a 10x amplifier, not a replacement.** You drive, AI codes.
2. **Testing is YOUR job.** AI writes it, you break it, AI fixes it.
3. **Start simple, iterate fast.** v1 in 30 min beats perfect-but-never-shipped.
4. **Screenshots > words.** Show the bug, get instant fixes.
5. **Deploy early.** Live link = real feedback. Localhost = assumptions.

---

## Try It Yourself

**Clone the repo:**
```bash
git clone https://github.com/aiagentwithdhruv/Euron.git
open Euron/index.html
```

**Or just open:** https://aiagentwithdhruv.github.io/Euron/

**Questions?** Open an issue or DM [@aiagentwithdhruv](https://github.com/aiagentwithdhruv)

---

**Built with:** Claude Code (Opus 4.6)
**Total prompts:** 6 (research, v1, multi-provider, 2 bug fixes, deploy)
**Lines of code:** ~1000 (single HTML file)
**Time:** 3 hours (idea → live deployment)

**The secret:** Clear prompts + iterative testing + trusting AI for patterns, not perfection.
