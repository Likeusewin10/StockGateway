"""Authenticated read-only downloads from the local downloads directory."""
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from stocksdk.security import require_key

ROOT = Path(__file__).resolve().parent.parent
DOWNLOADS_DIR = (ROOT / "downloads").resolve()

router = APIRouter(prefix="/downloads", tags=["文件下载"])


@router.get("/{filename}")
def download_file(filename: str, _=Depends(require_key)):
    """Return a file directly under downloads/ after API-key authentication."""
    if Path(filename).name != filename or filename in {"", ".", ".."}:
        raise HTTPException(404, "文件不存在")

    path = (DOWNLOADS_DIR / filename).resolve()
    if path.parent != DOWNLOADS_DIR or not path.is_file():
        raise HTTPException(404, "文件不存在")

    return FileResponse(path, filename=filename, media_type="application/octet-stream")
