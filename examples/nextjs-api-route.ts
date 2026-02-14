/**
 * Example: Next.js API Route using Euri API
 * Drop this in any Next.js project at: src/app/api/euri/route.ts
 *
 * Requires: EURI_API_KEY in .env.local
 */

import { NextRequest, NextResponse } from "next/server";
import { EuriClient } from "../euri-client";

const euri = new EuriClient(process.env.EURI_API_KEY!);

export async function POST(req: NextRequest) {
  try {
    const { messages, model, temperature, max_tokens } = await req.json();

    if (!messages || !Array.isArray(messages)) {
      return NextResponse.json({ error: "messages array is required" }, { status: 400 });
    }

    const response = await euri.chatCompletion(messages, {
      model: model || "gemini-2.5-flash",
      temperature: temperature ?? 0.7,
      max_tokens: max_tokens ?? 1000,
    });

    return NextResponse.json({
      content: response.choices[0]?.message?.content || "",
      model: response.model,
      usage: response.usage,
    });
  } catch (error: any) {
    console.error("Euri API error:", error.message);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
