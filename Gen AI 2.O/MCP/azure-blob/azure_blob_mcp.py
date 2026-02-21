import os
from datetime import datetime, timedelta, timezone

from mcp.server.fastmcp import FastMCP
from azure.storage.blob import (
    BlobServiceClient,
    BlobSasPermissions,
    generate_blob_sas,
)

mcp = FastMCP("AzureBlob")


def get_blob_service() -> BlobServiceClient:
    conn_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is required.")
    return BlobServiceClient.from_connection_string(conn_str)


@mcp.tool()
def list_containers() -> str:
    """List all blob containers in the storage account."""
    try:
        service = get_blob_service()
        containers = [c["name"] for c in service.list_containers()]
        if not containers:
            return "No containers found in this storage account."
        return "Containers:\n" + "\n".join(f"  • {name}" for name in containers)
    except Exception as e:
        return f"Error listing containers: {e}"


@mcp.tool()
def list_blobs(container: str, prefix: str = "", limit: int = 20) -> str:
    """List blobs in a container with name, size, and last modified date."""
    try:
        service = get_blob_service()
        container_client = service.get_container_client(container)
        blobs = []
        for i, blob in enumerate(container_client.list_blobs(name_starts_with=prefix or None)):
            if i >= limit:
                break
            size_kb = (blob.size or 0) / 1024
            modified = blob.last_modified.strftime("%Y-%m-%d %H:%M:%S") if blob.last_modified else "N/A"
            blobs.append(f"  • {blob.name}  ({size_kb:.1f} KB, modified {modified})")
        if not blobs:
            return f"No blobs found in container '{container}'" + (f" with prefix '{prefix}'" if prefix else "") + "."
        header = f"Blobs in '{container}'" + (f" (prefix='{prefix}')" if prefix else "") + f" (showing up to {limit}):"
        return header + "\n" + "\n".join(blobs)
    except Exception as e:
        return f"Error listing blobs: {e}"


@mcp.tool()
def upload_text(container: str, blob_name: str, content: str) -> str:
    """Upload text content as a blob to a container."""
    try:
        service = get_blob_service()
        blob_client = service.get_blob_client(container, blob_name)
        blob_client.upload_blob(content, overwrite=True)
        return f"Successfully uploaded '{blob_name}' to container '{container}' ({len(content)} characters)."
    except Exception as e:
        return f"Error uploading blob: {e}"


@mcp.tool()
def download_text(container: str, blob_name: str) -> str:
    """Download and return text content of a blob (first 5000 characters)."""
    try:
        service = get_blob_service()
        blob_client = service.get_blob_client(container, blob_name)
        data = blob_client.download_blob().readall().decode("utf-8")
        if len(data) > 5000:
            return data[:5000] + f"\n\n... (truncated, total {len(data)} characters)"
        return data
    except Exception as e:
        return f"Error downloading blob: {e}"


@mcp.tool()
def delete_blob(container: str, blob_name: str) -> str:
    """Delete a blob from a container."""
    try:
        service = get_blob_service()
        blob_client = service.get_blob_client(container, blob_name)
        blob_client.delete_blob()
        return f"Successfully deleted '{blob_name}' from container '{container}'."
    except Exception as e:
        return f"Error deleting blob: {e}"


@mcp.tool()
def create_container(container: str) -> str:
    """Create a new blob container in the storage account."""
    try:
        service = get_blob_service()
        service.create_container(container)
        return f"Container '{container}' created successfully."
    except Exception as e:
        return f"Error creating container: {e}"


@mcp.tool()
def generate_sas_url(container: str, blob_name: str, expiry_hours: int = 24) -> str:
    """Generate a temporary SAS URL for read access to a blob."""
    try:
        service = get_blob_service()
        account_name = service.account_name
        account_key = service.credential.account_key

        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=container,
            blob_name=blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.now(timezone.utc) + timedelta(hours=expiry_hours),
        )

        url = f"https://{account_name}.blob.core.windows.net/{container}/{blob_name}?{sas_token}"
        return f"SAS URL (expires in {expiry_hours}h):\n{url}"
    except Exception as e:
        return f"Error generating SAS URL: {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
