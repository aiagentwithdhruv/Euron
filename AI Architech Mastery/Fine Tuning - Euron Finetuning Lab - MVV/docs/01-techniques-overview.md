# Fine-Tuning Techniques Overview

## LoRA (Low-Rank Adaptation)
- **Models:** Llama, Mistral, Falcon
- Efficient fine-tuning with low-rank matrices
- Reduces trainable parameters while preserving base model quality

## QLoRA (Quantized Low-Rank Adaptation)
- **Models:** Llama-2, Mistral-7B, Qwen
- LoRA + quantization for memory-efficient training
- Enables fine-tuning on consumer hardware

## Dataset
Use `dataset/euron_lore_instruction.json` for prompt-response training.
