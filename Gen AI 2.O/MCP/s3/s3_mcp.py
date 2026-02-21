"""AWS S3 MCP Server — manage S3 buckets and objects via MCP tools."""

import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("S3Storage")


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )


def _human_size(nbytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(nbytes) < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} PB"


@mcp.tool()
def list_buckets() -> str:
    """List all S3 buckets in the account."""
    try:
        s3 = get_s3_client()
        response = s3.list_buckets()
        buckets = response.get("Buckets", [])
        if not buckets:
            return "No buckets found."
        lines = [f"Found {len(buckets)} bucket(s):\n"]
        for b in buckets:
            name = b["Name"]
            created = b["CreationDate"].strftime("%Y-%m-%d %H:%M:%S UTC")
            lines.append(f"  • {name}  (created {created})")
        return "\n".join(lines)
    except (BotoCoreError, ClientError) as exc:
        return f"Error listing buckets: {exc}"


@mcp.tool()
def list_objects(bucket: str, prefix: str = "", limit: int = 20) -> str:
    """List objects in an S3 bucket, optionally filtered by prefix."""
    try:
        s3 = get_s3_client()
        params: dict = {"Bucket": bucket, "MaxKeys": limit}
        if prefix:
            params["Prefix"] = prefix
        response = s3.list_objects_v2(**params)
        contents = response.get("Contents", [])
        if not contents:
            msg = f"No objects found in s3://{bucket}/{prefix}"
            return msg.rstrip("/")
        lines = [f"Objects in s3://{bucket}/{prefix}  ({len(contents)} shown, limit={limit}):\n"]
        for obj in contents:
            key = obj["Key"]
            size = _human_size(obj["Size"])
            modified = obj["LastModified"].strftime("%Y-%m-%d %H:%M:%S UTC")
            lines.append(f"  • {key}  |  {size}  |  {modified}")
        if response.get("IsTruncated"):
            lines.append("\n  (results truncated — increase limit to see more)")
        return "\n".join(lines)
    except (BotoCoreError, ClientError) as exc:
        return f"Error listing objects: {exc}"


@mcp.tool()
def upload_text(bucket: str, key: str, content: str) -> str:
    """Upload text content as a file to S3."""
    try:
        s3 = get_s3_client()
        s3.put_object(Bucket=bucket, Key=key, Body=content.encode("utf-8"), ContentType="text/plain")
        return f"Uploaded {len(content)} characters to s3://{bucket}/{key}"
    except (BotoCoreError, ClientError) as exc:
        return f"Error uploading to s3://{bucket}/{key}: {exc}"


@mcp.tool()
def download_text(bucket: str, key: str) -> str:
    """Download and return the text content of an S3 object (first 5 000 chars)."""
    try:
        s3 = get_s3_client()
        response = s3.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8", errors="replace")
        truncated = len(body) > 5000
        text = body[:5000]
        header = f"Content of s3://{bucket}/{key}"
        if truncated:
            header += f"  (showing first 5 000 of {len(body)} chars)"
        return f"{header}\n\n{text}"
    except (BotoCoreError, ClientError) as exc:
        return f"Error downloading s3://{bucket}/{key}: {exc}"


@mcp.tool()
def delete_object(bucket: str, key: str) -> str:
    """Delete an object from S3."""
    try:
        s3 = get_s3_client()
        s3.delete_object(Bucket=bucket, Key=key)
        return f"Deleted s3://{bucket}/{key}"
    except (BotoCoreError, ClientError) as exc:
        return f"Error deleting s3://{bucket}/{key}: {exc}"


@mcp.tool()
def get_presigned_url(bucket: str, key: str, expiration: int = 3600) -> str:
    """Generate a presigned URL for temporary access to an S3 object."""
    try:
        s3 = get_s3_client()
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expiration,
        )
        return f"Presigned URL (expires in {expiration}s):\n{url}"
    except (BotoCoreError, ClientError) as exc:
        return f"Error generating presigned URL: {exc}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
