/**
 * Euri API Model Definitions
 * All available models on https://euron.one/euri
 * Last updated: Mar 3, 2026
 *
 * 39 models · 7 providers · 24 free · 15 premium
 */

export type EuriModelType = "text" | "embedding" | "image" | "speech-to-text";
export type EuriTier = "free" | "premium";
export type EuriSpeed = "ultra-fast" | "very-fast" | "fast" | "medium";
export type EuriCost = "very-low" | "low" | "medium" | "high";
export type EuriProvider = "alibaba" | "anthropic" | "google" | "groq" | "meta" | "openai" | "together";

export interface EuriModel {
  id: string;
  name: string;
  provider: EuriProvider;
  type: EuriModelType;
  tier: EuriTier;
  contextWindow: number;
  speed: EuriSpeed;
  cost: EuriCost;
  pricing?: { input: number; output: number }; // $ per 1M tokens
  capabilities: string[];
}

// ── Text Generation Models — Free (20) ─────────────────────────────

export const EURI_FREE_TEXT_MODELS: EuriModel[] = [
  // Alibaba
  {
    id: "qwen/qwen3-32b",
    name: "Qwen 3 32B",
    provider: "alibaba",
    type: "text",
    tier: "free",
    contextWindow: 128_000,
    speed: "fast",
    cost: "medium",
    pricing: { input: 0.29, output: 0.59 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },

  // Google
  {
    id: "gemini-2.0-flash",
    name: "Gemini 2.0 Flash",
    provider: "google",
    type: "text",
    tier: "free",
    contextWindow: 1_000_000,
    speed: "very-fast",
    cost: "low",
    pricing: { input: 0.10, output: 0.40 },
    capabilities: ["Text Generation", "Code Generation", "Multimodal"],
  },
  {
    id: "gemini-2.5-pro",
    name: "Gemini 2.5 Pro",
    provider: "google",
    type: "text",
    tier: "free",
    contextWindow: 2_000_000,
    speed: "fast",
    cost: "medium",
    pricing: { input: 1.25, output: 10.00 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },
  {
    id: "gemini-2.5-flash",
    name: "Gemini 2.5 Flash",
    provider: "google",
    type: "text",
    tier: "free",
    contextWindow: 1_000_000,
    speed: "very-fast",
    cost: "low",
    pricing: { input: 0.15, output: 0.60 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },
  {
    id: "gemini-2.5-pro-preview-06-05",
    name: "Gemini 2.5 Pro Preview",
    provider: "google",
    type: "text",
    tier: "free",
    contextWindow: 2_000_000,
    speed: "fast",
    cost: "medium",
    pricing: { input: 1.25, output: 10.00 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },
  {
    id: "gemini-2.5-flash-preview-05-20",
    name: "Gemini 2.5 Flash Preview",
    provider: "google",
    type: "text",
    tier: "free",
    contextWindow: 1_000_000,
    speed: "very-fast",
    cost: "low",
    pricing: { input: 0.15, output: 0.60 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },
  {
    id: "gemini-2.5-flash-lite-preview-06-17",
    name: "Gemini 2.5 Flash Lite Preview",
    provider: "google",
    type: "text",
    tier: "free",
    contextWindow: 128_000,
    speed: "ultra-fast",
    cost: "very-low",
    pricing: { input: 0.10, output: 0.40 },
    capabilities: ["Text Generation", "Conversation", "Instruction Following"],
  },
  {
    id: "gemini-3-pro",
    name: "Gemini 3 Pro",
    provider: "google",
    type: "text",
    tier: "free",
    contextWindow: 1_000_000,
    speed: "fast",
    cost: "low",
    pricing: { input: 0, output: 0 },
    capabilities: ["Text Generation", "Code Generation", "Multimodal"],
  },

  // Groq
  {
    id: "groq/compound",
    name: "Groq Compound",
    provider: "groq",
    type: "text",
    tier: "free",
    contextWindow: 131_000,
    speed: "fast",
    cost: "medium",
    pricing: { input: 0.59, output: 0.79 },
    capabilities: ["Text Generation", "Code Generation", "Web Search"],
  },
  {
    id: "groq/compound-mini",
    name: "Groq Compound Mini",
    provider: "groq",
    type: "text",
    tier: "free",
    contextWindow: 131_000,
    speed: "fast",
    cost: "low",
    pricing: { input: 0.20, output: 0.34 },
    capabilities: ["Text Generation", "Code Generation", "Web Search"],
  },

  // Meta
  {
    id: "llama-4-scout-17b-16e-instruct",
    name: "Llama 4 Scout",
    provider: "meta",
    type: "text",
    tier: "free",
    contextWindow: 128_000,
    speed: "fast",
    cost: "low",
    pricing: { input: 0.11, output: 0.34 },
    capabilities: ["Text Generation", "Conversation", "Instruction Following"],
  },
  {
    id: "llama-3.3-70b-versatile",
    name: "Llama 3.3 70B",
    provider: "meta",
    type: "text",
    tier: "free",
    contextWindow: 128_000,
    speed: "medium",
    cost: "medium",
    pricing: { input: 0.59, output: 0.79 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },
  {
    id: "llama-3.1-8b-instant",
    name: "Llama 3.1 8B Instant",
    provider: "meta",
    type: "text",
    tier: "free",
    contextWindow: 128_000,
    speed: "very-fast",
    cost: "very-low",
    pricing: { input: 0.05, output: 0.08 },
    capabilities: ["Text Generation", "Code Generation", "Conversation"],
  },
  {
    id: "llama-guard-4-12b",
    name: "Llama Guard 4 12B",
    provider: "meta",
    type: "text",
    tier: "free",
    contextWindow: 128_000,
    speed: "fast",
    cost: "low",
    pricing: { input: 0.20, output: 0.20 },
    capabilities: ["Content Moderation", "Safety Classification"],
  },

  // OpenAI
  {
    id: "gpt-5-nano-2025-08-07",
    name: "GPT-5 Nano",
    provider: "openai",
    type: "text",
    tier: "free",
    contextWindow: 128_000,
    speed: "ultra-fast",
    cost: "very-low",
    pricing: { input: 0.10, output: 0.40 },
    capabilities: ["Text Generation", "Conversation", "Instruction Following"],
  },
  {
    id: "gpt-5-mini-2025-08-07",
    name: "GPT-5 Mini",
    provider: "openai",
    type: "text",
    tier: "free",
    contextWindow: 128_000,
    speed: "fast",
    cost: "low",
    pricing: { input: 0.40, output: 1.60 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },
  {
    id: "gpt-4.1-nano",
    name: "GPT-4.1 Nano",
    provider: "openai",
    type: "text",
    tier: "free",
    contextWindow: 128_000,
    speed: "ultra-fast",
    cost: "very-low",
    pricing: { input: 0.10, output: 0.40 },
    capabilities: ["Text Generation", "Conversation", "Instruction Following"],
  },
  {
    id: "gpt-4.1-mini",
    name: "GPT-4.1 Mini",
    provider: "openai",
    type: "text",
    tier: "free",
    contextWindow: 128_000,
    speed: "fast",
    cost: "low",
    pricing: { input: 0.40, output: 1.60 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },
  {
    id: "openai/gpt-oss-20b",
    name: "GPT-OSS 20B",
    provider: "openai",
    type: "text",
    tier: "free",
    contextWindow: 128_000,
    speed: "fast",
    cost: "low",
    pricing: { input: 0.10, output: 0.30 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },
  {
    id: "openai/gpt-oss-120b",
    name: "GPT-OSS 120B",
    provider: "openai",
    type: "text",
    tier: "free",
    contextWindow: 128_000,
    speed: "medium",
    cost: "medium",
    pricing: { input: 0.30, output: 0.90 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },
];

// ── Text Generation Models — Premium (13) ──────────────────────────

export const EURI_PREMIUM_TEXT_MODELS: EuriModel[] = [
  // Anthropic
  {
    id: "claude-sonnet-4",
    name: "Claude Sonnet 4",
    provider: "anthropic",
    type: "text",
    tier: "premium",
    contextWindow: 200_000,
    speed: "fast",
    cost: "medium",
    pricing: { input: 3.00, output: 15.00 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },
  {
    id: "claude-opus-4",
    name: "Claude Opus 4",
    provider: "anthropic",
    type: "text",
    tier: "premium",
    contextWindow: 200_000,
    speed: "medium",
    cost: "high",
    pricing: { input: 15.00, output: 75.00 },
    capabilities: ["Text Generation", "Code Generation", "Complex Reasoning"],
  },
  {
    id: "claude-sonnet-4-6",
    name: "Claude Sonnet 4.6",
    provider: "anthropic",
    type: "text",
    tier: "premium",
    contextWindow: 200_000,
    speed: "fast",
    cost: "medium",
    pricing: { input: 3.00, output: 15.00 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },
  {
    id: "claude-opus-4-6",
    name: "Claude Opus 4.6",
    provider: "anthropic",
    type: "text",
    tier: "premium",
    contextWindow: 200_000,
    speed: "medium",
    cost: "high",
    pricing: { input: 15.00, output: 75.00 },
    capabilities: ["Text Generation", "Code Generation", "Complex Reasoning"],
  },

  // Google
  {
    id: "gemini-3-flash",
    name: "Gemini 3 Flash",
    provider: "google",
    type: "text",
    tier: "premium",
    contextWindow: 1_000_000,
    speed: "very-fast",
    cost: "low",
    pricing: { input: 0.15, output: 0.60 },
    capabilities: ["Text Generation", "Code Generation", "Multimodal"],
  },
  {
    id: "gemini-3.1-pro",
    name: "Gemini 3.1 Pro",
    provider: "google",
    type: "text",
    tier: "premium",
    contextWindow: 2_000_000,
    speed: "fast",
    cost: "medium",
    pricing: { input: 1.25, output: 10.00 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },

  // OpenAI
  {
    id: "gpt-4.1",
    name: "GPT-4.1",
    provider: "openai",
    type: "text",
    tier: "premium",
    contextWindow: 128_000,
    speed: "fast",
    cost: "medium",
    pricing: { input: 2.00, output: 8.00 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },
  {
    id: "gpt-5",
    name: "GPT-5",
    provider: "openai",
    type: "text",
    tier: "premium",
    contextWindow: 128_000,
    speed: "fast",
    cost: "medium",
    pricing: { input: 2.00, output: 8.00 },
    capabilities: ["Text Generation", "Code Generation", "Complex Reasoning"],
  },
  {
    id: "gpt-5.1",
    name: "GPT-5.1",
    provider: "openai",
    type: "text",
    tier: "premium",
    contextWindow: 128_000,
    speed: "fast",
    cost: "medium",
    pricing: { input: 2.00, output: 8.00 },
    capabilities: ["Text Generation", "Code Generation", "Complex Reasoning"],
  },
  {
    id: "gpt-5-mini",
    name: "GPT-5 Mini",
    provider: "openai",
    type: "text",
    tier: "premium",
    contextWindow: 128_000,
    speed: "fast",
    cost: "low",
    pricing: { input: 0.40, output: 1.60 },
    capabilities: ["Text Generation", "Code Generation", "Mathematical Reasoning"],
  },
  {
    id: "gpt-5-nano",
    name: "GPT-5 Nano",
    provider: "openai",
    type: "text",
    tier: "premium",
    contextWindow: 128_000,
    speed: "ultra-fast",
    cost: "very-low",
    pricing: { input: 0.10, output: 0.40 },
    capabilities: ["Text Generation", "Conversation", "Instruction Following"],
  },
  {
    id: "o3",
    name: "OpenAI o3",
    provider: "openai",
    type: "text",
    tier: "premium",
    contextWindow: 200_000,
    speed: "medium",
    cost: "high",
    pricing: { input: 10.00, output: 40.00 },
    capabilities: ["Complex Reasoning", "Code Generation", "Mathematical Reasoning"],
  },
  {
    id: "o4-mini",
    name: "OpenAI o4-mini",
    provider: "openai",
    type: "text",
    tier: "premium",
    contextWindow: 200_000,
    speed: "medium",
    cost: "medium",
    pricing: { input: 1.10, output: 4.40 },
    capabilities: ["Complex Reasoning", "Code Generation", "Mathematical Reasoning"],
  },
];

// ── Embedding Models (3 — all free) ────────────────────────────────

export const EURI_EMBEDDING_MODELS: EuriModel[] = [
  {
    id: "gemini-embedding-001",
    name: "Gemini Embedding 001",
    provider: "google",
    type: "embedding",
    tier: "free",
    contextWindow: 8_000,
    speed: "very-fast",
    cost: "very-low",
    pricing: { input: 0.15, output: 0 },
    capabilities: ["Semantic Search", "Text Classification", "Named Entity Recognition"],
  },
  {
    id: "text-embedding-3-small",
    name: "Text Embedding 3 Small",
    provider: "openai",
    type: "embedding",
    tier: "free",
    contextWindow: 8_000,
    speed: "very-fast",
    cost: "very-low",
    pricing: { input: 0.02, output: 0 },
    capabilities: ["Semantic Search", "Text Classification", "Named Entity Recognition"],
  },
  {
    id: "togethercomputer/m2-bert-80M-32k-retrieval",
    name: "M2 BERT 80M 32K Retrieval",
    provider: "together",
    type: "embedding",
    tier: "free",
    contextWindow: 32_000,
    speed: "very-fast",
    cost: "very-low",
    pricing: { input: 0.008, output: 0 },
    capabilities: ["Semantic Search", "Text Classification", "Named Entity Recognition"],
  },
];

// ── Image Generation Models (1 — free) ─────────────────────────────

export const EURI_IMAGE_MODELS: EuriModel[] = [
  {
    id: "gemini-3-pro-image-preview",
    name: "Gemini 3 Pro Image Preview (Nano Banana Pro)",
    provider: "google",
    type: "image",
    tier: "free",
    contextWindow: 0,
    speed: "very-fast",
    cost: "low",
    pricing: { input: 0.04, output: 0 },
    capabilities: ["Image Generation", "Multimodal", "Creative Writing"],
  },
];

// ── Speech to Text Models (2 — premium) ────────────────────────────

export const EURI_STT_MODELS: EuriModel[] = [
  {
    id: "whisper-large-v3",
    name: "Whisper Large V3",
    provider: "openai",
    type: "speech-to-text",
    tier: "premium",
    contextWindow: 0,
    speed: "fast",
    cost: "medium",
    pricing: { input: 0, output: 0 }, // $0.111/hr
    capabilities: ["Speech to Text", "Multilingual", "Transcription"],
  },
  {
    id: "whisper-large-v3-turbo",
    name: "Whisper Large V3 Turbo",
    provider: "openai",
    type: "speech-to-text",
    tier: "premium",
    contextWindow: 0,
    speed: "very-fast",
    cost: "low",
    pricing: { input: 0, output: 0 }, // $0.04/hr
    capabilities: ["Speech to Text", "Multilingual", "Transcription"],
  },
];

// ── All Models ──────────────────────────────────────────────────────

export const EURI_TEXT_MODELS: EuriModel[] = [
  ...EURI_FREE_TEXT_MODELS,
  ...EURI_PREMIUM_TEXT_MODELS,
];

export const ALL_EURI_MODELS: EuriModel[] = [
  ...EURI_FREE_TEXT_MODELS,
  ...EURI_PREMIUM_TEXT_MODELS,
  ...EURI_EMBEDDING_MODELS,
  ...EURI_IMAGE_MODELS,
  ...EURI_STT_MODELS,
];

// ── Defaults ────────────────────────────────────────────────────────

export const EURI_DEFAULT_TEXT_MODEL = "gemini-2.5-flash";
export const EURI_DEFAULT_FAST_MODEL = "gemini-2.5-flash-lite-preview-06-17";
export const EURI_DEFAULT_SMART_MODEL = "gemini-2.5-pro";
export const EURI_DEFAULT_EMBEDDING_MODEL = "gemini-embedding-001";
export const EURI_DEFAULT_IMAGE_MODEL = "gemini-3-pro-image-preview";

// ── Helpers ─────────────────────────────────────────────────────────

export function getEuriModel(id: string): EuriModel | undefined {
  return ALL_EURI_MODELS.find((m) => m.id === id);
}

export function getEuriModelsByProvider(provider: EuriProvider): EuriModel[] {
  return ALL_EURI_MODELS.filter((m) => m.provider === provider);
}

export function getEuriModelsByType(type: EuriModelType): EuriModel[] {
  return ALL_EURI_MODELS.filter((m) => m.type === type);
}

export function getEuriModelsByTier(tier: EuriTier): EuriModel[] {
  return ALL_EURI_MODELS.filter((m) => m.tier === tier);
}

export function getFreeModels(): EuriModel[] {
  return ALL_EURI_MODELS.filter((m) => m.tier === "free");
}

export function getPremiumModels(): EuriModel[] {
  return ALL_EURI_MODELS.filter((m) => m.tier === "premium");
}
