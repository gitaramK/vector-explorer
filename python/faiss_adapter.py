#!/usr/bin/env python3
"""
FAISS Vector Database Adapter
Loads FAISS index and associated metadata to extract embeddings and text chunks.
Supports both standalone FAISS indexes and LangChain FAISS indexes.
"""

import sys
import json
import os
import numpy as np
import pickle
from pathlib import Path

def load_langchain_faiss(dir_path: str, max_records: int = 1000) -> dict:
    """
    Load LangChain FAISS index with docstore from .pkl file.
    
    Args:
        dir_path: Directory containing index.faiss and index.pkl
        max_records: Maximum number of vectors to return
        
    Returns:
        Dictionary with vector data in standardized format
    """
    try:
        import faiss
    except ImportError:
        return {"error": "faiss-cpu is not installed. Please install it using: pip install faiss-cpu"}
    
    faiss_file = os.path.join(dir_path, "index.faiss")
    pkl_file = os.path.join(dir_path, "index.pkl")
    
    if not os.path.exists(faiss_file):
        return {"error": f"FAISS index file not found: {faiss_file}"}
    
    if not os.path.exists(pkl_file):
        return {"error": f"Pickle file not found: {pkl_file}"}
    
    # Load FAISS index
    try:
        index = faiss.read_index(faiss_file)
    except Exception as e:
        return {"error": f"Failed to read FAISS index: {str(e)}"}
    
    # Load pickle file (LangChain docstore)
    try:
        with open(pkl_file, 'rb') as f:
            pkl_data = pickle.load(f)
        
        # LangChain saves (docstore, index_to_docstore_id) tuple
        if isinstance(pkl_data, tuple) and len(pkl_data) >= 2:
            docstore, index_to_id = pkl_data[0], pkl_data[1]
            print(f"Loaded LangChain docstore with {len(index_to_id)} documents", file=sys.stderr)
        else:
            return {"error": "Unexpected pickle format - not a LangChain FAISS index"}
    except Exception as e:
        return {"error": f"Failed to load pickle file: {str(e)}"}
    
    # Get index info
    dimension = index.d
    total_count = min(index.ntotal, max_records)
    
    # Extract vectors
    vectors_array = np.zeros((total_count, dimension), dtype=np.float32)
    try:
        if hasattr(index, 'reconstruct'):
            for i in range(total_count):
                try:
                    vectors_array[i] = index.reconstruct(i)
                except:
                    pass
        else:
            print(f"Warning: Index type {type(index).__name__} doesn't support vector reconstruction", 
                  file=sys.stderr)
    except Exception as e:
        print(f"Warning: Failed to extract vectors: {e}", file=sys.stderr)
    
    # Build result with text from docstore
    vectors = []
    for i in range(total_count):
        vector_id = f"chunk_{i:04d}"
        text = ""
        source = ""
        metadata = {}
        
        # Get document from docstore
        try:
            if i in index_to_id:
                doc_id = index_to_id[i]
                doc = docstore.search(doc_id)
                
                if doc:
                    # LangChain Document has page_content and metadata
                    if hasattr(doc, 'page_content'):
                        text = doc.page_content
                    elif hasattr(doc, 'text'):
                        text = doc.text
                    
                    if hasattr(doc, 'metadata') and isinstance(doc.metadata, dict):
                        metadata = doc.metadata
                        # Try multiple possible source field names
                        source = metadata.get('source', 
                                            metadata.get('file', 
                                            metadata.get('path', 
                                            metadata.get('filename', ''))))
        except Exception as e:
            print(f"Warning: Failed to get document {i}: {e}", file=sys.stderr)
        
        vectors.append({
            "id": vector_id,
            "vector": vectors_array[i].tolist(),
            "text": text,
            "source": source,
            "metadata": metadata
        })
    
    return {
        "type": "faiss",
        "count": len(vectors),
        "dimension": dimension,
        "total_vectors": index.ntotal,
        "vectors": vectors
    }


