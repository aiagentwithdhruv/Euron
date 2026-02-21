# Email Automation MCP Server

> Control your Gmail entirely from AI chat — read, send, search, and manage emails without opening your inbox.

Built with **Python**, **FastMCP**, and the **Gmail API** (OAuth 2.0). Functional programming style — no classes.

---

## Tools

| Tool | Description | Key Parameters |
|------|-------------|---------------|
| `send_email` | Send an email to anyone | `to_email`, `subject`, `body` |
| `read_recent_emails` | Fetch latest emails | `limit`, `query` |
| `search_emails` | Search using Gmail syntax | `query`, `limit` |
| `mark_email_seen` | Mark emails as read | `query` |

---

## Quick Start (5 Steps)

**Full detailed guide with screenshots-level detail:** [**MAIL-MCP-SETUP.md**](../../MAIL-MCP-SETUP.md)

```bash
# 1. Get credentials.json from Google Cloud Console (OAuth Desktop Client)
#    Save it in this folder as credentials.json

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate & install
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows
pip install -r requirements.txt

# 4. Authenticate (one-time browser login)
python authenticate.py

# 5. Add to Claude Desktop / Cursor config (see below)
```

---

## Config Snippets

Add this to your Claude Desktop or Cursor MCP config. Use **absolute paths** for your system.

### Claude Desktop

**File:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
"EmailAutomation": {
  "command": "/ABSOLUTE/PATH/TO/venv/bin/python",
  "args": ["/ABSOLUTE/PATH/TO/email_mcp.py"]
}
```

### Cursor

**File:** `~/.cursor/mcp.json`

```json
"EmailAutomation": {
  "command": "/ABSOLUTE/PATH/TO/venv/bin/python",
  "args": ["/ABSOLUTE/PATH/TO/email_mcp.py"]
}
```

Then restart Claude Desktop (Cmd+Q → Reopen) or reload Cursor (Cmd+Shift+P → Reload Window).

---

## Important Notes

- Server runs with **stdio** transport (`mcp.run(transport="stdio")`)
- Config must point directly to `email_mcp.py` — do **not** use `-m mcp run`
- **Never commit** `credentials.json`, `token.json`, or `venv/` to Git

---

## Files

| File | What | Git? |
|------|------|------|
| `email_mcp.py` | MCP server (4 tools) | Yes |
| `authenticate.py` | OAuth browser flow | Yes |
| `requirements.txt` | Dependencies | Yes |
| `credentials.json` | Google Cloud secret | No |
| `token.json` | Auth session | No |
| `venv/` | Virtual env | No |

---

*Part of the [Euron](https://github.com/aiagentwithdhruv/Euron) project. See [MAIL-MCP-SETUP.md](../../MAIL-MCP-SETUP.md) for the complete setup guide.*
