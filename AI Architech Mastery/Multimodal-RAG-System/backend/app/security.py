"""Security utilities — filename sanitization, input validation."""

import re
import uuid
from pathlib import Path


def safe_filename(filename: str) -> str:
    """Sanitize user-provided filename to prevent path traversal and special char issues.

    Strips directory components, replaces special characters, and falls back to UUID.
    """
    # Extract just the filename, no directory components
    name = Path(filename).name if filename else ""

    # Replace anything that isn't alphanumeric, dot, hyphen, or underscore
    name = re.sub(r"[^\w.\-]", "_", name)

    # Ensure it's not empty and has a reasonable length
    if not name or name.startswith("."):
        name = f"upload_{uuid.uuid4().hex[:8]}"

    # Cap filename length
    if len(name) > 200:
        ext = Path(name).suffix
        name = name[: 200 - len(ext)] + ext

    return name
