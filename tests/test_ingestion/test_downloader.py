"""Tests for the YGOJSON downloader module."""

import pytest
import httpx
from typer.testing import CliRunner

from ygo_ultime_deck.ingestion.downloader import download_ygojson, DEFAULT_URL
from ygo_ultime_deck.main import app

runner = CliRunner()

@pytest.mark.asyncio
async def test_download_success(httpx_mock, tmp_path):
    """Test successful download writes content to target path."""
    mock_file_content = b"fake zip content"
    httpx_mock.add_response(url=DEFAULT_URL, content=mock_file_content, headers={"Content-Length": str(len(mock_file_content))})
    
    target_path = tmp_path / "cache" / "aggregate.zip"
    await download_ygojson(target_path=target_path)
    
    assert target_path.exists()
    assert target_path.read_bytes() == mock_file_content

@pytest.mark.asyncio
async def test_download_failure_request_error(httpx_mock, tmp_path):
    """Test that network errors during download raise RequestError."""
    httpx_mock.add_exception(httpx.RequestError("Mock network error"))
    
    target_path = tmp_path / "cache" / "aggregate.zip"
    
    with pytest.raises(httpx.RequestError):
        await download_ygojson(target_path=target_path)
        
    assert not target_path.exists()
    assert not target_path.parent.exists()

@pytest.mark.asyncio
async def test_download_failure_http_error(httpx_mock, tmp_path):
    """Test that HTTP 404 responses raise HTTPStatusError."""
    httpx_mock.add_response(url=DEFAULT_URL, status_code=404)
    
    target_path = tmp_path / "cache" / "aggregate.zip"
    
    with pytest.raises(httpx.HTTPStatusError):
        await download_ygojson(target_path=target_path)

def test_cli_graceful_exit_on_network_error(httpx_mock):
    """Test that the CLI handles network errors gracefully with typer.Exit(1)."""
    httpx_mock.add_exception(httpx.RequestError("Mock network error"))
    
    result = runner.invoke(app, ["--update"])
    
    assert result.exit_code == 1
    assert "Erreur réseau lors du téléchargement" in result.output
