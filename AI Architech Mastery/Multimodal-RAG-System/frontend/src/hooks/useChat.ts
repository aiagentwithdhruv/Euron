"use client";

import { useState, useCallback, useRef } from "react";
import type { ChatMessage, SourceReference, SourceType } from "@/lib/types";
import { queryStream } from "@/lib/api";

/** Generates a simple unique id. */
function uid(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(
    async (question: string, sourceType?: SourceType | null, topK?: number) => {
      if (!question.trim() || isLoading) return;

      // Create abort controller for this request
      const controller = new AbortController();
      abortRef.current = controller;

      // Add user message
      const userMsg: ChatMessage = { id: uid(), role: "user", content: question };
      const assistantId = uid();
      const assistantMsg: ChatMessage = {
        id: assistantId,
        role: "assistant",
        content: "",
        isStreaming: true,
      };

      setMessages((prev) => [...prev, userMsg, assistantMsg]);
      setIsLoading(true);

      try {
        const response = await queryStream(
          {
            question,
            source_type: sourceType ?? undefined,
            top_k: topK,
          },
          controller.signal
        );

        if (!response.body) throw new Error("No response body");

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n");
          buffer = lines.pop() || "";

          for (const line of lines) {
            if (!line.startsWith("data: ")) continue;
            const payload = line.slice(6).trim();

            if (payload === "[DONE]") continue;

            try {
              const data = JSON.parse(payload) as
                | { content: string }
                | { sources: SourceReference[] };

              if ("content" in data) {
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantId
                      ? { ...m, content: m.content + data.content }
                      : m
                  )
                );
              } else if ("sources" in data) {
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantId ? { ...m, sources: data.sources } : m
                  )
                );
              }
            } catch {
              // Skip malformed JSON lines
            }
          }
        }

        // Mark streaming as done
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId ? { ...m, isStreaming: false } : m
          )
        );
      } catch (err) {
        if (err instanceof DOMException && err.name === "AbortError") {
          // User cancelled — mark as done with current content
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId ? { ...m, isStreaming: false } : m
            )
          );
        } else {
          const errorMessage =
            err instanceof Error ? err.message : "An error occurred";
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId
                ? { ...m, content: `Error: ${errorMessage}`, isStreaming: false }
                : m
            )
          );
        }
      } finally {
        abortRef.current = null;
        setIsLoading(false);
      }
    },
    [isLoading]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  const stopStreaming = useCallback(() => {
    abortRef.current?.abort();
    abortRef.current = null;
  }, []);

  return { messages, isLoading, sendMessage, clearMessages, stopStreaming };
}
