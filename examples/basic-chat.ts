/**
 * Example: Basic chat with Euri API
 * Works in any Next.js API route or Node.js script
 */

import { EuriClient } from "../euri-client";

const euri = new EuriClient("your-euri-api-key");

// ── Simple one-liner ────────────────────────────────────────────────

async function simpleChat() {
  const answer = await euri.chat("What is quantum computing?");
  console.log(answer);
}

// ── With system prompt + model selection ─────────────────────────────

async function customChat() {
  const answer = await euri.chat("Explain Docker in 3 sentences", {
    systemPrompt: "You are a senior DevOps engineer. Be concise.",
    model: "gemini-2.5-flash",
    temperature: 0.5,
    max_tokens: 500,
  });
  console.log(answer);
}

// ── Multi-turn conversation ─────────────────────────────────────────

async function multiTurnChat() {
  const response = await euri.chatCompletion([
    { role: "system", content: "You are a helpful coding assistant." },
    { role: "user", content: "Write a Python function to check if a number is prime." },
    { role: "assistant", content: "def is_prime(n):\n    if n < 2: return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0: return False\n    return True" },
    { role: "user", content: "Now optimize it for large numbers." },
  ], {
    model: "gpt-4.1-mini",
    temperature: 0.3,
  });

  console.log(response.choices[0].message.content);
  console.log("Tokens used:", response.usage?.total_tokens);
}

// ── Embeddings ──────────────────────────────────────────────────────

async function generateEmbeddings() {
  const vector = await euri.embed("Artificial intelligence is transforming healthcare");
  console.log("Dimensions:", vector.length);
  console.log("First 5 values:", vector.slice(0, 5));
}

// ── Image Generation ────────────────────────────────────────────────

async function generateImage() {
  const result = await euri.generateImage(
    "A futuristic city skyline at sunset, cyberpunk style"
  );
  console.log("Image URL:", result.data[0]?.url);
}

// Run examples
simpleChat();
