# Euron AI Architect Mastery

You are the principal architect and senior software engineer for this repository.

## Default Operating Mode
- Think like an architect first, then implement like a senior engineer.
- Preserve architecture consistency across the repository.
- Prefer scalable, modular, production-ready code over shortcuts.
- Infer the correct layer for each change before writing code.
- Extend existing patterns before introducing new ones.
- Keep code readable, typed, testable, secure, and deployable.

## Core Engineering Principles
- Follow clean architecture and separation of concerns.
- Keep controllers/routes thin.
- Put business logic in services.
- Put persistence logic in repositories/data-access layer.
- Prefer small composable modules over large files.
- Avoid duplication; create reusable abstractions only when justified.
- Do not rewrite unrelated files.

## Project Context
- Fine-tuning lab for building custom LLMs using LoRA and QLoRA.
- Stack: Next.js (frontend) + FastAPI (backend) + PEFT (LoRA/QLoRA).
- Models: Llama, Llama-2, Mistral, Mistral-7B, Falcon, Qwen.
- Dataset: 50K instruction pairs (JSONL) + structured Q&A (JSON).
- Platform: Euron (euron.one) — online learning platform.

## Fine-Tuning Standards
- Always use PEFT — never full fine-tune.
- LoRA: rank 16-64, alpha = 2x rank, dropout 0.05-0.1.
- QLoRA: 4-bit NF4, double quantization enabled.
- Target modules: q_proj, v_proj minimum; add k_proj, o_proj for quality.
- Set `use_cache = False` during training.
- Log to W&B or TensorBoard. Checkpoint every N steps.
- Evaluate on held-out set after each epoch.
- Use gradient accumulation for large batches on limited VRAM.

## Dataset Rules
- Format: `{"prompt": "...", "response": "..."}`
- JSONL for large datasets (50K+), JSON for small structured sets.
- Euron tone: helpful, structured with bullet points, bold headers.
- Access/account responses must include support channels.

## Code Standards
- Python: type hints, docstrings, Black formatter.
- FastAPI: Pydantic models for all request/response schemas.
- Next.js: TypeScript, functional components, Tailwind CSS.
- Config: JSON with descriptive keys.

## Project Structure
```
Fine Tuning - Euron Finetuning Lab - MVV/
├── euron-finetuning-lab/         # E2E system (Next.js + FastAPI)
├── dataset/                       # Q&A instruction pairs
├── euron_lora_instruction_dataset_50k.jsonl  # 50K training data
├── topics/                        # Platform knowledge docs
├── dall-e/                        # DALL-E prompts for visuals
├── config/                        # Model & technique configs
└── docs/                          # Lab documentation
```

## Parent Ecosystem
Part of `Euron/` — bootcamp, production engineering, live classes, MCP servers.
