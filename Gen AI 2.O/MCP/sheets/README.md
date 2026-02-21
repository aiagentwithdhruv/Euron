# Google Sheets MCP Server

MCP server for reading, writing, and managing Google Sheets via the Sheets API v4.

## Tools

| Tool | Description |
|---|---|
| `read_sheet` | Read data from a spreadsheet range. Returns a formatted table. |
| `write_to_sheet` | Write a 2D array of values to a specific range. |
| `append_to_sheet` | Append rows to the end of existing data. |
| `create_spreadsheet` | Create a new spreadsheet. Returns ID and URL. |
| `list_sheets` | List all sheet tabs in a spreadsheet with names and IDs. |

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Place credentials.json in this directory
#    (Download from Google Cloud Console → APIs & Services → Credentials → OAuth 2.0 Client ID)

# 3. Authenticate (opens browser for OAuth consent)
python authenticate.py

# 4. Run the server
python sheets_mcp.py
```

## Cursor / Claude Desktop Config

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "python",
      "args": ["/full/path/to/sheets_mcp.py"],
      "transport": "stdio"
    }
  }
}
```

## Prerequisites

- Python 3.10+
- A Google Cloud project with the **Google Sheets API** enabled
- An OAuth 2.0 Client ID (`credentials.json`) downloaded into this directory
