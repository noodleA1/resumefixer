"""
Resume-Job Analyzer & Optimizer Backend
Main FastAPI application entry point
"""

import os
import sys
import socket
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import uvicorn

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

# Global variables for spaCy model
nlp_model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global nlp_model
    
    # Startup
    logger.info("Starting Resume Analyzer Backend...")
    
    try:
        import spacy
        logger.info("Loading spaCy model...")
        nlp_model = spacy.load("en_core_web_sm")
        logger.info("spaCy model loaded successfully")
    except OSError as e:
        logger.error(f"Failed to load spaCy model: {e}")
        logger.info("Please install the model: python -m spacy download en_core_web_sm")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error loading spaCy: {e}")
        sys.exit(1)
    
    yield
    
    # Shutdown
    logger.info("Shutting down Resume Analyzer Backend...")


# Create FastAPI app
app = FastAPI(
    title="Resume Analyzer API",
    description="Backend API for Resume-Job Analyzer & Optimizer",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Resume Analyzer Backend",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    global nlp_model
    
    return {
        "status": "healthy",
        "spacy_model_loaded": nlp_model is not None,
        "model_name": "en_core_web_sm" if nlp_model else None
    }


def find_free_port():
    """Find a free port for the server"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def main():
    """Main entry point"""
    # Configure logging
    logger.remove()
    logger.add(sys.stderr, level="INFO", format="{time} | {level} | {message}")
    
    # Find available port
    port = find_free_port()
    logger.info(f"Starting server on port {port}")
    
    # Write port to file for frontend to discover
    port_file = Path("backend_port.txt")
    port_file.write_text(str(port))
    
    try:
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=port,
            log_level="info",
            reload=False
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    finally:
        # Clean up port file
        if port_file.exists():
            port_file.unlink()


if __name__ == "__main__":
    main()
