# MongoDB MCP Server

A lightweight MCP server that exposes MongoDB operations as tools, built with FastMCP and pymongo.

## Tools

| Tool | Description |
|------|-------------|
| `list_collections` | List all collections in the database |
| `query_collection` | Query documents with optional filter and limit |
| `insert_document` | Insert a single document |
| `update_documents` | Update documents matching a filter (`$set`) |
| `delete_documents` | Delete documents matching a filter |
| `count_documents` | Count documents matching a filter |
| `aggregate` | Run an aggregation pipeline |

## Quick Start

```bash
cd mongodb
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
export MONGODB_DATABASE="your_database_name"
python mongodb_mcp.py
```

## Cursor / Claude Desktop Config

```json
"MongoDB": {
  "command": "/path/to/venv/bin/python",
  "args": ["/path/to/mongodb_mcp.py"],
  "env": {
    "MONGODB_URI": "mongodb+srv://user:pass@cluster.mongodb.net/",
    "MONGODB_DATABASE": "your_database_name"
  }
}
```

Replace the paths and credentials with your own values. Works with both **MongoDB Atlas** connection strings and **local MongoDB** (`mongodb://localhost:27017/`).
