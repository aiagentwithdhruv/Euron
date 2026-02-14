# Euri API in n8n - HTTP Request Node Config

## Chat Completions

**HTTP Request Node Settings:**
- Method: `POST`
- URL: `https://api.euron.one/api/v1/euri/chat/completions`
- Authentication: None (use header below)
- Headers:
  - `Authorization`: `Bearer {{ $env.EURI_API_KEY }}`
  - `Content-Type`: `application/json`
- Body (JSON):
```json
{
  "model": "gemini-2.5-flash",
  "messages": [
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "{{ $json.userMessage }}" }
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```
- Extract response: `{{ $json.choices[0].message.content }}`

## Embeddings

- Method: `POST`
- URL: `https://api.euron.one/api/v1/euri/embeddings`
- Body:
```json
{
  "model": "gemini-embedding-001",
  "input": "{{ $json.textToEmbed }}"
}
```
- Extract: `{{ $json.data[0].embedding }}`

## Image Generation

- Method: `POST`
- URL: `https://api.euron.one/api/v1/euri/images/generations`
- Body:
```json
{
  "model": "gemini-3-pro-image-preview",
  "prompt": "{{ $json.imagePrompt }}",
  "n": 1
}
```
- Extract: `{{ $json.data[0].url }}`

## n8n Code Node (JavaScript)

```javascript
const response = await $http.request({
  method: 'POST',
  url: 'https://api.euron.one/api/v1/euri/chat/completions',
  headers: {
    'Authorization': `Bearer ${$env.EURI_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: {
    model: 'gemini-2.5-flash',
    messages: [
      { role: 'user', content: $input.first().json.prompt }
    ],
    temperature: 0.7,
    max_tokens: 1000,
  },
  json: true,
});

return [{ json: { response: response.choices[0].message.content } }];
```

## OpenAI-Compatible Credential in n8n

Since Euri is OpenAI-compatible, you can use n8n's built-in OpenAI credential:
1. Create "OpenAI" credential in n8n
2. Set API Key: your Euri API key
3. Set Base URL: `https://api.euron.one/api/v1/euri`
4. Use any OpenAI node — it will route through Euri
