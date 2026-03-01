# Live Class Delivery — SKILL.md

> Dhruv's teaching delivery system. Patterns for compelling live classes, presentation structure, and continuous improvement.

---

## The Problem

Dhruv's technical content is excellent. The gap is **presentation delivery** — making the content land with maximum impact during live sessions.

This skill captures patterns, structures, and checklists that compound over time.

---

## Presentation Architecture (The "Build Live" Format)

Dhruv's classes are NOT slide decks. They're live builds. But even live builds need structure.

### The 5-Act Class Structure

```
ACT 1 — HOOK (5 min)
  "Here's what we're building today, and here's why it matters to YOUR career/business"
  → Show the finished system FIRST (demo the end result)
  → Create desire: "By the end of this session, you'll have this running"

ACT 2 — CONTEXT (10 min)
  "Here's the architecture behind what you just saw"
  → One clear diagram (Excalidraw/draw.io)
  → Explain the system, not the tools
  → Connect to real business value (Rs. amounts, time saved, clients served)

ACT 3 — BUILD (60-70 min)
  "Let's build this together, step by step"
  → Screen share + live coding
  → Narrate decisions: "I'm choosing X because..."
  → Pause at checkpoints: "Everyone with me?"
  → Handle errors live (shows real debugging)

ACT 4 — DEPLOY (15-20 min)
  "Now let's make it live — production, not localhost"
  → Push to GitHub
  → Deploy to Vercel/VPS
  → Show it working from a fresh browser/phone
  → This is the "wow" moment

ACT 5 — EXERCISE + WRAP (10-15 min)
  "Your turn — here's your assignment"
  → Give a specific, achievable exercise
  → Share the repo/template
  → Preview next session
  → "Questions?"
```

### Time Template (2-hour session)

| Act | Duration | Content |
|-----|----------|---------|
| Hook | 0:00 - 0:05 | Demo finished system, create desire |
| Context | 0:05 - 0:15 | Architecture diagram, business value |
| Build (Part 1) | 0:15 - 0:55 | Core system build |
| Break / Q&A | 0:55 - 1:00 | Quick questions, breathing room |
| Build (Part 2) | 1:00 - 1:30 | Complete build + edge cases |
| Deploy | 1:30 - 1:50 | Push → deploy → verify live |
| Exercise + Wrap | 1:50 - 2:00 | Assignment, next session preview |

---

## Presentation Improvement Patterns

### Pattern 1: "Show Don't Tell" Opening
**Instead of:** "Today we'll learn about MCP..."
**Do this:** Share screen → run a command → AI automatically sends an email, creates a calendar event, updates a spreadsheet → "That just happened in 3 seconds. Let me show you how."

### Pattern 2: The Architecture Anchor
Every class needs ONE visual anchor — a diagram that students can screenshot and remember.
- Use Excalidraw (hand-drawn feel = approachable)
- Max 5-7 boxes connected by arrows
- Label every connection with what flows through it
- Return to this diagram multiple times during the build

### Pattern 3: Narrate Your Thinking
During live coding, say out loud:
- "I'm choosing FastAPI here because..."
- "This is the part that breaks most often, so..."
- "A client would pay Rs.50K for just this piece because..."
- "The mistake most people make here is..."

This is what separates a tutorial from a masterclass.

### Pattern 4: Planned "Failures"
Intentionally hit common errors and debug them live:
- Wrong API key → show the error → fix it
- Missing env variable → explain why it matters
- Deployment fails → troubleshoot live

Students learn MORE from watching you debug than from watching a perfect demo.

### Pattern 5: Revenue Anchoring
Connect every technical concept to money:
- "This automation replaces 2 hours of manual work daily → Rs.30K/month value"
- "A client would pay Rs.50K-1L for this exact system"
- "This is what I charged Rs.80K for at Bartisans"

This keeps non-technical students engaged and gives developers business context.

