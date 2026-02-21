# Mail MCP Setup — Complete Guide

A step-by-step guide to set up the **Email Automation MCP** (Model Context Protocol) server so you can read, send, search, and manage Gmail directly from **Claude Desktop** and **Cursor** — no need to open your inbox.

---

## Table of Contents

1. [Overview](#1-overview)
2. [What You Get](#2-what-you-get)
3. [Prerequisites](#3-prerequisites)
4. [Step 1: Google Cloud Credentials](#4-step-1-google-cloud-credentials)
5. [Step 2: Local Project Setup](#5-step-2-local-project-setup)
6. [Step 3: One-Time Authentication](#6-step-3-one-time-authentication)
7. [Step 4: Claude Desktop Setup](#7-step-4-claude-desktop-setup)
8. [Step 5: Cursor Setup](#8-step-5-cursor-setup)
9. [Using the Tools](#9-using-the-tools)
10. [Troubleshooting](#10-troubleshooting)
11. [Project Structure](#11-project-structure)

---

## 1. Overview

This MCP server uses:

- **Python** and the **FastMCP** library
- **Gmail API** via **Google Cloud OAuth 2.0** (no app passwords)
- **Functional style** (no classes); all logic in plain functions

Once set up, Claude or Cursor can manage your Gmail from chat: read recent mail, send messages, search, and mark as read.

---

## 2. What You Get

| Tool | Description |
|------|-------------|
| **Read recent emails** | Fetch the latest N emails, optionally filtered by Gmail query |
| **Send email** | Compose and send an email to any address |
| **Search emails** | Search using Gmail syntax (`from:`, `subject:`, `is:unread`, etc.) |
| **Mark as read** | Mark messages matching a query as read (remove UNREAD label) |

---

## 3. Prerequisites

- **Python 3.9+** installed
- A **Google account** (Gmail)
- **Claude Desktop** and/or **Cursor** installed
- Terminal (or Cursor integrated terminal) access

---

## 4. Step 1: Google Cloud Credentials

You need an OAuth 2.0 **Desktop** client so the MCP can access Gmail on your behalf.

### 4.1 Create or select a project

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a **new project** or select an existing one.

### 4.2 Enable Gmail API

1. Open **APIs & Services** → **Library**.
2. Search for **Gmail API**.
3. Open it and click **Enable**.

### 4.3 Create OAuth client ID

1. Go to **APIs & Services** → **Credentials**.
2. Click **Create Credentials** → **OAuth client ID**.
3. If asked, configure the **OAuth consent screen** (External, add your email as test user).
4. Application type: **Desktop app**.
5. Name it (e.g. `Mail MCP`) and click **Create**.
6. Click **Download JSON** (or copy Client ID and Client Secret).

### 4.4 Add credentials to the project

1. Clone or copy the **Mail MCP** folder (e.g. `Gen AI 2.O/MCP`) to your machine.
2. Rename the downloaded JSON file to **`credentials.json`**.
3. Place `credentials.json` **inside the MCP folder** (same directory as `email_mcp.py`).

> **Security:** Do **not** commit `credentials.json` or `token.json` to Git. Add them to `.gitignore` (see [Project Structure](#11-project-structure)).

---

## 5. Step 2: Local Project Setup

All commands below assume you are inside the MCP folder (e.g. `Gen AI 2.O/MCP`).

### 5.1 Create a virtual environment

```bash
cd "Gen AI 2.O/MCP"   # or your actual path
python3 -m venv venv
```

### 5.2 Activate the virtual environment

- **macOS/Linux:** `source venv/bin/activate`
- **Windows:** `venv\Scripts\activate`

### 5.3 Install dependencies

```bash
pip install -r requirements.txt
```

Required packages (already in `requirements.txt`):

- `mcp[cli]` — MCP server and CLI
- `google-api-python-client` — Gmail API client
- `google-auth-httplib2` — Auth for HTTP
- `google-auth-oauthlib` — OAuth 2.0 flow

---

## 6. Step 3: One-Time Authentication

The first time (and when the token expires), you must log in in the browser. After that, the server uses `token.json` and refreshes it automatically.

### 6.1 Run the auth script

From the MCP folder, with `venv` activated:

```bash
python authenticate.py
```

### 6.2 Complete the browser flow

1. A browser window opens with the Google sign-in page.
2. Choose the **Gmail account** you want the MCP to use.
3. If you see “Google hasn’t verified this app”, click **Advanced** → **Go to … (unsafe)**.
4. Grant access to **view and manage your email**.
5. When you see “The authentication flow has completed”, you can close the tab.

### 6.3 Verify

- A file **`token.json`** should appear in the MCP folder.
- The script prints a success message. The MCP server will use this token and refresh it when needed.

---

## 7. Step 4: Claude Desktop Setup

Claude Desktop talks to the MCP over **stdio**. The server must run with `transport="stdio"` (this is already set in `email_mcp.py`).

### 7.1 Locate the config file

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

### 7.2 Add the EmailAutomation server

Open `claude_desktop_config.json` and add an entry under `mcpServers`. Use **absolute paths** for your machine.

**macOS example:**

```json
{
  "mcpServers": {
    "EmailAutomation": {
      "command": "/full/path/to/Gen AI 2.O/MCP/venv/bin/python",
      "args": [
        "/full/path/to/Gen AI 2.O/MCP/email_mcp.py"
      ]
    }
  }
}
```

**Windows example** (adjust paths):

```json
{
  "mcpServers": {
    "EmailAutomation": {
      "command": "C:\\path\\to\\Gen AI 2.O\\MCP\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\path\\to\\Gen AI 2.O\\MCP\\email_mcp.py"
      ]
    }
  }
}
```

- **command:** Python interpreter inside the project’s `venv`.
- **args:** Single argument: full path to `email_mcp.py`.
- No `env` needed; credentials come from `credentials.json` and `token.json` in the MCP folder.

### 7.3 Restart Claude Desktop

Quit the app completely (e.g. Cmd+Q on macOS), then reopen it. The “MCP EmailAutomation: Server disconnected” error should go away once the server starts correctly with stdio.

---

## 8. Step 5: Cursor Setup

### 8.1 Locate the MCP config

- **macOS/Linux:** `~/.cursor/mcp.json`
- **Windows:** `%USERPROFILE%\.cursor\mcp.json`

### 8.2 Add the EmailAutomation server

Same structure as Claude Desktop: `command` = venv Python, `args` = path to `email_mcp.py`.

**Example (macOS):**

```json
{
  "mcpServers": {
    "EmailAutomation": {
      "command": "/full/path/to/Gen AI 2.O/MCP/venv/bin/python",
      "args": [
        "/full/path/to/Gen AI 2.O/MCP/email_mcp.py"
      ]
    }
  }
}
```

### 8.3 Reload Cursor

- **Cmd+Shift+P** (or Ctrl+Shift+P) → **“Reload Window”** → Enter.

Then check **Cursor Settings → MCP**; EmailAutomation should show as connected.

---

## 9. Using the Tools

Once the MCP is connected in Claude or Cursor, you can say things like:

- *“What are my last 5 emails?”*
- *“Read my last 4 emails.”*
- *“Send an email to john@example.com with subject ‘Hello’ and body ‘Hi from MCP.’”*
- *“Search for unread emails from support@company.com.”*
- *“Mark all unread emails from newsletters as read.”*

Search uses **Gmail query syntax**, e.g.:

- `from:someone@example.com`
- `subject:meeting`
- `is:unread`
- `after:2026/01/01`

---

## 10. Troubleshooting

### “MCP EmailAutomation: Server disconnected” (Claude Desktop)

- The server must use **stdio** transport. In `email_mcp.py`, the main block should be:
  ```python
  if __name__ == "__main__":
      mcp.run(transport="stdio")
  ```
- Config must run the script **directly** with the venv Python, e.g.:
  - `"command": "/path/to/venv/bin/python"`
  - `"args": ["/path/to/email_mcp.py"]`
- No `-m mcp run` in `args` when using stdio from Claude.

### “Authentication token missing or invalid”

- Run `python authenticate.py` again from the MCP folder (with venv activated).
- Ensure `credentials.json` is in the same folder as `email_mcp.py` and `authenticate.py`.

### “Failed to refresh token”

- Delete `token.json` and run `python authenticate.py` again to re-authorize.

### Cursor: MCP shows as errored

- Confirm paths in `~/.cursor/mcp.json` are absolute and point to the same venv and `email_mcp.py`.
- Reload the window (Cmd+Shift+P → Reload Window).

### Gmail API errors (e.g. quota, disabled)

- In Google Cloud Console, ensure **Gmail API** is enabled for the project.
- Check that the OAuth consent screen is configured and your user is added as a test user if the app is in “Testing”.

---

## 11. Project Structure

```
Gen AI 2.O/MCP/
├── email_mcp.py        # MCP server (run with transport="stdio")
├── authenticate.py     # One-time OAuth flow → creates token.json
├── credentials.json    # From Google Cloud (do not commit)
├── token.json          # From authenticate.py (do not commit)
├── requirements.txt   # Python dependencies
├── README.md           # Short reference in the folder
└── venv/               # Virtual environment (do not commit)
```

### Suggested .gitignore (repo or MCP folder)

```gitignore
# Mail MCP — keep secrets and venv out of Git
Gen AI 2.O/MCP/credentials.json
Gen AI 2.O/MCP/token.json
Gen AI 2.O/MCP/venv/
```

Or inside `Gen AI 2.O/MCP/.gitignore`:

```gitignore
credentials.json
token.json
venv/
```

---

## Quick Reference: Config Snippets

**Claude Desktop** (`claude_desktop_config.json`):

```json
"EmailAutomation": {
  "command": "/ABSOLUTE/PATH/TO/venv/bin/python",
  "args": ["/ABSOLUTE/PATH/TO/email_mcp.py"]
}
```

**Cursor** (`~/.cursor/mcp.json`):

```json
"EmailAutomation": {
  "command": "/ABSOLUTE/PATH/TO/venv/bin/python",
  "args": ["/ABSOLUTE/PATH/TO/email_mcp.py"]
}
```

Replace `/ABSOLUTE/PATH/TO/` with your actual path to the MCP folder (e.g. `.../Euron/Gen AI 2.O/MCP/`).

---

*This guide is part of the Euron project. For the in-folder summary, see `Gen AI 2.O/MCP/README.md`.*
