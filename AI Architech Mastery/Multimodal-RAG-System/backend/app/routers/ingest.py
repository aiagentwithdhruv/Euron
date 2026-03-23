"""Ingestion endpoints — one per modality with file size limits and safe error handling."""

import asyncio
import logging

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from slowapi import Limiter

from app.config import settings, MAX_FILE_SIZES
from app.models.schemas import IngestResponse, TextIngestRequest
from app.processors.text_processor import process_text
from app.processors.pdf_processor import process_pdf
from app.processors.image_processor import process_image, validate_image
from app.processors.audio_processor import process_audio, validate_audio
from app.processors.video_processor import process_video, validate_video
from app.services.vectorstore import upsert_vectors
from app.rate_limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ingest", tags=["ingestion"])


def _check_file_size(contents: bytes, source_type: str, filename: str) -> None:
    """Raise 413 if file exceeds size limit."""
    max_size = MAX_FILE_SIZES.get(source_type)
    if max_size and len(contents) > max_size:
        max_mb = max_size // (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size for {source_type}: {max_mb} MB",
        )


@router.post("/text", response_model=IngestResponse)
@limiter.limit(settings.rate_limit_ingests)
async def ingest_text(request: Request, body: TextIngestRequest) -> IngestResponse:
    """Ingest raw text — chunks and embeds."""
    try:
        loop = asyncio.get_running_loop()
        vectors = await loop.run_in_executor(
            None, lambda: process_text(body.text, source_file="raw_text")
        )
        count = await loop.run_in_executor(
            None, lambda: upsert_vectors(vectors, source_type="text")
        )
        return IngestResponse(
            status="success",
            source_type="text",
            source_file="raw_text",
            chunks_ingested=count,
            message=f"Ingested {count} text chunks",
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Text ingestion failed")
        raise HTTPException(status_code=500, detail="Text ingestion failed. Please try again.")


@router.post("/pdf", response_model=IngestResponse)
@limiter.limit(settings.rate_limit_ingests)
async def ingest_pdf(request: Request, file: UploadFile = File(...)) -> IngestResponse:
    """Ingest a PDF file."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf files are accepted")
    try:
        contents = await file.read()
        _check_file_size(contents, "pdf", file.filename)
        loop = asyncio.get_running_loop()
        vectors = await loop.run_in_executor(
            None, lambda: process_pdf(contents, file.filename)
        )
        count = await loop.run_in_executor(
            None, lambda: upsert_vectors(vectors, source_type="pdf")
        )
        return IngestResponse(
            status="success",
            source_type="pdf",
            source_file=file.filename,
            chunks_ingested=count,
            message=f"Ingested {count} chunks from {file.filename}",
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("PDF ingestion failed: %s", file.filename)
        raise HTTPException(status_code=500, detail="PDF ingestion failed. Please try again.")


@router.post("/image", response_model=IngestResponse)
@limiter.limit(settings.rate_limit_ingests)
async def ingest_image(request: Request, file: UploadFile = File(...)) -> IngestResponse:
    """Ingest an image file (PNG, JPEG)."""
    if not file.filename or not validate_image(file.filename):
        raise HTTPException(status_code=400, detail="Only .png, .jpg, .jpeg files are accepted")
    try:
        contents = await file.read()
        _check_file_size(contents, "image", file.filename)
        loop = asyncio.get_running_loop()
        vectors = await loop.run_in_executor(
            None, lambda: process_image(contents, file.filename)
        )
        count = await loop.run_in_executor(
            None, lambda: upsert_vectors(vectors, source_type="image")
        )
        return IngestResponse(
            status="success",
            source_type="image",
            source_file=file.filename,
            chunks_ingested=count,
            message=f"Ingested image: {file.filename}",
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Image ingestion failed: %s", file.filename)
        raise HTTPException(status_code=500, detail="Image ingestion failed. Please try again.")


@router.post("/audio", response_model=IngestResponse)
@limiter.limit(settings.rate_limit_ingests)
async def ingest_audio(request: Request, file: UploadFile = File(...)) -> IngestResponse:
    """Ingest an audio file (MP3, WAV)."""
    if not file.filename or not validate_audio(file.filename):
        raise HTTPException(status_code=400, detail="Only .mp3, .wav files are accepted")
    try:
        contents = await file.read()
        _check_file_size(contents, "audio", file.filename)
        loop = asyncio.get_running_loop()
        vectors = await loop.run_in_executor(
            None, lambda: process_audio(contents, file.filename)
        )
        count = await loop.run_in_executor(
            None, lambda: upsert_vectors(vectors, source_type="audio")
        )
        return IngestResponse(
            status="success",
            source_type="audio",
            source_file=file.filename,
            chunks_ingested=count,
            message=f"Ingested audio: {file.filename}",
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Audio ingestion failed: %s", file.filename)
        raise HTTPException(status_code=500, detail="Audio ingestion failed. Please try again.")


@router.post("/video", response_model=IngestResponse)
@limiter.limit(settings.rate_limit_ingests)
async def ingest_video(request: Request, file: UploadFile = File(...)) -> IngestResponse:
    """Ingest a video file (MP4, MOV)."""
    if not file.filename or not validate_video(file.filename):
        raise HTTPException(status_code=400, detail="Only .mp4, .mov files are accepted")
    try:
        contents = await file.read()
        _check_file_size(contents, "video", file.filename)
        loop = asyncio.get_running_loop()
        vectors = await loop.run_in_executor(
            None, lambda: process_video(contents, file.filename)
        )
        count = await loop.run_in_executor(
            None, lambda: upsert_vectors(vectors, source_type="video")
        )
        return IngestResponse(
            status="success",
            source_type="video",
            source_file=file.filename,
            chunks_ingested=count,
            message=f"Ingested video: {file.filename}",
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Video ingestion failed: %s", file.filename)
        raise HTTPException(status_code=500, detail="Video ingestion failed. Please try again.")
