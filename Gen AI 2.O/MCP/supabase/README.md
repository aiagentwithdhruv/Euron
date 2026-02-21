# Supabase Database MCP Server

MCP server for interacting with a Supabase database — query, insert, update, delete rows, list tables, and run raw SQL.

## Tools

| Tool | Description |
|------|-------------|
| `query_table` | Query a table with optional column selection, limit, and JSON filters |
| `insert_row` | Insert a row using a JSON string of key-value pairs |
| `update_row` | Update rows matching a column value |
| `delete_row` | Delete rows matching a column value |
| `list_tables` | List all tables in the public schema (requires RPC function) |
| `run_sql` | Execute raw SQL via an RPC function |

## Quick Start

```bash
cd /path/to/supabase
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set your environment variables:

```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-anon-or-service-key"
```

Test the server:

```bash
python supabase_mcp.py
```

## MCP Configuration

Add to your MCP client config (e.g. `mcp.json` or Cursor settings):

```json
{
  "mcpServers": {
    "SupabaseDB": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/supabase_mcp.py"],
      "env": {
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_KEY": "your-anon-or-service-key"
      }
    }
  }
}
```

## RPC Functions Setup

`list_tables` and `run_sql` require Postgres functions. Run these in the Supabase SQL Editor:

```sql
-- For list_tables
CREATE OR REPLACE FUNCTION list_tables()
RETURNS TABLE(table_name text) AS $$
  SELECT table_name::text
  FROM information_schema.tables
  WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
$$ LANGUAGE sql SECURITY DEFINER;

-- For run_sql
CREATE OR REPLACE FUNCTION run_sql(query text)
RETURNS json AS $$
DECLARE result json;
BEGIN
  EXECUTE query INTO result;
  RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## Auth Key Notes

- **Anon key**: Respects Row Level Security (RLS) policies. Use for user-scoped access.
- **Service role key**: Bypasses RLS entirely. Use for full admin access — keep it secret.