### Pattern 6: The "Checkpoint" Rhythm
Every 15 minutes, pause and:
1. Recap what we just built
2. Show it working (run the test/trigger)
3. Ask "Everyone with me? Drop a thumbs up in chat"
4. Preview what's next

This prevents students from falling behind silently.

---

## Pre-Class Checklist

### 24 Hours Before
- [ ] Final system works end-to-end (tested fresh)
- [ ] Architecture diagram ready (Excalidraw/screenshot)
- [ ] Opening hook script written (first 60 seconds)
- [ ] Demo data prepared (fake leads, test emails, etc.)
- [ ] Backup plan if live coding breaks (pre-recorded fallback clip)
- [ ] GitHub repo ready (template for students)
- [ ] Student exercise defined (specific, achievable in 30 min)

### 1 Hour Before
- [ ] Close unnecessary browser tabs + apps
- [ ] Terminal clean (no sensitive data visible)
- [ ] Zoom settings: screen share optimized, chat visible
- [ ] Water + notes nearby
- [ ] Phone on DND
- [ ] Test internet speed + backup hotspot ready

### During Class
- [ ] Start with the hook (demo first, explain second)
- [ ] Return to architecture diagram at each checkpoint
- [ ] Narrate decisions out loud
- [ ] Check chat every 15 minutes
- [ ] Time check at 1-hour mark (adjust pace if needed)
- [ ] Deploy something live before wrapping up
- [ ] End with clear exercise + next session preview

### Post-Class (Within 24 Hours)
- [ ] Upload recording (if applicable)
- [ ] Update CLASSES-STATUS.md (what worked, what to improve)
- [ ] Share repo/template with students
- [ ] Post exercise instructions in WhatsApp group
- [ ] Note top 3 student questions (for future content)
- [ ] Rate own presentation 1-5 and note specific improvement

---

## Presentation Weak Spots to Fix (Dhruv's Self-Assessment)

> This section tracks specific areas for improvement. Update after every class.

| Area | Current Level | Target | How to Improve |
|------|--------------|--------|----------------|
| Opening hook | Jumps to content too fast | Captivating first 60 seconds | Script the first minute, practice it |
| Slide design | Minimal/no slides | 3-5 high-impact visual anchors per class | Create Excalidraw templates |
| Pacing | Sometimes rushes through complex parts | Consistent rhythm with checkpoints | Use timer, checkpoint every 15 min |
| Storytelling | Mostly technical narration | Weave in business stories + client examples | Prep 2-3 stories per class |
| Student engagement | One-way delivery | Interactive questions + exercises | Plan 3 interaction points per class |
| Energy management | Consistent but flat | Peaks at key moments (hook, deploy, wrap) | Mark "energy up" moments in notes |

---

## Slide/Visual Templates

When slides ARE needed (rare), use this structure:

### Title Slide
```
[Big statement — not the topic name]
"Your AI should work while you sleep"
— Dhruv Tomar | AIwithDhruv
```

### Architecture Slide
```
[Excalidraw diagram — hand-drawn style]
Max 5-7 components
Clear data flow arrows
Labels on every connection
```

### "Before vs After" Slide
```
BEFORE: [manual process, time, cost]
AFTER:  [automated system, speed, savings]
→ This is what we're building today
```

### Money Slide
```
"This system is worth Rs.___ to a client"
[3 bullet points: what it replaces, time saved, revenue impact]
```

### Exercise Slide
```
YOUR TURN
1. [Specific step]
2. [Specific step]
3. [Specific step]
→ Share your result in the WhatsApp group
```

---

## Compounding Improvement System

After every 5 classes, review:
1. Watch the first 5 minutes of each recording — is the hook improving?
2. Count student questions — more questions = more engagement
3. Track exercise completion rate — if low, exercises are too hard
4. Ask for 1-word feedback: "What was the most valuable thing today?"
5. Compare energy levels across sessions — which format gave best energy?

**Goal:** Every class should be measurably better than the last. The skill compounds.

---

*Last updated: 2026-02-28 | Version: 1.0*
