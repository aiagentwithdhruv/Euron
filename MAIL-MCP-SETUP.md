# MCP Toolkit — Complete Setup Guide

> **8 MCP servers. 50 tools. One setup guide.**
> Control Gmail, Calendar, Sheets, Supabase, MongoDB, S3, Azure Blob, YouTube, Instagram, and Facebook — entirely from AI chat via Claude Desktop or Cursor.

---

## Table of Contents

1. [What is This?](#what-is-this)
2. [Architecture](#architecture)
3. [All Servers & Tools](#all-servers--tools)
4. [Prerequisites](#prerequisites)
5. [Setup: Google Services (Mail, Calendar, Sheets)](#setup-google-services-mail-calendar-sheets)
6. [Setup: Supabase](#setup-supabase)
7. [Setup: MongoDB](#setup-mongodb)
8. [Setup: AWS S3](#setup-aws-s3)
9. [Setup: Azure Blob Storage](#setup-azure-blob-storage)
10. [Setup: Social Media (YouTube + Instagram + Facebook)](#setup-social-media-youtube--instagram--facebook)
11. [Adding to Claude Desktop](#adding-to-claude-desktop)
12. [Adding to Cursor IDE](#adding-to-cursor-ide)
13. [Full Config Example (All 8 Servers)](#full-config-example-all-8-servers)
14. [Usage Examples](#usage-examples)
15. [Troubleshooting](#troubleshooting)
16. [Project Structure](#project-structure)

---

## What is This?

This is a collection of **Model Context Protocol (MCP)** servers built in Python using the **FastMCP** library. Each server connects a real-world service (Gmail, Calendar, databases, cloud storage, social media) to AI assistants like Claude and Cursor.

Once configured, you just chat naturally:
- *"Read my last 5 emails"*
- *"What's on my calendar today?"*
- *"Query the users table where status is active"*
- *"Upload this text to my S3 bucket"*
- *"How many subscribers does my YouTube channel have?"*

**Key design principles:**
- **Functional style** — no classes, just plain decorated functions
- **Stdio transport** — works natively with Claude Desktop and Cursor
- **Each server is independent** — pick and choose what you need
- **Secure** — credentials are never committed to Git

---

## Architecture

```
You (Natural Language)
   │
   ▼
Claude Desktop / Cursor IDE
   │
   ▼  (MCP Protocol — stdio)
┌─────────────────────────────────────────────┐
│              MCP Servers (Python)            │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Gmail   │  │ Calendar │  │  Sheets  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │              │              │        │
│       ▼              ▼              ▼        │
│     Google APIs (OAuth 2.0)                  │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Supabase │  │ MongoDB  │  │   S3     │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │              │              │        │
│       ▼              ▼              ▼        │
│   REST API      pymongo         boto3       │
│                                             │
│  ┌──────────┐  ┌───────────────────────┐    │
│  │  Azure   │  │  Social Media         │    │
│  │  Blob    │  │  (YT + IG + FB)       │    │
│  └────┬─────┘  └────┬──────────────────┘    │
│       │              │                       │
│       ▼              ▼                       │
│  azure SDK    Google + Meta APIs             │
└─────────────────────────────────────────────┘
```

---

## All Servers & Tools

### 1. Gmail (4 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `send_email` | Send an email | `to_email`, `subject`, `body` |
| `read_recent_emails` | Fetch latest emails | `limit`, `query` |
| `search_emails` | Search with Gmail syntax | `query`, `limit` |
| `mark_email_seen` | Mark as read | `query` |

### 2. Google Calendar (5 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_events` | Upcoming events | `limit`, `days_ahead` |
| `create_event` | Create an event | `summary`, `start_datetime`, `end_datetime`, `description`, `location` |
| `search_events` | Search by text | `query`, `limit` |
| `delete_event` | Delete an event | `event_id` |
| `get_todays_schedule` | Today's full schedule | — |

### 3. Google Sheets (5 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `read_sheet` | Read a range | `spreadsheet_id`, `range_name` |
| `write_to_sheet` | Write to a range | `spreadsheet_id`, `range_name`, `values` |
| `append_to_sheet` | Append rows | `spreadsheet_id`, `range_name`, `values` |
| `create_spreadsheet` | Create new spreadsheet | `title` |
| `list_sheets` | List all tabs | `spreadsheet_id` |

### 4. Supabase (6 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `query_table` | Query with filters | `table_name`, `select_columns`, `limit`, `filters` |
| `insert_row` | Insert a row | `table_name`, `data` (JSON) |
| `update_row` | Update matching rows | `table_name`, `match_column`, `match_value`, `data` |
| `delete_row` | Delete matching rows | `table_name`, `match_column`, `match_value` |
| `list_tables` | List all tables | — |
| `run_sql` | Execute raw SQL | `sql_query` |

### 5. MongoDB (7 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_collections` | List collections | — |
| `query_collection` | Query documents | `collection`, `filter_json`, `limit` |
| `insert_document` | Insert a document | `collection`, `document` (JSON) |
| `update_documents` | Update matching docs | `collection`, `filter_json`, `update_json` |
| `delete_documents` | Delete matching docs | `collection`, `filter_json` |
| `count_documents` | Count matching docs | `collection`, `filter_json` |
| `aggregate` | Aggregation pipeline | `collection`, `pipeline_json` |

### 6. AWS S3 (6 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_buckets` | List all buckets | — |
| `list_objects` | List objects in bucket | `bucket`, `prefix`, `limit` |
| `upload_text` | Upload text content | `bucket`, `key`, `content` |
| `download_text` | Download text content | `bucket`, `key` |
| `delete_object` | Delete an object | `bucket`, `key` |
| `get_presigned_url` | Temporary access URL | `bucket`, `key`, `expiration` |

### 7. Azure Blob Storage (7 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_containers` | List containers | — |
| `list_blobs` | List blobs | `container`, `prefix`, `limit` |
| `upload_text` | Upload text content | `container`, `blob_name`, `content` |
| `download_text` | Download text content | `container`, `blob_name` |
| `delete_blob` | Delete a blob | `container`, `blob_name` |
| `create_container` | Create container | `container` |
| `generate_sas_url` | Temporary SAS URL | `container`, `blob_name`, `expiry_hours` |

### 8. Social Media (10 tools)

**YouTube:**

| Tool | Description | Parameters |
|------|-------------|------------|
| `youtube_search` | Search videos | `query`, `limit` |
| `youtube_channel_stats` | Channel analytics | `channel_id` |
| `youtube_video_details` | Video stats | `video_id` |
| `youtube_my_videos` | Your uploaded videos | `limit` |

**Instagram:**

| Tool | Description | Parameters |
|------|-------------|------------|
| `instagram_profile` | Profile & followers | — |
| `instagram_recent_posts` | Recent posts | `limit` |
| `instagram_post_insights` | Post analytics | `media_id` |

**Facebook:**

| Tool | Description | Parameters |
|------|-------------|------------|
| `facebook_page_info` | Page info & followers | — |
| `facebook_recent_posts` | Recent page posts | `limit` |
| `facebook_post_to_page` | Post to page | `message` |

---

## Prerequisites

- [ ] **Python 3.9+** — [Download](https://www.python.org/downloads/)
- [ ] **Claude Desktop** — [Download](https://claude.ai/download) and/or **Cursor IDE** — [Download](https://cursor.com)
- [ ] **Terminal** access (macOS Terminal, Windows CMD/PowerShell, or IDE terminal)
- [ ] Accounts for the services you want to use (Google, Supabase, MongoDB, AWS, Azure, Meta)

---

## Setup: Google Services (Mail, Calendar, Sheets)

All three Google services share the same authentication pattern. Set up Google Cloud once, then reuse the same `credentials.json` for each.

### Step 1 — Google Cloud Project (One-Time)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a **new project** (e.g., `MCP Toolkit`)
3. Enable the following APIs under **APIs & Services → Library**:
   - **Gmail API**
   - **Google Calendar API**
   - **Google Sheets API**

### Step 2 — OAuth Consent Screen (One-Time)

1. Go to **APIs & Services → OAuth consent screen**
2. Choose **External** → Create
3. Fill in: App name, Support email, Developer email
4. Click through remaining steps
5. Under **Test users** → Add your Google email address

### Step 3 — Create OAuth Client (One-Time)

1. Go to **APIs & Services → Credentials**
2. Click **+ Create Credentials → OAuth client ID**
3. Application type: **Desktop app**
4. Download the JSON file
5. Rename it to `credentials.json`

### Step 4 — Set Up Each Server

Repeat for each: `Gen AI 2.O/MCP/` (mail), `calendar/`, `sheets/`

```bash
# Navigate to the server folder
cd "Gen AI 2.O/MCP"          # For mail
# cd "Gen AI 2.O/MCP/calendar"  # For calendar
# cd "Gen AI 2.O/MCP/sheets"    # For sheets

# Copy your credentials.json into this folder
cp /path/to/credentials.json .

# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate      # macOS/Linux
# venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Authenticate (opens browser — one-time)
python authenticate.py
```

After authenticating, a `token.json` file is created. The server auto-refreshes it.

### Step 5 — Verify

```bash
# Quick test (mail example)
python -c "
from email_mcp import get_gmail_service
service = get_gmail_service()
results = service.users().messages().list(userId='me', maxResults=1).execute()
print(f'Connected! Found {len(results.get(\"messages\", []))} message(s).')
"
```

---

## Setup: Supabase

### Step 1 — Get Your Credentials

1. Go to your [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to **Settings → API**
4. Copy your **Project URL** and **API Key** (use `service_role` key for full access)

### Step 2 — Install & Test

```bash
cd "Gen AI 2.O/MCP/supabase"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Quick test
SUPABASE_URL="https://your-project.supabase.co" \
SUPABASE_KEY="your-service-role-key" \
python -c "from supabase_mcp import get_supabase_client; print('Connected!')"
```

### Auth Note

- **Anon key**: Respects Row Level Security (RLS) policies
- **Service role key**: Bypasses RLS — full database access (use for admin tools)

---

## Setup: MongoDB

### Step 1 — Get Your Connection String

**MongoDB Atlas (Cloud):**
1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Click **Connect** on your cluster
3. Choose **Connect your application**
4. Copy the connection string (replace `<password>` with your actual password)

**Local MongoDB:**
- Use `mongodb://localhost:27017/`

### Step 2 — Install & Test

```bash
cd "Gen AI 2.O/MCP/mongodb"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Quick test
MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/" \
MONGODB_DATABASE="your_db" \
python -c "from mongodb_mcp import get_mongo_client; db = get_mongo_client(); print(f'Connected! Collections: {db.list_collection_names()}')"
```

---

## Setup: AWS S3

### Step 1 — Get Your AWS Credentials

1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Create a user (or use an existing one) with **AmazonS3FullAccess** policy
3. Generate **Access Key ID** and **Secret Access Key**

### Step 2 — Install & Test

```bash
cd "Gen AI 2.O/MCP/s3"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Quick test
AWS_ACCESS_KEY_ID="your-key" \
AWS_SECRET_ACCESS_KEY="your-secret" \
AWS_REGION="us-east-1" \
python -c "from s3_mcp import get_s3_client; s3 = get_s3_client(); print(f'Connected! Buckets: {[b[\"Name\"] for b in s3.list_buckets()[\"Buckets\"]]}')"
```

---

## Setup: Azure Blob Storage

### Step 1 — Get Your Connection String

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to your **Storage Account**
3. Go to **Access keys** under Security + networking
4. Copy the **Connection string**

### Step 2 — Install & Test

```bash
cd "Gen AI 2.O/MCP/azure-blob"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Quick test
AZURE_STORAGE_CONNECTION_STRING="your-connection-string" \
python -c "from azure_blob_mcp import get_blob_service; svc = get_blob_service(); print('Connected!')"
```

---

## Setup: Social Media (YouTube + Instagram + Facebook)

This server combines three platforms. YouTube uses Google OAuth (same as Gmail), while Instagram and Facebook use Meta's Graph API.

### YouTube Setup

1. Enable **YouTube Data API v3** in your Google Cloud project
2. Copy your `credentials.json` into `Gen AI 2.O/MCP/social-media/`

```bash
cd "Gen AI 2.O/MCP/social-media"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python authenticate.py    # Browser login for YouTube
```

### Instagram & Facebook Setup

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create an app → Choose **Business** type
3. Add **Instagram Graph API** and **Facebook Login** products
4. Generate a **long-lived access token**
5. Get your **Instagram Business Account ID** and **Facebook Page ID**

These are passed as environment variables when configuring the MCP server (see config below).

> **Note:** Instagram requires a Business or Creator account connected to a Facebook Page.

---

## Adding to Claude Desktop

### Config File Location

| OS | Path |
|----|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

### Config Structure

Each server is an entry under `mcpServers`:

```json
"ServerName": {
  "command": "/absolute/path/to/venv/bin/python",
  "args": ["/absolute/path/to/server_script.py"],
  "env": {
    "KEY": "value"
  }
}
```

- `command` — Python from the server's **venv** (not system Python)
- `args` — Absolute path to the MCP server script
- `env` — Only for servers that need API keys/connection strings (not Google OAuth servers)

After updating the config: **Quit Claude Desktop (Cmd+Q) → Reopen**

---

## Adding to Cursor IDE

### Config File Location

| OS | Path |
|----|------|
| macOS / Linux | `~/.cursor/mcp.json` |
| Windows | `%USERPROFILE%\.cursor\mcp.json` |

Same config format as Claude Desktop. After updating: **Cmd+Shift+P → Reload Window**

---

## Full Config Example (All 8 Servers)

Replace `/PATH/TO/MCP` with the actual absolute path to your `Gen AI 2.O/MCP/` folder.

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
        "SUPABASE_KEY": "your-service-role-key"
      }
    },
    "MongoDB": {
      "command": "/PATH/TO/MCP/mongodb/venv/bin/python",
      "args": ["/PATH/TO/MCP/mongodb/mongodb_mcp.py"],
      "env": {
        "MONGODB_URI": "mongodb+srv://user:pass@cluster.mongodb.net/",
        "MONGODB_DATABASE": "your_database"
      }
    },
    "S3Storage": {
      "command": "/PATH/TO/MCP/s3/venv/bin/python",
      "args": ["/PATH/TO/MCP/s3/s3_mcp.py"],
      "env": {
        "AWS_ACCESS_KEY_ID": "your-access-key",
        "AWS_SECRET_ACCESS_KEY": "your-secret-key",
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
        "META_ACCESS_TOKEN": "your-meta-access-token",
        "INSTAGRAM_BUSINESS_ID": "your-ig-business-id",
        "FACEBOOK_PAGE_ID": "your-fb-page-id"
      }
    }
  }
}
```

---

## Usage Examples

### Gmail
- *"Show me my last 5 emails"*
- *"Send an email to john@example.com about tomorrow's meeting"*
- *"Search for emails from GitHub with attachments"*

### Calendar
- *"What's on my schedule today?"*
- *"Create a meeting with Sarah tomorrow at 3 PM for 1 hour"*
- *"Find all events with 'standup' in the next 2 weeks"*

### Sheets
- *"Read data from spreadsheet ABC123, range Sheet1!A1:D10"*
- *"Append a new row with name John, age 30 to my sheet"*
- *"Create a new spreadsheet called 'Project Tracker'"*

### Supabase
- *"Query the users table where status is active"*
- *"Insert a new task: title 'Fix login bug', priority 'high'"*
- *"How many messages are in the conversations table?"*

### MongoDB
- *"List all collections in the database"*
- *"Find documents in 'orders' where amount is greater than 1000"*
- *"Count how many users signed up this month"*

### S3
- *"List all my S3 buckets"*
- *"Upload this text as 'notes/meeting.txt' to my-bucket"*
- *"Generate a download link for report.pdf that expires in 1 hour"*

### Azure Blob
- *"List all containers in my storage account"*
- *"Upload this content as 'data/export.csv'"*
- *"Generate a temporary link for the backup file"*

### Social Media
- *"How many subscribers does my YouTube channel have?"*
- *"Show me my latest 5 YouTube videos with view counts"*
- *"What are my recent Instagram posts and their engagement?"*
- *"Post 'Exciting update coming soon!' to my Facebook page"*

---

## Troubleshooting

### "MCP Server disconnected" (Claude Desktop)

1. Verify `email_mcp.py` (or any server) has `mcp.run(transport="stdio")` at the bottom
2. Config should NOT use `-m mcp run` — run the script directly
3. Restart Claude Desktop completely (Cmd+Q → Reopen)

### "Authentication token missing or invalid" (Google services)

```bash
cd <server-folder>
source venv/bin/activate
python authenticate.py
```

### "Failed to refresh token" (Google services)

```bash
rm token.json
python authenticate.py
```

### Cursor MCP shows error

1. Check that all paths in `~/.cursor/mcp.json` are **absolute**
2. Cmd+Shift+P → **Reload Window**

### "Google hasn't verified this app" during OAuth

This is normal for personal OAuth apps. Click **Advanced → Go to [App Name] (unsafe)**. Safe because you own both the app and the account.

### Supabase: "Could not find function"

The `list_tables` and `run_sql` tools require RPC functions in Supabase. See `Gen AI 2.O/MCP/supabase/README.md` for the SQL to create them. Other tools (query, insert, update, delete) work out of the box.

### MongoDB: Connection timeout

- Ensure your IP is whitelisted in MongoDB Atlas (Network Access → Add IP)
- Verify the connection string has the correct password

### S3/Azure: Permission denied

- AWS: Ensure the IAM user has `AmazonS3FullAccess` or equivalent policy
- Azure: Ensure the storage account access key is correct and not rotated

---

## Project Structure

```
Gen AI 2.O/MCP/
│
├── email_mcp.py              # Gmail — 4 tools
├── authenticate.py           # Gmail OAuth
├── requirements.txt
│
├── calendar/                 # Google Calendar — 5 tools
│   ├── calendar_mcp.py
│   ├── authenticate.py
│   └── requirements.txt
│
├── sheets/                   # Google Sheets — 5 tools
│   ├── sheets_mcp.py
│   ├── authenticate.py
│   └── requirements.txt
│
├── supabase/                 # Supabase (Postgres) — 6 tools
│   ├── supabase_mcp.py
│   └── requirements.txt
│
├── mongodb/                  # MongoDB — 7 tools
│   ├── mongodb_mcp.py
│   └── requirements.txt
│
├── s3/                       # AWS S3 — 6 tools
│   ├── s3_mcp.py
│   └── requirements.txt
│
├── azure-blob/               # Azure Blob Storage — 7 tools
│   ├── azure_blob_mcp.py
│   └── requirements.txt
│
└── social-media/             # YouTube + Instagram + Facebook — 10 tools
    ├── social_mcp.py
    ├── authenticate.py
    └── requirements.txt
```

### What NOT to commit

| File | Why |
|------|-----|
| `credentials.json` | Your Google Cloud OAuth secret |
| `token.json` | Your personal auth session |
| `venv/` | Virtual environment (recreate with `pip install -r requirements.txt`) |
| `.env` | Environment variables with API keys |

All `.gitignore` files are pre-configured to handle this.

---

## About

Built as part of the **Euron AI Automation Bootcamp** by [AI with Dhruv](https://youtube.com/@aiwithdhruv) — demonstrating how to build production-ready MCP servers that connect AI assistants to real-world services using functional Python and FastMCP.

**Repository:** [github.com/aiagentwithdhruv/Euron](https://github.com/aiagentwithdhruv/Euron)
