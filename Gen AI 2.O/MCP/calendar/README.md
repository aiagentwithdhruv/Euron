# Google Calendar MCP Server

> Manage your Google Calendar entirely from AI chat — list, create, search, and delete events without opening your browser.

Built with **Python**, **FastMCP**, and the **Google Calendar API** (OAuth 2.0). Functional programming style — no classes.

---

## Tools

| Tool | Description | Key Parameters |
|------|-------------|---------------|
| `list_events` | List upcoming events | `limit`, `days_ahead` |
| `create_event` | Create a new event | `summary`, `start_datetime`, `end_datetime`, `description`, `location` |
| `search_events` | Search events by text | `query`, `limit` |
| `delete_event` | Delete an event by ID | `event_id` |
| `get_todays_schedule` | Get all events for today | — |

---

## Quick Start (5 Steps)

```bash
# 1. Get credentials.json from Google Cloud Console (OAuth Desktop Client)
#    Enable the Google Calendar API and save the file in this folder

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
"GoogleCalendar": {
  "command": "/ABSOLUTE/PATH/TO/venv/bin/python",
  "args": ["/ABSOLUTE/PATH/TO/calendar_mcp.py"]
}
```

### Cursor

**File:** `~/.cursor/mcp.json`

```json
"GoogleCalendar": {
  "command": "/ABSOLUTE/PATH/TO/venv/bin/python",
  "args": ["/ABSOLUTE/PATH/TO/calendar_mcp.py"]
}
```

Then restart Claude Desktop (Cmd+Q → Reopen) or reload Cursor (Cmd+Shift+P → Reload Window).

---

## Important Notes

- Server runs with **stdio** transport (`mcp.run(transport="stdio")`)
- Config must point directly to `calendar_mcp.py` — do **not** use `-m mcp run`
- **Never commit** `credentials.json`, `token.json`, or `venv/` to Git

---

## Files

| File | What | Git? |
|------|------|------|
| `calendar_mcp.py` | MCP server (5 tools) | Yes |
| `authenticate.py` | OAuth browser flow | Yes |
| `requirements.txt` | Dependencies | Yes |
| `credentials.json` | Google Cloud secret | No |
| `token.json` | Auth session | No |
| `venv/` | Virtual env | No |

---

*Part of the [Euron](https://github.com/aiagentwithdhruv/Euron) project.*
