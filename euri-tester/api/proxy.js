/**
 * Euri CORS Proxy — Vercel Edge Function
 * Proxies requests to Euri API, adding CORS headers.
 * Euri's API doesn't handle OPTIONS preflight, so browser
 * requests fail. This fixes it.
 *
 * Usage: POST /api/proxy?endpoint=/chat/completions
 * Headers and body are forwarded as-is to Euri.
 */
export const config = { runtime: "edge" };

const EURI_BASE = "https://api.euron.one/api/v1/euri";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
  "Access-Control-Max-Age": "86400",
};

export default async function handler(req) {
  // Handle preflight
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }

  const url = new URL(req.url);
  const endpoint = url.searchParams.get("endpoint");
  if (!endpoint) {
    return new Response(JSON.stringify({ error: "Missing ?endpoint= param" }), {
      status: 400,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }

  // Forward request to Euri
  const euriUrl = EURI_BASE + endpoint;
  const headers = {};
  for (const [key, value] of req.headers.entries()) {
    if (["content-type", "authorization"].includes(key.toLowerCase())) {
      headers[key] = value;
    }
  }

  try {
    const euriRes = await fetch(euriUrl, {
      method: req.method,
      headers,
      body: req.method !== "GET" ? await req.arrayBuffer() : undefined,
    });

    const body = await euriRes.arrayBuffer();
    return new Response(body, {
      status: euriRes.status,
      headers: {
        ...CORS_HEADERS,
        "Content-Type": euriRes.headers.get("Content-Type") || "application/json",
      },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 502,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }
}
