"use client";

export default function IngestError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center h-full gap-4 text-zinc-400">
      <h2 className="text-xl font-semibold text-zinc-200">Something went wrong</h2>
      <p className="text-sm">{error.message || "An unexpected error occurred during ingestion."}</p>
      <button
        onClick={reset}
        className="px-4 py-2 text-sm bg-teal-600 text-white rounded-lg hover:bg-teal-500 transition-colors"
      >
        Try again
      </button>
    </div>
  );
}
