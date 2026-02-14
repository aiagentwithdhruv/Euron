"""
Example: Euri API with Python SDK
pip install euriai
"""

from euriai import EuriaiClient

# ── Basic Chat ───────────────────────────────────────────────────────

client = EuriaiClient(
    api_key="your-euri-api-key",
    model="gemini-2.5-flash"
)

response = client.generate_completion(
    prompt="What is artificial intelligence?",
    temperature=0.7,
    max_tokens=1000
)

print(response["choices"][0]["message"]["content"])


# ── With Different Models ────────────────────────────────────────────

# Fast & cheap
fast_client = EuriaiClient(api_key="your-key", model="gpt-4.1-nano")

# Smart & powerful
smart_client = EuriaiClient(api_key="your-key", model="gemini-2.5-pro")

# Web search capable
search_client = EuriaiClient(api_key="your-key", model="groq/compound")


# ── Raw HTTP (no SDK needed) ─────────────────────────────────────────

import requests

response = requests.post(
    "https://api.euron.one/api/v1/euri/chat/completions",
    headers={
        "Authorization": "Bearer your-euri-api-key",
        "Content-Type": "application/json",
    },
    json={
        "model": "gemini-2.5-flash",
        "messages": [{"role": "user", "content": "Hello!"}],
        "temperature": 0.7,
        "max_tokens": 500,
    },
)

data = response.json()
print(data["choices"][0]["message"]["content"])


# ── With LangChain ───────────────────────────────────────────────────
# pip install euriai[langchain]

# from euriai.langchain import EuriaiChatModel
# chat = EuriaiChatModel(api_key="your-key", model="gemini-2.5-flash")
# result = chat.invoke("Explain Docker")
# print(result.content)
