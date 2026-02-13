"""
File handling utilities for uploads
"""
from pathlib import Path
import tempfile
import uuid
from datetime import datetime


# Upload directory in system temp
UPLOAD_DIR = Path(tempfile.gettempdir()) / "abb_sim_uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


def generate_file_id(prefix: str) -> str:
    """
    Generate unique file ID

    Args:
        prefix: Prefix for the ID (e.g., 'rapid', 'obs')

    Returns:
        Unique file ID like 'rapid_1707145800_abc123'
    """
    timestamp = int(datetime.now().timestamp())
    random_id = uuid.uuid4().hex[:8]
    return f"{prefix}_{timestamp}_{random_id}"


def save_temp_file(file_id: str, contents: bytes, extension: str) -> Path:
    """
    Save uploaded file to temp directory

    Args:
        file_id: Unique file identifier
        contents: File contents as bytes
        extension: File extension (e.g., '.mod', '.stl')

    Returns:
        Path to saved file
    """
    filepath = UPLOAD_DIR / f"{file_id}{extension}"
    filepath.write_bytes(contents)
    return filepath


def validate_rapid_file(contents: bytes) -> bool:
    """
    Basic validation for RAPID file

    Args:
        contents: File contents as bytes

    Returns:
        True if file appears to be valid text (not binary)
    """
    try:
        # RAPID files should be text (UTF-8 or ASCII)
        contents.decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False


def validate_stl_file(contents: bytes) -> bool:
    """
    Basic validation for STL file

    Args:
        contents: File contents as bytes

    Returns:
        True if file appears to be valid STL (ASCII or binary)
    """
    # Check for ASCII STL header
    if contents.startswith(b'solid'):
        return True

    # Check for binary STL header (should be 80 bytes header + data)
    if len(contents) > 84:  # Minimum binary STL size
        return True

    return False


def cleanup_old_files(max_age_hours: int = 24):
    """
    Clean up uploaded files older than max_age_hours

    Args:
        max_age_hours: Maximum age of files to keep (default 24 hours)
    """
    import time

    current_time = time.time()
    max_age_seconds = max_age_hours * 3600

    for file_path in UPLOAD_DIR.glob("*"):
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                try:
                    file_path.unlink()
                except Exception:
                    pass  # Ignore errors during cleanup
