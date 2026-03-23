# Skill: euron-mcp

> Set up and use the 8 MCP servers built for Euron's Gen AI 2.0 course. Covers calendar, sheets, social media, Supabase, MongoDB, Azure Blob, S3, and email.

## When to Use
- Setting up MCP servers from the Gen AI 2.0 course
- Connecting Claude Desktop/Cursor to Google Sheets, Calendar, etc.
- Troubleshooting MCP server connections
- Building new MCP servers following Euron patterns

## Available MCP Servers

| Server | Path | Purpose |
|--------|------|---------|
| Calendar | `Gen-AI-2.O/MCP/calendar/` | Google Calendar read/write |
| Sheets | `Gen-AI-2.O/MCP/sheets/` | Google Sheets CRUD |
| Social Media | `Gen-AI-2.O/MCP/social-media/` | Social media posting |
| Supabase | `Gen-AI-2.O/MCP/supabase/` | Supabase DB operations |
| MongoDB | `Gen-AI-2.O/MCP/mongodb/` | MongoDB CRUD |
| Azure Blob | `Gen-AI-2.O/MCP/azure-blob/` | Azure Blob Storage |
| S3 | `Gen-AI-2.O/MCP/s3/` | AWS S3 operations |
| Email | `Gen-AI-2.O/MCP/email_mcp.py` | Gmail send/read via OAuth |

## Setup Pattern

### 1. Install Dependencies
```bash
cd Euron/Gen-AI-2.O/MCP
pip install -r requirements.txt
```

### 2. Gmail OAuth (for Calendar, Sheets, Email)
```bash
# Already have credentials.json and token.json in MCP/
# If token expired:
python authenticate.py
```

### 3. MCP Config for Claude Desktop
```json
{
  "mcpServers": {
    "euron-calendar": {
      "command": "python3",
      "args": ["Euron/Gen-AI-2.O/MCP/calendar/server.py"]
    },
    "euron-sheets": {
      "command": "python3",
      "args": ["Euron/Gen-AI-2.O/MCP/sheets/server.py"]
    }
  }
}
```

### 4. Each Server Has Its Own venv
Some servers have their own `venv/` for isolation. Activate before running:
```bash
cd Euron/Gen-AI-2.O/MCP/calendar
source venv/bin/activate
python server.py
```

## Common Issues

| Issue | Fix |
|-------|-----|
| Token expired | Run `python authenticate.py` in MCP/ folder |
| Module not found | Activate the server's venv, not the global one |
| Permission denied | Re-run OAuth flow, grant all requested scopes |
| Port conflict | Each server uses stdio transport, no port needed |

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| server_name | string | yes | Which MCP server (calendar, sheets, etc.) |
| action | string | yes | What to do (setup, test, troubleshoot) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| config | object | MCP config JSON for Claude Desktop |
| status | string | Server health status |

### Credentials
| Name | Source | Description |
|------|--------|-------------|
| Google OAuth | `Gen-AI-2.O/MCP/credentials.json` | Google Cloud Console |
| Google Token | `Gen-AI-2.O/MCP/token.json` | Auto-generated via authenticate.py |
| Supabase | Environment variable | Supabase project URL + anon key |
| MongoDB | Environment variable | MongoDB connection string |
| AWS | Environment variable | AWS access key + secret |
| Azure | Environment variable | Azure connection string |

## Files
| File | Purpose |
|------|---------|
| `../../Gen-AI-2.O/MCP/README.md` | Full MCP setup guide |
| `../../Gen-AI-2.O/MCP/requirements.txt` | Python dependencies |
| `../../Gen-AI-2.O/MCP/authenticate.py` | Google OAuth flow |
| `../../MAIL-MCP-SETUP.md` | Email MCP detailed setup |

## Self-Update Rules
| Event | Update |
|-------|--------|
| New MCP server added | Add to table above + create server folder |
| OAuth flow changed | Update authenticate.py + this file |
| New dependency | Update requirements.txt |
