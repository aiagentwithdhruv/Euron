"""MongoDB MCP Server — functional style with FastMCP."""

import json
import os

from bson import json_util
from mcp.server.fastmcp import FastMCP
from pymongo import MongoClient

mcp = FastMCP("MongoDB")


def get_mongo_client():
    uri = os.environ.get("MONGODB_URI")
    db_name = os.environ.get("MONGODB_DATABASE")
    if not uri or not db_name:
        raise ValueError(
            "MONGODB_URI and MONGODB_DATABASE environment variables are required."
        )
    client = MongoClient(uri)
    return client[db_name]


@mcp.tool()
def list_collections() -> str:
    """List all collections in the configured MongoDB database."""
    try:
        db = get_mongo_client()
        names = db.list_collection_names()
        if not names:
            return "No collections found in the database."
        return "Collections:\n" + "\n".join(f"  • {name}" for name in sorted(names))
    except Exception as e:
        return f"Error listing collections: {e}"


@mcp.tool()
def query_collection(
    collection: str, filter_json: str = "{}", limit: int = 10
) -> str:
    """Query documents from a collection.

    Args:
        collection: Name of the MongoDB collection.
        filter_json: JSON string filter, e.g. '{"status": "active"}'.
        limit: Maximum number of documents to return (default 10).
    """
    try:
        db = get_mongo_client()
        query_filter = json.loads(filter_json)
        docs = list(db[collection].find(query_filter).limit(limit))
        if not docs:
            return "No documents found matching the filter."
        return f"Found {len(docs)} document(s):\n{json_util.dumps(docs, indent=2)}"
    except json.JSONDecodeError as e:
        return f"Invalid filter JSON: {e}"
    except Exception as e:
        return f"Error querying collection: {e}"


@mcp.tool()
def insert_document(collection: str, document: str) -> str:
    """Insert a single document into a collection.

    Args:
        collection: Name of the MongoDB collection.
        document: JSON string of the document to insert, e.g. '{"name": "Alice", "age": 30}'.
    """
    try:
        db = get_mongo_client()
        doc = json.loads(document)
        result = db[collection].insert_one(doc)
        return f"Document inserted successfully. ID: {result.inserted_id}"
    except json.JSONDecodeError as e:
        return f"Invalid document JSON: {e}"
    except Exception as e:
        return f"Error inserting document: {e}"


@mcp.tool()
def update_documents(collection: str, filter_json: str, update_json: str) -> str:
    """Update documents matching a filter by setting fields.

    Args:
        collection: Name of the MongoDB collection.
        filter_json: JSON string filter to match documents, e.g. '{"status": "pending"}'.
        update_json: JSON string of fields to set, e.g. '{"status": "complete"}'.
                     Automatically wrapped in $set.
    """
    try:
        db = get_mongo_client()
        query_filter = json.loads(filter_json)
        update_fields = json.loads(update_json)
        result = db[collection].update_many(query_filter, {"$set": update_fields})
        return (
            f"Matched {result.matched_count} document(s), "
            f"modified {result.modified_count} document(s)."
        )
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {e}"
    except Exception as e:
        return f"Error updating documents: {e}"


@mcp.tool()
def delete_documents(collection: str, filter_json: str) -> str:
    """Delete documents matching a filter.

    Args:
        collection: Name of the MongoDB collection.
        filter_json: JSON string filter to match documents, e.g. '{"status": "archived"}'.
    """
    try:
        db = get_mongo_client()
        query_filter = json.loads(filter_json)
        result = db[collection].delete_many(query_filter)
        return f"Deleted {result.deleted_count} document(s)."
    except json.JSONDecodeError as e:
        return f"Invalid filter JSON: {e}"
    except Exception as e:
        return f"Error deleting documents: {e}"


@mcp.tool()
def count_documents(collection: str, filter_json: str = "{}") -> str:
    """Count documents in a collection matching an optional filter.

    Args:
        collection: Name of the MongoDB collection.
        filter_json: JSON string filter, e.g. '{"active": true}'. Defaults to all documents.
    """
    try:
        db = get_mongo_client()
        query_filter = json.loads(filter_json)
        count = db[collection].count_documents(query_filter)
        return f"Count: {count} document(s) match the filter."
    except json.JSONDecodeError as e:
        return f"Invalid filter JSON: {e}"
    except Exception as e:
        return f"Error counting documents: {e}"


@mcp.tool()
def aggregate(collection: str, pipeline_json: str) -> str:
    """Run an aggregation pipeline on a collection.

    Args:
        collection: Name of the MongoDB collection.
        pipeline_json: JSON array string representing the pipeline stages,
                       e.g. '[{"$match": {"status": "active"}}, {"$group": {"_id": "$city", "total": {"$sum": 1}}}]'.
    """
    try:
        db = get_mongo_client()
        pipeline = json.loads(pipeline_json)
        if not isinstance(pipeline, list):
            return "Pipeline must be a JSON array of stages."
        results = list(db[collection].aggregate(pipeline))
        if not results:
            return "Aggregation returned no results."
        return f"Aggregation returned {len(results)} result(s):\n{json_util.dumps(results, indent=2)}"
    except json.JSONDecodeError as e:
        return f"Invalid pipeline JSON: {e}"
    except Exception as e:
        return f"Error running aggregation: {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
