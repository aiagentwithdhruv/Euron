# Azure Blob Storage MCP Server

MCP server for managing Azure Blob Storage — list, upload, download, delete blobs and containers, and generate SAS URLs.

## Tools

| Tool | Description |
|------|-------------|
| `list_containers` | List all blob containers in the storage account |
| `list_blobs` | List blobs in a container (name, size, last modified) |
| `upload_text` | Upload text content as a blob |
| `download_text` | Download text content of a blob (first 5000 chars) |
| `delete_blob` | Delete a blob from a container |
| `create_container` | Create a new blob container |
| `generate_sas_url` | Generate a temporary SAS URL for read access |

## Quick Start

```bash
cd /path/to/azure-blob
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Cursor / MCP Client Config

```json
"AzureBlob": {
  "command": "/path/to/venv/bin/python",
  "args": ["/path/to/azure_blob_mcp.py"],
  "env": {
    "AZURE_STORAGE_CONNECTION_STRING": "DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net"
  }
}
```

Set `AZURE_STORAGE_CONNECTION_STRING` to your Azure Storage account connection string (found in the Azure Portal under **Storage Account → Access keys**).
