# MCP Servers Collection — AI-Powered Automation Toolkit

> **8 MCP servers** that let you control Gmail, Calendar, Sheets, Supabase, MongoDB, S3, Azure Blob, and Social Media — entirely from AI chat.

Built with **Python**, **FastMCP**, and a **functional programming** style (no classes). Works with **Claude Desktop** and **Cursor IDE**.

---

## All Servers at a Glance

| # | Server | Folder | Tools | Auth Method |
|---|--------|--------|-------|-------------|
| 1 | **Gmail** | `./` (root) | 4 | Google OAuth 2.0 |
| 2 | **Google Calendar** | `calendar/` | 5 | Google OAuth 2.0 |
| 3 | **Google Sheets** | `sheets/` | 5 | Google OAuth 2.0 |
| 4 | **Supabase** | `supabase/` | 6 | API Key (env var) |
| 5 | **MongoDB** | `mongodb/` | 7 | Connection String (env var) |
| 6 | **AWS S3** | `s3/` | 6 | AWS Credentials (env var) |
| 7 | **Azure Blob** | `azure-blob/` | 7 | Connection String (env var) |
| 8 | **Social Media** | `social-media/` | 10 | Google OAuth + Meta Token |

**Total: 50 tools** across 8 services.

---

## Quick Setup Pattern

Every server follows the same 4-step pattern:

```bash
# 1. Navigate to the server folder
cd <server-folder>

# 2. Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Authenticate (if needed)
python authenticate.py     # Google OAuth servers only
```

Then add to your Claude Desktop or Cursor config. See each server's `README.md` for the exact config snippet.

---

## Server Details

### 1. Gmail (`./`)

| Tool | Description |
|------|-------------|
| `send_email` | Send email to any address |
| `read_recent_emails` | Fetch latest N emails |
| `search_emails` | Search with Gmail syntax |
| `mark_email_seen` | Mark emails as read |

**Setup:** [MAIL-MCP-SETUP.md](../../MAIL-MCP-SETUP.md) | **Auth:** Google OAuth (credentials.json + authenticate.py)

---

### 2. Google Calendar (`calendar/`)

| Tool | Description |
|------|-------------|
| `list_events` | Upcoming events in next N days |
| `create_event` | Create a calendar event |
| `search_events` | Search by text query |
| `delete_event` | Delete an event by ID |
| `get_todays_schedule` | All events for today |

**Auth:** Google OAuth — enable **Calendar API** in same Google Cloud project, run `authenticate.py`

---

### 3. Google Sheets (`sheets/`)

| Tool | Description |
|------|-------------|
| `read_sheet` | Read data from a range |
| `write_to_sheet` | Write data to a range |
| `append_to_sheet` | Append rows to existing data |
| `create_spreadsheet` | Create a new spreadsheet |
| `list_sheets` | List all tabs in a spreadsheet |

**Auth:** Google OAuth — enable **Sheets API** in same Google Cloud project, run `authenticate.py`

---

### 4. Supabase (`supabase/`)

| Tool | Description |
|------|-------------|
| `query_table` | Query with filters and limits |
| `insert_row` | Insert a row from JSON |
| `update_row` | Update matching rows |
| `delete_row` | Delete matching rows |
| `list_tables` | List all tables |
| `run_sql` | Execute raw SQL |

**Auth:** Environment variables — `SUPABASE_URL` + `SUPABASE_KEY`

---

### 5. MongoDB (`mongodb/`)

| Tool | Description |
|------|-------------|
| `list_collections` | List all collections |
| `query_collection` | Query with JSON filter |
| `insert_document` | Insert a document |
| `update_documents` | Update matching documents |
| `delete_documents` | Delete matching documents |
| `count_documents` | Count matching documents |
| `aggregate` | Run aggregation pipeline |

**Auth:** Environment variables — `MONGODB_URI` + `MONGODB_DATABASE`

---

### 6. AWS S3 (`s3/`)

| Tool | Description |
|------|-------------|
| `list_buckets` | List all S3 buckets |
| `list_objects` | List objects with prefix filter |
| `upload_text` | Upload text content |
| `download_text` | Download text content |
| `delete_object` | Delete an object |
| `get_presigned_url` | Generate temporary access URL |

**Auth:** Environment variables — `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` + `AWS_REGION`

---

### 7. Azure Blob (`azure-blob/`)

| Tool | Description |
|------|-------------|
| `list_containers` | List all containers |
| `list_blobs` | List blobs with prefix filter |
| `upload_text` | Upload text content |
| `download_text` | Download text content |
| `delete_blob` | Delete a blob |
| `create_container` | Create a new container |
| `generate_sas_url` | Generate temporary SAS URL |

**Auth:** Environment variable — `AZURE_STORAGE_CONNECTION_STRING`

---

### 8. Social Media (`social-media/`)

