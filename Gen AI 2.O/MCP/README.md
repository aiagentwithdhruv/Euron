# Email Automation MCP Server

MCP server for Gmail: read, send, search, and mark emails as read from **Claude Desktop** and **Cursor** via chat. Uses Gmail API and Google Cloud OAuth 2.0; implementation is functional (no classes).

## Quick links

- **Full setup guide:** [MAIL-MCP-SETUP.md](../../MAIL-MCP-SETUP.md) (in repo root) — follow this for first-time setup.
- **Tools:** `read_recent_emails`, `send_email`, `search_emails`, `mark_email_seen`.

## One-minute summary

1. Put **Google OAuth Desktop** client JSON in this folder as `credentials.json`.
2. `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
3. Run once: `python authenticate.py` (browser login → creates `token.json`).
4. Add **EmailAutomation** to Claude Desktop and/or Cursor config (see [MAIL-MCP-SETUP.md](../../MAIL-MCP-SETUP.md)).
5. Restart Claude / Reload Cursor.

**Important:** Server must run with **stdio** transport. In `email_mcp.py`, the main block is `mcp.run(transport="stdio")`. Config must run the script directly with venv Python, e.g. `"args": ["/path/to/email_mcp.py"]`.

Do **not** commit `credentials.json`, `token.json`, or `venv/`.
