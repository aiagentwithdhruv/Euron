# MCP Setup Guide — Connect AI to Real Tools

> **From Euron Live Class: Claude Code + MCP**
> By Dhruv Tomar ([AIwithDhruv](https://linkedin.com/in/aiwithdhruv))

---

## What You'll Build

By the end of this guide, your AI will be able to:
- Read your emails
- Create Google Sheets
- Query databases
- Run any custom Python function

All through natural chat — no API calls, no Postman, no code.

---

## What is MCP?

**MCP = Model Context Protocol**

Think of it like a **USB port for AI**.

```
Without MCP:
  You → "Send email" → AI → "Here's how you would send an email..." (just text)

With MCP:
  You → "Send email" → AI → [uses Gmail tool] → Email actually sent!
```

MCP lets AI **do things**, not just **talk about things**.

---

## Setup (3 Options — Pick One)

### Option A: Claude Desktop (Easiest)

**Best for:** Quick tasks, non-developers, trying MCP for the first time.

1. Download Claude Desktop from [claude.ai](https://claude.ai)
2. Install it
3. That's it — continue to "Build Your First MCP Server" below

### Option B: Claude Code (Terminal)

**Best for:** Developers who love the terminal.

```bash
npm install -g @anthropic-ai/claude-code
claude
```

### Option C: Cursor / VS Code

**Best for:** Developers who want MCP inside their IDE.

1. Download [Cursor](https://cursor.com) or install Claude Code extension in VS Code
2. Open any project folder
3. Continue to "Build Your First MCP Server" below

---

## Build Your First MCP Server (5 minutes)

### Step 1: Install FastMCP

```bash
pip install "mcp[cli]"
```

### Step 2: Create the Server

Create a file called `hello_mcp.py`:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("HelloWorld")

@mcp.tool()
def greet(name: str) -> str:
    """Say hello to someone by name"""
    return f"Hello, {name}! You're connected to MCP!"

@mcp.tool()
def add_numbers(a: int, b: int) -> str:
    """Add two numbers together"""
    return f"{a} + {b} = {a + b}"

@mcp.tool()
def current_time() -> str:
    """Get the current date and time"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

mcp.run(transport="stdio")
```

**That's your MCP server.** 3 tools. 20 lines.

### Step 3: Connect It

Find your config file:

| Platform | Config File |
|----------|-------------|
| Claude Desktop (Mac) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `.cursor/mcp.json` (in project root) |
| Claude Code | `.claude/settings.local.json` (in project root) |

Add this (replace the path with YOUR actual path):

```json
{
  "mcpServers": {
    "HelloWorld": {
      "command": "python3",
      "args": ["/full/path/to/hello_mcp.py"]
    }
  }
}
```

### Step 4: Test It

Restart Claude Desktop (or reload Cursor). Then chat:

```
"Say hello to Dhruv"
```

You should see Claude use the `greet` tool and respond with "Hello, Dhruv! You're connected to MCP!"

```
"What time is it?"
```

Claude uses the `current_time` tool. Real time. Not hallucinated.

```
"What is 42 + 58?"
```

Claude uses `add_numbers` instead of calculating itself. Provably correct.

---

## Level Up: Gmail MCP Server

Once your hello world works, try connecting to real Gmail.

### Step 1: Google Cloud Setup (One Time)

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (name it anything)
3. Go to "APIs & Services" → "Enable APIs"
4. Enable **Gmail API**
5. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
6. Application type: **Desktop app**
7. Download the JSON → save as `credentials.json`

### Step 2: Create Gmail MCP Server

Create `gmail_mcp.py`:

```python
import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Gmail")

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

@mcp.tool()
def read_recent_emails(limit: int = 5) -> str:
    """Read recent emails from Gmail inbox"""
    service = get_gmail_service()
    results = service.users().messages().list(userId="me", maxResults=limit).execute()
    messages = results.get("messages", [])
    output = []
    for msg in messages:
        detail = service.users().messages().get(userId="me", id=msg["id"], format="metadata").execute()
        headers = {h["name"]: h["value"] for h in detail["payload"]["headers"]}
        output.append(f"From: {headers.get('From', '?')} | Subject: {headers.get('Subject', '?')}")
    return "\n".join(output) if output else "No emails found"

@mcp.tool()
def send_email(to_email: str, subject: str, body: str) -> str:
    """Send an email via Gmail"""
    service = get_gmail_service()
    message = MIMEText(body)
    message["to"] = to_email
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    return f"Email sent to {to_email}"

mcp.run(transport="stdio")
```

### Step 3: Install Dependencies

```bash
pip install "mcp[cli]" google-auth google-auth-oauthlib google-api-python-client
```

### Step 4: Authenticate (One Time)

```bash
python gmail_mcp.py
# First run opens browser → sign in → authorize → token.json saved
```

Actually, create a separate `authenticate.py` for first-time auth:

```python
from google_auth_oauthlib.flow import InstalledAppFlow
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)
with open("token.json", "w") as f:
    f.write(creds.to_json())
print("Authentication complete! token.json saved.")
```

Run it: `python authenticate.py`

### Step 5: Add to Config

```json
{
  "mcpServers": {
    "Gmail": {
      "command": "python3",
      "args": ["/full/path/to/gmail_mcp.py"]
    }
  }
}
```

### Step 6: Test

Restart Claude Desktop. Then:

```
"Read my last 3 emails"
```

Real emails appear. In your AI chat. Magic.

---

## How It All Connects (The Big Picture)

```
YOU
 "Read my emails and save them to a spreadsheet"
    |
    v
CLAUDE (Desktop / Code / Cursor)
    |
    |-- uses Gmail MCP --> reads 5 emails
    |-- uses Sheets MCP --> creates spreadsheet
    |-- uses Sheets MCP --> writes email data
    |
    v
DONE (3 tools, 1 instruction, 0 code)
```

---

## Exercise: Build Your Own MCP Server

Pick one:

### Option 1: Calculator Server (Beginner)
Build a server with: `add`, `subtract`, `multiply`, `divide`, `percentage`

### Option 2: File Manager Server (Intermediate)
Build a server with: `list_files` (in a directory), `read_file`, `file_info` (size, modified date)

### Option 3: Weather Server (Intermediate)
Build a server that fetches weather from [open-meteo.com](https://open-meteo.com) (free, no API key):
```python
import requests

@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city"""
    # Geocode city → get lat/lon → fetch weather
    geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1").json()
    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    weather = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()
    w = weather["current_weather"]
    return f"{city}: {w['temperature']}C, wind {w['windspeed']} km/h"
```

### Submit
Share a screenshot of your MCP server working in the WhatsApp group!

---

## Common Issues

| Problem | Fix |
|---------|-----|
| "Server not found" | Check the path in config is **absolute** (not relative) |
| "Permission denied" | Make sure `python3` path is correct: run `which python3` |
| Server doesn't show up | Restart Claude Desktop completely (quit + reopen) |
| "No module named mcp" | Run `pip install "mcp[cli]"` in the correct environment |
| Google auth fails | Delete `token.json` and re-run `authenticate.py` |
| Config syntax error | Validate JSON at [jsonlint.com](https://jsonlint.com) |

---

## Resources

| Resource | Link |
|----------|------|
| MCP Spec (Official) | [modelcontextprotocol.io](https://modelcontextprotocol.io) |
| FastMCP Docs | [github.com/jlowin/fastmcp](https://github.com/jlowin/fastmcp) |
| Claude Desktop | [claude.ai](https://claude.ai) |
| Claude Code | `npm install -g @anthropic-ai/claude-code` |
| Cursor IDE | [cursor.com](https://cursor.com) |
| Our MCP Servers (8) | `Euron/Gen-AI-2.O/MCP/` |
| Full Setup Guide | `Euron/MAIL-MCP-SETUP.md` |

---

## What's Next (Day 2)

- Deploy MCP servers to the cloud
- Triggers and webhooks (run automation 24/7)
- Error handling and retry logic
- GitHub → production pipeline

---

*Built for Euron Live Class by [AIwithDhruv](https://linkedin.com/in/aiwithdhruv)*
