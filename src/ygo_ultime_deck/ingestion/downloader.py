"""Ingestion downloader module."""

import httpx
import aiofiles
from pathlib import Path
from rich.progress import Progress

DEFAULT_URL = "https://github.com/iconmaster5326/YGOJSON/releases/download/v1/aggregate.zip"

async def download_ygojson(target_path: Path, url: str = DEFAULT_URL) -> None:
    """Download YGOJSON zip file asynchronously.
    
    Args:
        target_path: Where to save the file.
        url: The URL to download from.
    """
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        try:
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                header_val = response.headers.get("Content-Length", "0")
                total = int(header_val) if header_val.isdigit() else 0
                
                with Progress() as progress:
                    task = progress.add_task("[cyan]Downloading YGOJSON...", total=total)
                    async with aiofiles.open(target_path, "wb") as f:
                        async for chunk in response.aiter_bytes():
                            await f.write(chunk)
                            progress.update(task, advance=len(chunk))
        except BaseException:
            if target_path.exists():
                try:
                    target_path.unlink()
                except OSError:
                    pass
            # Try to clean up the parent directory if we created it and it's empty
            if target_path.parent.exists():
                try:
                    target_path.parent.rmdir()
                except OSError:
                    pass
            raise
