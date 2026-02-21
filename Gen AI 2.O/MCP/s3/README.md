# AWS S3 MCP Server

Manage AWS S3 buckets and objects through the Model Context Protocol.

## Tools

| Tool | Description |
|------|-------------|
| `list_buckets` | List all S3 buckets in the account |
| `list_objects` | List objects in a bucket (with optional prefix filter and limit) |
| `upload_text` | Upload text content as a file to S3 |
| `download_text` | Download and return text content of an object (first 5 000 chars) |
| `delete_object` | Delete an object from a bucket |
| `get_presigned_url` | Generate a temporary presigned URL for an object |

## Quick Start

```bash
cd s3
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Cursor / MCP Client Config

```json
{
  "mcpServers": {
    "S3Storage": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/s3_mcp.py"],
      "env": {
        "AWS_ACCESS_KEY_ID": "your-access-key",
        "AWS_SECRET_ACCESS_KEY": "your-secret-key",
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

Replace the paths and credentials with your own values. `AWS_REGION` defaults to `us-east-1` if omitted.
