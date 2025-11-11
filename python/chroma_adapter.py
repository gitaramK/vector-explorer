#!/usr/bin/env python3
"""
Chroma Vector Database Adapter
Loads Chroma database to extract embeddings, documents, and metadata.
"""

import sys
import json
import os
from pathlib import Path

def load_chroma_vectors(db_path: str, max_records: int = 1000) -> dict:
    """
    Load vectors from Chroma database.
    
    Args:
        db_path: Path to Chroma database directory
        max_records: Maximum number of vectors to return
        
    Returns:
        Dictionary with vector data in standardized format
    """
    try:
        import chromadb
        from chromadb.config import Settings
    except ImportError:
        return {
            "error": "chromadb is not installed. Please install it using: pip install chromadb"
        }
    
    # Check if path exists and is a directory
    if not os.path.exists(db_path):
        return {"error": f"Database path not found: {db_path}"}
    
    if not os.path.isdir(db_path):
        return {"error": f"Path is not a directory: {db_path}"}
    
    try:
        # Initialize Chroma client
        client = chromadb.PersistentClient(path=db_path)
        
        # Get all collections
        collections = client.list_collections()
        
        if not collections:
            return {"error": "No collections found in Chroma database"}
        
        # Use the first collection
        collection = collections[0]
        
        # Get collection info
        collection_count = collection.count()
        
        if collection_count == 0:
            return {
                "type": "chroma",
                "count": 0,
                "dimension": 0,
                "vectors": []
            }
        
        # Fetch data
        limit = min(collection_count, max_records)
        
        # Get all data from collection
        results = collection.get(
            limit=limit,
            include=["embeddings", "documents", "metadatas"]
        )
        
        # Extract dimension from first embedding
        dimension = len(results["embeddings"][0]) if results["embeddings"] is not None and len(results["embeddings"]) > 0 else 0
        
        # Build vector records
        vectors = []
        
        ids = results.get("ids", [])
        embeddings = results.get("embeddings", [])
        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])
        
        for i in range(len(ids)):
            # Convert embedding to list if it's a numpy array
            embedding = embeddings[i] if i < len(embeddings) else []
            if hasattr(embedding, 'tolist'):
                embedding = embedding.tolist()
            
            vector_record = {
                "id": ids[i] if i < len(ids) else f"chunk_{i:04d}",
                "vector": embedding,
                "text": documents[i] if i < len(documents) else "",
                "source": "",
                "metadata": metadatas[i] if i < len(metadatas) else {}
            }
            
            # Extract source from metadata if available
            if vector_record["metadata"]:
                # Common metadata keys for source
                for key in ["source", "file", "filename", "document", "doc_id"]:
                    if key in vector_record["metadata"]:
                        vector_record["source"] = str(vector_record["metadata"][key])
                        break
            
            vectors.append(vector_record)
        
        return {
            "type": "chroma",
            "count": len(vectors),
            "dimension": dimension,
            "total_vectors": collection_count,
            "collection_name": collection.name,
            "vectors": vectors
        }
        
    except Exception as e:
        return {"error": f"Failed to load Chroma database: {str(e)}"}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: chroma_adapter.py <path_to_chroma_db>"}))
        sys.exit(1)
    
    db_path = sys.argv[1]
    result = load_chroma_vectors(db_path)
    
    # Output as JSON
    print(json.dumps(result, indent=2))
    
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