def load_faiss_vectors(index_path: str, max_records: int = 1000) -> dict:
    """
    Load vectors from FAISS index and associated metadata file.
    
    Args:
        index_path: Path to .faiss index file or directory containing index.faiss
        max_records: Maximum number of vectors to return
        
    Returns:
        Dictionary with vector data in standardized format
    """
    try:
        import faiss
    except ImportError:
        return {
            "error": "faiss-cpu is not installed. Please install it using: pip install faiss-cpu"
        }
    
    # Determine paths
    if os.path.isdir(index_path):
        faiss_file = os.path.join(index_path, "index.faiss")
        pkl_file = os.path.join(index_path, "index.pkl")
        
        # Check if this is a LangChain FAISS index
        if os.path.exists(faiss_file) and os.path.exists(pkl_file):
            print(f"Detected LangChain FAISS index format", file=sys.stderr)
            return load_langchain_faiss(index_path, max_records)
        
        metadata_file = os.path.join(index_path, "metadata.json")
    else:
        faiss_file = index_path
        dir_path = os.path.dirname(faiss_file)
        pkl_file = os.path.join(dir_path, "index.pkl")
        
        # Check if this is a LangChain FAISS index
        if os.path.exists(pkl_file):
            print(f"Detected LangChain FAISS index format", file=sys.stderr)
            return load_langchain_faiss(dir_path, max_records)
        
        # Look for metadata file in same directory with multiple naming conventions
        base_path = os.path.splitext(faiss_file)[0]
        
        # Try multiple metadata file names
        metadata_candidates = [
            base_path + ".json",                    # index.json
            base_path + "_metadata.json",           # index_metadata.json
            os.path.join(dir_path, "metadata.json"), # metadata.json in same dir
            os.path.join(dir_path, "chunks.json"),   # chunks.json
            os.path.join(dir_path, "documents.json"), # documents.json
        ]
        
        metadata_file = None
        for candidate in metadata_candidates:
            if os.path.exists(candidate):
                metadata_file = candidate
                print(f"Found metadata file: {metadata_file}", file=sys.stderr)
                break
        
        if not metadata_file:
            print(f"Warning: No metadata file found. Searched for:", file=sys.stderr)
            for candidate in metadata_candidates:
                print(f"  - {candidate}", file=sys.stderr)
            print(f"Tip: Create a metadata.json file with structure:", file=sys.stderr)
            print(f'  {{"chunks": [{{"id": "...", "text": "...", "source": "..."}}]}}', file=sys.stderr)
    
    # Check if files exist
    if not os.path.exists(faiss_file):
        return {"error": f"FAISS index file not found: {faiss_file}"}
    
    # Load FAISS index
    try:
        index = faiss.read_index(faiss_file)
    except Exception as e:
        return {"error": f"Failed to read FAISS index: {str(e)}"}
    
    # Get basic index info
    dimension = index.d
    total_count = index.ntotal
    
    # Load metadata if available
    metadata = None
    if metadata_file and os.path.exists(metadata_file):
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            print(f"Successfully loaded metadata from: {metadata_file}", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Failed to load metadata: {e}", file=sys.stderr)
    else:
        print(f"No metadata available - text chunks will be empty", file=sys.stderr)
    
    # Extract vectors
    vectors = []
    count = min(total_count, max_records)
    
    try:
        # Reconstruct vectors if possible
        if hasattr(index, 'reconstruct_n'):
            # IndexFlatL2, IndexFlatIP support reconstruction
            vectors_array = np.zeros((count, dimension), dtype=np.float32)
            for i in range(count):
                try:
                    vectors_array[i] = index.reconstruct(i)
                except:
                    pass
        else:
            # For other index types, we can't reconstruct vectors
            # Create placeholder vectors
            vectors_array = np.zeros((count, dimension), dtype=np.float32)
            print(f"Warning: Index type {type(index).__name__} doesn't support vector reconstruction", 
                  file=sys.stderr)
    except Exception as e:
        print(f"Warning: Failed to extract vectors: {e}", file=sys.stderr)
        vectors_array = np.zeros((count, dimension), dtype=np.float32)
    
    # Build result
    for i in range(count):
        vector_record = {
            "id": f"chunk_{i:04d}",
            "vector": vectors_array[i].tolist(),
            "text": "",
            "source": "",
            "metadata": {}
        }
        
        # Add metadata if available
        if metadata:
            if isinstance(metadata, dict):
                # Check different possible metadata structures
                if "chunks" in metadata and isinstance(metadata["chunks"], list):
                    if i < len(metadata["chunks"]):
                        chunk = metadata["chunks"][i]
                        vector_record["id"] = chunk.get("id", vector_record["id"])
                        vector_record["text"] = chunk.get("text", "")
                        vector_record["source"] = chunk.get("source", "")
                        vector_record["metadata"] = chunk.get("metadata", {})
                elif "documents" in metadata and isinstance(metadata["documents"], list):
                    if i < len(metadata["documents"]):
                        vector_record["text"] = metadata["documents"][i]
                elif "texts" in metadata and isinstance(metadata["texts"], list):
                    if i < len(metadata["texts"]):
                        vector_record["text"] = metadata["texts"][i]
                        
                # Check for sources
                if "sources" in metadata and isinstance(metadata["sources"], list):
                    if i < len(metadata["sources"]):
                        vector_record["source"] = metadata["sources"][i]
                        
                # Check for IDs
                if "ids" in metadata and isinstance(metadata["ids"], list):
                    if i < len(metadata["ids"]):
                        vector_record["id"] = metadata["ids"][i]
            elif isinstance(metadata, list):
                # Metadata is a list of records
                if i < len(metadata):
                    item = metadata[i]
                    if isinstance(item, dict):
                        vector_record["id"] = item.get("id", vector_record["id"])
                        vector_record["text"] = item.get("text", item.get("content", ""))
                        vector_record["source"] = item.get("source", item.get("file", ""))
                        vector_record["metadata"] = item.get("metadata", {})
                    elif isinstance(item, str):
                        vector_record["text"] = item
        
        vectors.append(vector_record)
    
    return {
        "type": "faiss",
        "count": count,
        "dimension": dimension,
        "total_vectors": total_count,
        "vectors": vectors
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: faiss_adapter.py <path_to_faiss_index>"}))
        sys.exit(1)
    
    index_path = sys.argv[1]
    result = load_faiss_vectors(index_path)
    
    # Output as JSON
    print(json.dumps(result, indent=2))
    
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
