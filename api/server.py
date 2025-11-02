"""
Optional FastAPI backend for Vector Explorer
Provides a REST API to serve vector data from FAISS and Chroma databases
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python.faiss_adapter import load_faiss_vectors
from python.chroma_adapter import load_chroma_vectors

app = FastAPI(
    title="Vector Explorer API",
    description="REST API for exploring FAISS and Chroma vector databases",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VectorRecord(BaseModel):
    id: str
    vector: List[float]
    text: str
    source: str
    metadata: Optional[Dict[str, Any]] = {}


class VectorDataResponse(BaseModel):
    type: str
    count: int
    dimension: int
    total_vectors: Optional[int] = None
    vectors: List[VectorRecord]


class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Vector Explorer API",
        "version": "1.0.0",
        "endpoints": {
            "/": "This help message",
            "/health": "Health check",
            "/api/faiss": "Load FAISS vector database",
            "/api/chroma": "Load Chroma vector database",
            "/api/detect": "Auto-detect and load database"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/api/faiss", response_model=VectorDataResponse)
async def load_faiss(
    path: str = Query(..., description="Path to FAISS index file or directory"),
    max_records: int = Query(1000, description="Maximum number of records to return", ge=1, le=10000)
):
    """
    Load vectors from FAISS database
    
    Args:
        path: Path to .faiss index file or directory containing index.faiss
        max_records: Maximum number of vectors to return (default: 1000)
    
    Returns:
        VectorDataResponse with loaded vectors
    """
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Path not found: {path}")
    
    result = load_faiss_vectors(path, max_records)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.get("/api/chroma", response_model=VectorDataResponse)
async def load_chroma(
    path: str = Query(..., description="Path to Chroma database directory"),
    max_records: int = Query(1000, description="Maximum number of records to return", ge=1, le=10000)
):
    """
    Load vectors from Chroma database
    
    Args:
        path: Path to Chroma database directory
        max_records: Maximum number of vectors to return (default: 1000)
    
    Returns:
        VectorDataResponse with loaded vectors
    """
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Path not found: {path}")
    
    if not os.path.isdir(path):
        raise HTTPException(status_code=400, detail=f"Path is not a directory: {path}")
    
    result = load_chroma_vectors(path, max_records)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.get("/api/detect", response_model=VectorDataResponse)
async def detect_and_load(
    path: str = Query(..., description="Path to vector database"),
    max_records: int = Query(1000, description="Maximum number of records to return", ge=1, le=10000)
):
    """
    Auto-detect database type and load vectors
    
    Args:
        path: Path to vector database (file or directory)
        max_records: Maximum number of vectors to return (default: 1000)
    
    Returns:
        VectorDataResponse with loaded vectors
    """
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Path not found: {path}")
    
    # Detect database type
    if os.path.isfile(path):
        if path.endswith('.faiss') or path.endswith('.index'):
            result = load_faiss_vectors(path, max_records)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    elif os.path.isdir(path):
        # Check for Chroma
        if os.path.exists(os.path.join(path, 'chroma.sqlite3')):
            result = load_chroma_vectors(path, max_records)
        # Check for FAISS
        elif os.path.exists(os.path.join(path, 'index.faiss')):
            result = load_faiss_vectors(path, max_records)
        else:
            raise HTTPException(
                status_code=400,
                detail="Could not detect database type. Looking for chroma.sqlite3 or index.faiss"
            )
    else:
        raise HTTPException(status_code=400, detail="Invalid path")
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Vector Explorer API...")
    print("📚 Documentation available at: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/health")
    print("\n📝 Example usage:")
    print("   curl 'http://localhost:8000/api/faiss?path=/path/to/index.faiss'")
    print("   curl 'http://localhost:8000/api/chroma?path=/path/to/chroma_db'")
    print("   curl 'http://localhost:8000/api/detect?path=/path/to/db'")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
