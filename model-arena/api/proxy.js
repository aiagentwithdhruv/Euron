/**
 * Universal CORS Proxy — Vercel Edge Function
 * Proxies requests to any API that doesn't support browser CORS.
 * Used by Model Arena for Euri API (which returns 500 on OPTIONS preflight).
 *
 * Usage: POST /api/proxy?url=https://api.euron.one/api/v1/euri/chat/completions
 * Headers and body are forwarded as-is.
 */
export const config = { runtime: "edge" };

// Only allow proxying to these API domains (security)
const ALLOWED_HOSTS = [
  "api.euron.one",
];

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, x-api-key, anthropic-version, anthropic-dangerous-direct-browser-access, HTTP-Referer, X-Title",
  "Access-Control-Max-Age": "86400",
};

export default async function handler(req) {
  // Handle preflight
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }

  const reqUrl = new URL(req.url);
  const targetUrl = reqUrl.searchParams.get("url");
  if (!targetUrl) {
    return new Response(JSON.stringify({ error: "Missing ?url= param" }), {
      status: 400,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }

  // Security: only proxy to allowed hosts
  let parsed;
  try { parsed = new URL(targetUrl); } catch {
    return new Response(JSON.stringify({ error: "Invalid URL" }), {
      status: 400,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }
  if (!ALLOWED_HOSTS.includes(parsed.hostname)) {
    return new Response(JSON.stringify({ error: "Host not allowed: " + parsed.hostname }), {
      status: 403,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }

  // Forward request
  const headers = {};
  for (const [key, value] of req.headers.entries()) {
    const lower = key.toLowerCase();
    if (["content-type", "authorization", "x-api-key", "anthropic-version",
         "anthropic-dangerous-direct-browser-access", "http-referer", "x-title"].includes(lower)) {
      headers[key] = value;
    }
  }

  try {
    const upstream = await fetch(targetUrl, {
      method: req.method,
      headers,
      body: req.method !== "GET" ? await req.arrayBuffer() : undefined,
    });

    const body = await upstream.arrayBuffer();
    return new Response(body, {
      status: upstream.status,
      headers: {
        ...CORS_HEADERS,
        "Content-Type": upstream.headers.get("Content-Type") || "application/json",
      },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 502,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }
}
