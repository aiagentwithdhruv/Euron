import os
import json
from mcp.server.fastmcp import FastMCP
from supabase import create_client

mcp = FastMCP("SupabaseDB")


def get_supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required.")
    return create_client(url, key)


@mcp.tool()
def query_table(table_name: str, select_columns: str = "*", limit: int = 10, filters: str = "") -> str:
    """Query a Supabase table with optional filtering.

    Args:
        table_name: Name of the table to query.
        select_columns: Comma-separated columns to select (default "*").
        limit: Maximum number of rows to return (default 10).
        filters: Optional JSON string for filtering, e.g.
                 '{"column": "status", "operator": "eq", "value": "active"}'
                 or a JSON array of such objects for multiple filters.
    """
    try:
        client = get_supabase_client()
        query = client.table(table_name).select(select_columns).limit(limit)

        if filters:
            parsed = json.loads(filters)
            filter_list = parsed if isinstance(parsed, list) else [parsed]
            for f in filter_list:
                col = f["column"]
                op = f["operator"]
                val = f["value"]
                query = getattr(query, op)(col, val)

        result = query.execute()
        if not result.data:
            return f"No rows found in '{table_name}'."
        return json.dumps(result.data, indent=2, default=str)
    except json.JSONDecodeError:
        return "Error: 'filters' must be a valid JSON string."
    except Exception as e:
        return f"Error querying '{table_name}': {e}"


@mcp.tool()
def insert_row(table_name: str, data: str) -> str:
    """Insert a row into a Supabase table.

    Args:
        table_name: Name of the table.
        data: JSON string of key-value pairs, e.g. '{"name": "John", "age": 30}'.
    """
    try:
        client = get_supabase_client()
        row = json.loads(data)
        result = client.table(table_name).insert(row).execute()
        return f"Inserted into '{table_name}': {json.dumps(result.data, indent=2, default=str)}"
    except json.JSONDecodeError:
        return "Error: 'data' must be a valid JSON string."
    except Exception as e:
        return f"Error inserting into '{table_name}': {e}"


@mcp.tool()
def update_row(table_name: str, match_column: str, match_value: str, data: str) -> str:
    """Update rows in a Supabase table where match_column equals match_value.

    Args:
        table_name: Name of the table.
        match_column: Column to match on.
        match_value: Value to match.
        data: JSON string of fields to update, e.g. '{"status": "completed"}'.
    """
    try:
        client = get_supabase_client()
        updates = json.loads(data)
        result = (
            client.table(table_name)
            .update(updates)
            .eq(match_column, match_value)
            .execute()
        )
        if not result.data:
            return f"No rows matched '{match_column}' = '{match_value}' in '{table_name}'."
        return f"Updated {len(result.data)} row(s) in '{table_name}': {json.dumps(result.data, indent=2, default=str)}"
    except json.JSONDecodeError:
        return "Error: 'data' must be a valid JSON string."
    except Exception as e:
        return f"Error updating '{table_name}': {e}"


@mcp.tool()
def delete_row(table_name: str, match_column: str, match_value: str) -> str:
    """Delete rows from a Supabase table where match_column equals match_value.

    Args:
        table_name: Name of the table.
        match_column: Column to match on.
        match_value: Value to match.
    """
    try:
        client = get_supabase_client()
        result = (
            client.table(table_name)
            .delete()
            .eq(match_column, match_value)
            .execute()
        )
        if not result.data:
            return f"No rows matched '{match_column}' = '{match_value}' in '{table_name}'."
        return f"Deleted {len(result.data)} row(s) from '{table_name}'."
    except Exception as e:
        return f"Error deleting from '{table_name}': {e}"


@mcp.tool()
def list_tables() -> str:
    """List all tables in the Supabase database.

    Requires a Postgres function 'list_tables' created via:
        CREATE OR REPLACE FUNCTION list_tables()
        RETURNS TABLE(table_name text) AS $$
            SELECT table_name::text
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        $$ LANGUAGE sql SECURITY DEFINER;
    """
    try:
        client = get_supabase_client()
        result = client.rpc("list_tables").execute()
        if not result.data:
            return "No tables found, or the 'list_tables' RPC function is not set up."
        tables = [row.get("table_name", row) for row in result.data]
        return "Tables in database:\n" + "\n".join(f"  - {t}" for t in tables)
    except Exception as e:
        return (
            f"Error listing tables: {e}\n\n"
            "Hint: Create an RPC function in Supabase SQL Editor:\n"
            "  CREATE OR REPLACE FUNCTION list_tables()\n"
            "  RETURNS TABLE(table_name text) AS $$\n"
            "    SELECT table_name::text\n"
            "    FROM information_schema.tables\n"
            "    WHERE table_schema = 'public' AND table_type = 'BASE TABLE';\n"
            "  $$ LANGUAGE sql SECURITY DEFINER;"
        )


@mcp.tool()
def run_sql(sql_query: str) -> str:
    """Execute a raw SQL query via a Supabase RPC function.

    Requires a Postgres function 'run_sql' created via:
        CREATE OR REPLACE FUNCTION run_sql(query text)
        RETURNS json AS $$
        DECLARE result json;
        BEGIN
            EXECUTE query INTO result;
            RETURN result;
        END;
        $$ LANGUAGE plpgsql SECURITY DEFINER;

    Args:
        sql_query: The SQL query to execute.
    """
    try:
        client = get_supabase_client()
        result = client.rpc("run_sql", {"query": sql_query}).execute()
        return json.dumps(result.data, indent=2, default=str)
    except Exception as e:
        return (
            f"Error executing SQL: {e}\n\n"
            "Hint: Create an RPC function in Supabase SQL Editor:\n"
            "  CREATE OR REPLACE FUNCTION run_sql(query text)\n"
            "  RETURNS json AS $$\n"
            "  DECLARE result json;\n"
            "  BEGIN\n"
            "    EXECUTE query INTO result;\n"
            "    RETURN result;\n"
            "  END;\n"
            "  $$ LANGUAGE plpgsql SECURITY DEFINER;"
        )


if __name__ == "__main__":
    mcp.run(transport="stdio")
