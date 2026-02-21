# Mail MCP — Build Your Own Email Automation with AI

> **Control your Gmail entirely from Claude Desktop or Cursor.**
> Read, send, search, and manage emails — all from chat. Zero inbox visits.

---

## What is This?

This project is a **Model Context Protocol (MCP)** server written in Python that connects your Gmail account to AI tools like **Claude Desktop** and **Cursor IDE**.

Once configured, you can literally type:
- *"Show me my last 5 emails"*
- *"Send an email to john@example.com about the meeting"*
- *"Find all unread emails from GitHub"*
- *"Mark all newsletter emails as read"*

...and the AI does it for you instantly.

### How It Works (Architecture)

```
You (Chat)
   |
   v
Claude Desktop / Cursor
   |
   v  (MCP Protocol over stdio)
Email MCP Server (Python + FastMCP)
   |
   v  (OAuth 2.0)
Gmail API (Google Cloud)
   |
   v
Your Gmail Inbox
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Client | Claude Desktop / Cursor IDE |
| Protocol | MCP (Model Context Protocol) via stdio |
| Server | Python + FastMCP library |
| Email API | Gmail API (Google Cloud) |
| Auth | OAuth 2.0 Desktop Client (no app passwords!) |
| Style | Functional programming (no classes) |

---

## Available Tools

| # | Tool Name | What It Does | Parameters |
|---|-----------|-------------|------------|
| 1 | `send_email` | Send an email to anyone | `to_email`, `subject`, `body` |
| 2 | `read_recent_emails` | Fetch latest N emails | `limit` (default: 5), `query` (optional) |
| 3 | `search_emails` | Search with Gmail syntax | `query`, `limit` (default: 5) |
| 4 | `mark_email_seen` | Mark matching emails as read | `query` |

---

## Prerequisites

Before you start, make sure you have:

- [ ] **Python 3.9+** installed ([Download](https://www.python.org/downloads/))
- [ ] A **Gmail account**
- [ ] **Claude Desktop** ([Download](https://claude.ai/download)) and/or **Cursor IDE** ([Download](https://cursor.com))
- [ ] Access to [Google Cloud Console](https://console.cloud.google.com/)
- [ ] A terminal / command line

---

## Step-by-Step Setup

### Step 1 of 5 — Google Cloud Credentials

You need to create an OAuth 2.0 client so the MCP server can access Gmail securely on your behalf. This is a one-time setup.

#### 1A. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown (top-left) → **New Project**
3. Name it something like `Mail MCP` → **Create**
4. Make sure your new project is selected in the dropdown

#### 1B. Enable the Gmail API

1. In the left sidebar: **APIs & Services** → **Library**
2. Search for **Gmail API**
3. Click on it → **Enable**

#### 1C. Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Choose **External** → **Create**
3. Fill in:
   - App name: `Mail MCP`
   - User support email: *your email*
   - Developer contact email: *your email*
4. Click **Save and Continue** through the remaining steps
5. Under **Test users**, click **Add Users** → add your Gmail address
6. **Save and Continue** → **Back to Dashboard**

#### 1D. Create OAuth Client ID

1. Go to **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: `Mail MCP` (or anything)
5. Click **Create**
6. A dialog shows your **Client ID** and **Client Secret** — copy both or click **Download JSON**

#### 1E. Save Credentials

**Option A — Downloaded JSON file:**
- Rename the file to `credentials.json`
- Place it inside the MCP project folder (same directory as `email_mcp.py`)

**Option B — Manual (if you copied Client ID and Secret):**
- Create a file called `credentials.json` in the MCP folder with this structure:

```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID_HERE",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET_HERE",
    "redirect_uris": ["http://localhost"]
  }
}
```

> **Security Warning:** Never commit `credentials.json` or `token.json` to Git. The included `.gitignore` already handles this.

---

### Step 2 of 5 — Project Setup (Python Environment)

Open a terminal and navigate to the MCP folder.

#### 2A. Clone the repo (if you haven't)

```bash
git clone https://github.com/aiagentwithdhruv/Euron.git
cd "Euron/Gen AI 2.O/MCP"
```

#### 2B. Create a virtual environment

```bash
python3 -m venv venv
```

#### 2C. Activate the virtual environment

| OS | Command |
|----|---------|
| macOS / Linux | `source venv/bin/activate` |
| Windows (CMD) | `venv\Scripts\activate` |
| Windows (PowerShell) | `venv\Scripts\Activate.ps1` |

You should see `(venv)` in your terminal prompt after activation.

#### 2D. Install dependencies

```bash
pip install -r requirements.txt
```

This installs:

| Package | Purpose |
|---------|---------|
| `mcp[cli]` | FastMCP server framework and CLI tools |
| `google-api-python-client` | Official Google API client for Gmail |
| `google-auth-httplib2` | HTTP transport for Google Auth |
| `google-auth-oauthlib` | OAuth 2.0 browser-based login flow |

---

### Step 3 of 5 — One-Time Authentication

Before the MCP server can run in the background, you need to authorize it once through your browser. After this, it stores a `token.json` that auto-refreshes.

#### 3A. Run the authentication script

Make sure venv is activated, then:

```bash
python authenticate.py
```

#### 3B. Complete the browser login

1. A browser window opens automatically with Google Sign-In
2. Select the **Gmail account** you want the MCP to manage
3. You may see a warning: *"Google hasn't verified this app"*
   - Click **Advanced** → **Go to Mail MCP (unsafe)**
   - This is normal for personal OAuth apps
4. Click **Allow** to grant Gmail access
5. You'll see: *"The authentication flow has completed. You may close this window."*

#### 3C. Verify it worked

Check that `token.json` now exists in your MCP folder:

```bash
ls token.json
```

You should also see in your terminal:

```
Authentication successful!
token.json has been generated or refreshed.
```

#### 3D. Quick test (optional)

Verify the connection to Gmail works:

```bash
python -c "
from email_mcp import get_gmail_service
service = get_gmail_service()
results = service.users().messages().list(userId='me', maxResults=1).execute()
print(f'Connection OK! Found {len(results.get(\"messages\", []))} message(s).')
"
```

---

### Step 4 of 5 — Claude Desktop Configuration

#### 4A. Locate the config file

| OS | Path |
|----|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

#### 4B. Add the EmailAutomation MCP server

Open the config file in any editor and add the `EmailAutomation` entry under `mcpServers`.

**macOS example:**

```json
{
  "mcpServers": {
    "EmailAutomation": {
      "command": "/ABSOLUTE/PATH/TO/Euron/Gen AI 2.O/MCP/venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/Euron/Gen AI 2.O/MCP/email_mcp.py"
      ]
    }
  }
}
```

**Windows example:**

```json
{
  "mcpServers": {
    "EmailAutomation": {
      "command": "C:\\Users\\YOU\\Euron\\Gen AI 2.O\\MCP\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YOU\\Euron\\Gen AI 2.O\\MCP\\email_mcp.py"
      ]
    }
  }
}
```

> **Key points:**
> - `command` = the Python binary **inside the venv** (not your system Python)
> - `args` = single item: the **absolute path** to `email_mcp.py`
> - No `env` block needed — credentials are read from `credentials.json` and `token.json` in the same folder
> - No `-m mcp run` — the script handles stdio transport directly

#### 4C. Restart Claude Desktop

- **macOS:** Cmd+Q → Reopen
- **Windows:** Close completely from system tray → Reopen

The MCP should now show as connected. If you see errors, check [Troubleshooting](#troubleshooting).

---

### Step 5 of 5 — Cursor IDE Configuration

#### 5A. Locate the config file

| OS | Path |
|----|------|
| macOS / Linux | `~/.cursor/mcp.json` |
| Windows | `%USERPROFILE%\.cursor\mcp.json` |

#### 5B. Add the EmailAutomation MCP server

Same structure as Claude Desktop:

```json
{
  "mcpServers": {
    "EmailAutomation": {
      "command": "/ABSOLUTE/PATH/TO/Euron/Gen AI 2.O/MCP/venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/Euron/Gen AI 2.O/MCP/email_mcp.py"
      ]
    }
  }
}
```

#### 5C. Reload Cursor

- Press **Cmd+Shift+P** (macOS) or **Ctrl+Shift+P** (Windows/Linux)
- Type **Reload Window** → Enter
- Go to **Cursor Settings → MCP** to verify EmailAutomation shows green

---

## Usage Examples

Once the MCP is connected, just chat naturally:

### Reading Emails

| Prompt | What happens |
|--------|-------------|
| *"What are my last 5 emails?"* | Fetches the 5 most recent emails with sender, subject, date, and body preview |
| *"Show me unread emails"* | Uses query `is:unread` to filter |
| *"Read emails from GitHub"* | Uses query `from:github.com` |

### Sending Emails

| Prompt | What happens |
|--------|-------------|
| *"Send an email to john@example.com about our meeting tomorrow"* | Composes and sends with AI-generated subject and body |
| *"Email sarah@company.com — subject: Invoice, body: Please find attached."* | Sends exactly as specified |

### Searching Emails

Uses standard **Gmail search syntax** — same queries you'd type in Gmail's search bar:

| Query Syntax | Meaning |
|-------------|---------|
| `from:boss@example.com` | Emails from a specific sender |
| `subject:meeting` | Emails with "meeting" in the subject |
| `is:unread` | All unread emails |
| `is:unread in:inbox` | Unread emails in inbox only |
| `after:2026/01/01` | Emails after a specific date |
| `has:attachment` | Emails with attachments |
| `from:amazon.com subject:order` | Combined filters |

### Managing Emails

| Prompt | What happens |
|--------|-------------|
| *"Mark all newsletter emails as read"* | Finds unread newsletter emails and removes the UNREAD label |
| *"Mark emails from noreply@medium.com as read"* | Marks all matching unread emails as seen |

---

## Troubleshooting

### "MCP EmailAutomation: Server disconnected" (Claude Desktop)

**Cause:** The server isn't using stdio transport, or the config is wrong.

**Fix:**
1. In `email_mcp.py`, verify the last line is:
   ```python
   mcp.run(transport="stdio")
   ```
2. In `claude_desktop_config.json`, the config should NOT use `-m mcp run`. It should directly run the script:
   ```json
   "command": "/path/to/venv/bin/python",
   "args": ["/path/to/email_mcp.py"]
   ```
3. Restart Claude Desktop completely (Cmd+Q → Reopen)

### "Authentication token missing or invalid"

**Cause:** `token.json` doesn't exist or is corrupted.

**Fix:**
```bash
cd "path/to/Gen AI 2.O/MCP"
source venv/bin/activate
python authenticate.py
```

### "Failed to refresh token"

**Cause:** The refresh token has expired or been revoked.

**Fix:**
```bash
rm token.json
python authenticate.py
```

### Cursor MCP shows as errored

**Fix:**
1. Verify paths in `~/.cursor/mcp.json` are **absolute** paths
2. Ensure the venv Python and `email_mcp.py` paths match your actual file locations
3. Reload: Cmd+Shift+P → **Reload Window**

### Gmail API errors (quota, disabled, etc.)

**Fix:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/) → **APIs & Services** → **Dashboard**
2. Verify **Gmail API** is enabled
3. Check **OAuth consent screen** → your email is listed as a test user
4. If app is in "Testing" mode, only test users can authenticate

### "Google hasn't verified this app" warning during auth

**This is normal.** Since you created the OAuth client yourself, Google shows this warning. Click **Advanced** → **Go to [App Name] (unsafe)** to proceed. This is safe because you are the owner of both the app and the Gmail account.

---

## Project Structure

```
Gen AI 2.O/MCP/
│
├── email_mcp.py          # MCP server — 4 tools, runs with stdio transport
├── authenticate.py       # One-time OAuth flow — creates token.json
├── requirements.txt      # Python dependencies
├── README.md             # Quick reference (points here)
├── .gitignore            # Keeps secrets out of Git
│
├── credentials.json      # YOUR Google Cloud OAuth client (do NOT commit)
├── token.json            # Generated by authenticate.py (do NOT commit)
└── venv/                 # Python virtual environment (do NOT commit)
```

### What each file does

| File | Purpose | Commit to Git? |
|------|---------|---------------|
| `email_mcp.py` | The MCP server with all 4 email tools | Yes |
| `authenticate.py` | Runs the Google OAuth browser flow once | Yes |
| `requirements.txt` | Lists Python package dependencies | Yes |
| `README.md` | Quick summary with link to this guide | Yes |
| `.gitignore` | Prevents committing secrets | Yes |
| `credentials.json` | Your Google Cloud OAuth secret | **No** |
| `token.json` | Your personal auth session token | **No** |
| `venv/` | Isolated Python environment | **No** |

---

## Quick Reference — Config Snippets

Copy-paste these into your config files. Replace the paths with your actual absolute paths.

### Claude Desktop (`claude_desktop_config.json`)

```json
"EmailAutomation": {
  "command": "/YOUR/PATH/TO/venv/bin/python",
  "args": ["/YOUR/PATH/TO/email_mcp.py"]
}
```

### Cursor (`~/.cursor/mcp.json`)

```json
"EmailAutomation": {
  "command": "/YOUR/PATH/TO/venv/bin/python",
  "args": ["/YOUR/PATH/TO/email_mcp.py"]
}
```

---

## About

Built as part of the **Euron AI Automation Bootcamp** — demonstrating how to build production-ready MCP servers that connect AI assistants to real-world services using functional Python.

**Repository:** [github.com/aiagentwithdhruv/Euron](https://github.com/aiagentwithdhruv/Euron)

*For the in-folder quick reference, see [`Gen AI 2.O/MCP/README.md`](Gen%20AI%202.O/MCP/README.md).*