**YouTube:**

| Tool | Description |
|------|-------------|
| `youtube_search` | Search YouTube videos |
| `youtube_channel_stats` | Channel subscriber/view stats |
| `youtube_video_details` | Video views, likes, comments |
| `youtube_my_videos` | List your uploaded videos |

**Instagram:**

| Tool | Description |
|------|-------------|
| `instagram_profile` | Profile info and follower count |
| `instagram_recent_posts` | Recent posts with engagement |
| `instagram_post_insights` | Impressions, reach, engagement |

**Facebook:**

| Tool | Description |
|------|-------------|
| `facebook_page_info` | Page info and follower count |
| `facebook_recent_posts` | Recent page posts |
| `facebook_post_to_page` | Post a message to the page |

**Auth:** YouTube = Google OAuth | Instagram/Facebook = Meta Access Token (env vars)

---

## Config Example — All Servers

Here's what a full `claude_desktop_config.json` or `~/.cursor/mcp.json` looks like with all 8 servers:

```json
{
  "mcpServers": {
    "EmailAutomation": {
      "command": "/PATH/TO/MCP/venv/bin/python",
      "args": ["/PATH/TO/MCP/email_mcp.py"]
    },
    "GoogleCalendar": {
      "command": "/PATH/TO/MCP/calendar/venv/bin/python",
      "args": ["/PATH/TO/MCP/calendar/calendar_mcp.py"]
    },
    "GoogleSheets": {
      "command": "/PATH/TO/MCP/sheets/venv/bin/python",
      "args": ["/PATH/TO/MCP/sheets/sheets_mcp.py"]
    },
    "SupabaseDB": {
      "command": "/PATH/TO/MCP/supabase/venv/bin/python",
      "args": ["/PATH/TO/MCP/supabase/supabase_mcp.py"],
      "env": {
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_KEY": "your-key"
      }
    },
    "MongoDB": {
      "command": "/PATH/TO/MCP/mongodb/venv/bin/python",
      "args": ["/PATH/TO/MCP/mongodb/mongodb_mcp.py"],
      "env": {
        "MONGODB_URI": "mongodb+srv://user:pass@cluster.mongodb.net/",
        "MONGODB_DATABASE": "your_db"
      }
    },
    "S3Storage": {
      "command": "/PATH/TO/MCP/s3/venv/bin/python",
      "args": ["/PATH/TO/MCP/s3/s3_mcp.py"],
      "env": {
        "AWS_ACCESS_KEY_ID": "your-key",
        "AWS_SECRET_ACCESS_KEY": "your-secret",
        "AWS_REGION": "us-east-1"
      }
    },
    "AzureBlob": {
      "command": "/PATH/TO/MCP/azure-blob/venv/bin/python",
      "args": ["/PATH/TO/MCP/azure-blob/azure_blob_mcp.py"],
      "env": {
        "AZURE_STORAGE_CONNECTION_STRING": "your-connection-string"
      }
    },
    "SocialMedia": {
      "command": "/PATH/TO/MCP/social-media/venv/bin/python",
      "args": ["/PATH/TO/MCP/social-media/social_mcp.py"],
      "env": {
        "META_ACCESS_TOKEN": "your-meta-token",
        "INSTAGRAM_BUSINESS_ID": "your-ig-id",
        "FACEBOOK_PAGE_ID": "your-fb-page-id"
      }
    }
  }
}
```

Replace `/PATH/TO/MCP/` with your actual absolute path to the `Gen AI 2.O/MCP/` folder.

---

## Project Structure

```
Gen AI 2.O/MCP/
├── email_mcp.py              # Gmail MCP server
├── authenticate.py           # Gmail OAuth flow
├── requirements.txt          # Gmail dependencies
│
├── calendar/                 # Google Calendar MCP
│   ├── calendar_mcp.py
│   ├── authenticate.py
│   └── requirements.txt
│
├── sheets/                   # Google Sheets MCP
│   ├── sheets_mcp.py
│   ├── authenticate.py
│   └── requirements.txt
│
├── supabase/                 # Supabase (Postgres) MCP
│   ├── supabase_mcp.py
│   └── requirements.txt
│
├── mongodb/                  # MongoDB MCP
│   ├── mongodb_mcp.py
│   └── requirements.txt
│
├── s3/                       # AWS S3 MCP
│   ├── s3_mcp.py
│   └── requirements.txt
│
├── azure-blob/               # Azure Blob Storage MCP
│   ├── azure_blob_mcp.py
│   └── requirements.txt
│
└── social-media/             # YouTube + Instagram + Facebook MCP
    ├── social_mcp.py
    ├── authenticate.py
    └── requirements.txt
```

---

*Part of the [Euron](https://github.com/aiagentwithdhruv/Euron) project. Built for the AI Automation Bootcamp.*
