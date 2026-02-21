# Fine Tuning - Euron Finetuning Lab - MVV

Euron fine-tuning lab MVP — techniques, models, and dataset for training.

## Techniques
- **LoRA** — Low-Rank Adaptation
- **QLoRA** — Quantized Low-Rank Adaptation

## Dataset
See `dataset/euron_lore_instruction.json` for prompt–response pairs (Euron lore, support Q&A, Resume AI).

## Models & Techniques

| Technique | Models |
|-----------|--------|
| **LoRA** | Llama, Mistral, Falcon |
| **QLoRA** | Llama-2, Mistral-7B, Qwen |

## Structure
- `euron-finetuning-lab/` — **Full E2E fine-tuning system** (Next.js + FastAPI + LoRA/QLoRA)
- `dataset/` — Fine-tuning Q&A dataset
- `topics/` — Markdown topic docs (password, support, courses, Resume AI)
- `dall-e/` — DALL-E prompts for platform visuals
- `config/` — Model and technique configs
- `docs/` — Lab documentation
