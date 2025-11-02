#!/usr/bin/env python3
"""
Complete FAISS Database Generator with HuggingFace Embeddings

This utility creates a full FAISS vector database with embeddings and metadata
from text files, demonstrating a complete use case for Vector Explorer.

Features:
- Chunks text files using semantic splitting
- Generates embeddings using HuggingFace models
- Creates FAISS index with vectors
- Generates metadata.json for text visualization
- Supports multiple input formats

Usage:
    # Create FAISS database from text files
    python create_metadata.py --create-faiss <input_files_or_dir> --output <output_dir>
    
    # Create metadata only for existing FAISS index
    python create_metadata.py --metadata-only <path_to_index.faiss> <path_to_text_chunks>

Examples:
    # Create complete FAISS DB from a directory of files
    python create_metadata.py --create-faiss ./documents --output ./my_faiss_db
    
    # Create from specific files
    python create_metadata.py --create-faiss file1.txt file2.py --output ./vectors
    
    # Just create metadata for existing index
    python create_metadata.py --metadata-only ./vectors/index.faiss ./chunks.json
"""

import sys
import json
import os
import argparse
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


# ============================================================================
# Text Chunking Functions
# ============================================================================

def chunk_text_by_tokens(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """
    Split text into chunks by token count (word-based approximation).
    
    Args:
        text: Input text to chunk
        chunk_size: Maximum tokens per chunk
        overlap: Number of tokens to overlap between chunks
        
    Returns:
        List of text chunks
    """
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks


def chunk_text_by_sentences(text: str, max_sentences: int = 5) -> List[str]:
    """
    Split text into chunks by sentences.
    
    Args:
        text: Input text to chunk
        max_sentences: Maximum sentences per chunk
        
    Returns:
        List of text chunks
    """
    import re
    
    # Simple sentence splitting (can be improved with nltk)
    sentences = re.split(r'[.!?]+\s+', text)
    chunks = []
    
    for i in range(0, len(sentences), max_sentences):
        chunk = '. '.join(sentences[i:i + max_sentences])
        if chunk.strip():
            chunks.append(chunk.strip() + '.')
    
    return chunks


def chunk_text_fixed_size(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Split text into fixed-size character chunks with overlap.
    
    Args:
        text: Input text to chunk
        chunk_size: Number of characters per chunk
        overlap: Number of characters to overlap
        
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        if chunk.strip():
            chunks.append(chunk)
        
        start += (chunk_size - overlap)
    
    return chunks


def chunk_code_by_function(code: str, language: str = 'python') -> List[Dict[str, Any]]:
    """
    Split code into chunks by functions/classes (simple version).
    
    Args:
        code: Source code to chunk
        language: Programming language
        
    Returns:
        List of chunks with metadata
    """
    import re
    
    chunks = []
    
    if language == 'python':
        # Split by function/class definitions
        pattern = r'((?:^|\n)(?:def|class)\s+\w+[^\n]*:(?:\n[ \t]+[^\n]*)*)'
        matches = list(re.finditer(pattern, code, re.MULTILINE))
        
        if matches:
            for i, match in enumerate(matches):
                chunk_text = match.group(1)
                # Extract function/class name
                name_match = re.search(r'(def|class)\s+(\w+)', chunk_text)
                name = name_match.group(2) if name_match else f"chunk_{i}"
                
                chunks.append({
                    'text': chunk_text,
                    'type': name_match.group(1) if name_match else 'code',
                    'name': name
                })
        else:
            # No functions found, chunk by size
            for i, chunk in enumerate(chunk_text_fixed_size(code, 500, 50)):
                chunks.append({
                    'text': chunk,
                    'type': 'code',
                    'name': f'chunk_{i}'
                })
    else:
        # Generic code chunking for other languages
        for i, chunk in enumerate(chunk_text_fixed_size(code, 500, 50)):
            chunks.append({
                'text': chunk,
                'type': 'code',
                'name': f'chunk_{i}'
            })
    
    return chunks


# ============================================================================
# File Reading Functions
# ============================================================================

def read_file_with_encoding(filepath: str) -> Optional[str]:
    """
    Read file with automatic encoding detection.
    
    Args:
        filepath: Path to file
        
    Returns:
        File contents or None if error
    """
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return None
    
    print(f"Warning: Could not read {filepath} with any encoding")
    return None


def process_file(filepath: str, chunk_method: str = 'fixed', chunk_size: int = 1000) -> List[Dict[str, Any]]:
    """
    Process a single file into chunks.
    
    Args:
        filepath: Path to file
        chunk_method: Chunking method ('fixed', 'tokens', 'sentences', 'code')
        chunk_size: Size parameter for chunking
        
    Returns:
        List of chunk dictionaries
    """
    content = read_file_with_encoding(filepath)
    if not content:
        return []
    
    file_ext = Path(filepath).suffix.lower()
    filename = os.path.basename(filepath)
    
    chunks_data = []
    
    # Determine if this is code
    code_extensions = ['.py', '.js', '.java', '.cpp', '.c', '.cs', '.go', '.rs', '.ts']
    is_code = file_ext in code_extensions
    
    if chunk_method == 'code' and is_code:
        chunks = chunk_code_by_function(content, language=file_ext[1:])
        for i, chunk_info in enumerate(chunks):
            chunks_data.append({
                'text': chunk_info['text'],
                'source': filepath,
                'chunk_type': chunk_info['type'],
                'chunk_name': chunk_info['name'],
                'chunk_index': i
            })
    elif chunk_method == 'tokens':
        chunks = chunk_text_by_tokens(content, chunk_size=chunk_size)
        for i, chunk in enumerate(chunks):
            chunks_data.append({
                'text': chunk,
                'source': filepath,
                'chunk_index': i
            })
    elif chunk_method == 'sentences':
        chunks = chunk_text_by_sentences(content, max_sentences=chunk_size)
        for i, chunk in enumerate(chunks):
            chunks_data.append({
                'text': chunk,
                'source': filepath,
                'chunk_index': i
            })
    else:  # fixed size
        chunks = chunk_text_fixed_size(content, chunk_size=chunk_size, overlap=chunk_size // 10)
        for i, chunk in enumerate(chunks):
            chunks_data.append({
                'text': chunk,
                'source': filepath,
                'chunk_index': i
            })
    
    print(f"  Processed {filename}: {len(chunks_data)} chunks")
    return chunks_data


# ============================================================================
# Embedding Generation
# ============================================================================

def generate_embeddings_huggingface(texts: List[str], model_name: str = 'sentence-transformers/all-MiniLM-L6-v2') -> np.ndarray:
    """
    Generate embeddings using HuggingFace sentence transformers.
    
    Args:
        texts: List of text strings to embed
        model_name: HuggingFace model name
        
    Returns:
        Numpy array of embeddings
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("\nError: sentence-transformers not installed.")
        print("Install with: pip install sentence-transformers")
        sys.exit(1)
    
    print(f"\nLoading HuggingFace model: {model_name}")
    model = SentenceTransformer(model_name)
    
    print(f"Generating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    
    print(f"Generated embeddings shape: {embeddings.shape}")
    return embeddings


def generate_embeddings_openai(texts: List[str], model: str = 'text-embedding-3-small', api_key: Optional[str] = None) -> np.ndarray:
    """
    Generate embeddings using OpenAI API.
    
    Args:
        texts: List of text strings to embed
        model: OpenAI embedding model
        api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        
    Returns:
        Numpy array of embeddings
    """
    try:
        import openai
    except ImportError:
        print("\nError: openai not installed.")
        print("Install with: pip install openai")
        sys.exit(1)
    
    if api_key:
        openai.api_key = api_key
    elif not os.getenv('OPENAI_API_KEY'):
        print("\nError: OpenAI API key not found.")
        print("Set OPENAI_API_KEY environment variable or pass --api-key")
        sys.exit(1)
    
    print(f"\nGenerating OpenAI embeddings for {len(texts)} chunks...")
    embeddings = []
    
    # OpenAI has rate limits, process in batches
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        print(f"  Processing batch {i // batch_size + 1}/{(len(texts) + batch_size - 1) // batch_size}")
        
        response = openai.embeddings.create(
            model=model,
            input=batch
        )
        
        batch_embeddings = [item.embedding for item in response.data]
        embeddings.extend(batch_embeddings)
    
    embeddings_array = np.array(embeddings, dtype=np.float32)
    print(f"Generated embeddings shape: {embeddings_array.shape}")
    return embeddings_array


# ============================================================================
# FAISS Database Creation
# ============================================================================

def create_faiss_database(
    chunks: List[Dict[str, Any]],
    embeddings: np.ndarray,
    output_dir: str,
    index_type: str = 'flat'
) -> None:
    """
    Create FAISS index and metadata files.
    
    Args:
        chunks: List of chunk dictionaries with text and metadata
        embeddings: Numpy array of embeddings
        output_dir: Output directory for FAISS files
        index_type: FAISS index type ('flat', 'ivf', 'hnsw')
    """
    try:
        import faiss
    except ImportError:
        print("\nError: faiss-cpu not installed.")
        print("Install with: pip install faiss-cpu")
        sys.exit(1)
    
    os.makedirs(output_dir, exist_ok=True)
    
    dimension = embeddings.shape[1]
    n_vectors = embeddings.shape[0]
    
    print(f"\nCreating FAISS index...")
    print(f"  Dimension: {dimension}")
    print(f"  Vectors: {n_vectors}")
    print(f"  Index type: {index_type}")
    
    # Create FAISS index
    if index_type == 'flat':
        index = faiss.IndexFlatL2(dimension)
    elif index_type == 'ivf':
        quantizer = faiss.IndexFlatL2(dimension)
        n_clusters = min(100, n_vectors // 10)
        index = faiss.IndexIVFFlat(quantizer, dimension, n_clusters)
        print(f"  Training IVF index with {n_clusters} clusters...")
        index.train(embeddings)
    elif index_type == 'hnsw':
        index = faiss.IndexHNSWFlat(dimension, 32)
    else:
        print(f"Unknown index type: {index_type}, using flat")
        index = faiss.IndexFlatL2(dimension)
    
    # Add vectors
    print("  Adding vectors to index...")
    index.add(embeddings)
    
    # Save FAISS index
    index_path = os.path.join(output_dir, 'index.faiss')
    faiss.write_index(index, index_path)
    print(f"✓ Saved FAISS index: {index_path}")
    
    # Create metadata
    metadata = {
        'chunks': [
            {
                'id': f"chunk_{i:04d}",
                'text': chunk['text'],
                'source': chunk.get('source', ''),
                'metadata': {k: v for k, v in chunk.items() if k not in ['text', 'source']}
            }
            for i, chunk in enumerate(chunks)
        ],
        'total': len(chunks),
        'dimension': dimension,
        'index_type': index_type,
        'created_at': datetime.now().isoformat()
    }
    
    # Save metadata
    metadata_path = os.path.join(output_dir, 'metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved metadata: {metadata_path}")
    
    # Create summary
    summary = {
        'total_chunks': len(chunks),
        'dimension': dimension,
        'index_type': index_type,
        'created_at': datetime.now().isoformat(),
        'files_processed': len(set(chunk.get('source', '') for chunk in chunks))
    }
    
    summary_path = os.path.join(output_dir, 'summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    print(f"✓ Saved summary: {summary_path}")
    
    print(f"\n🎉 FAISS database created successfully!")
    print(f"📁 Location: {output_dir}")
    print(f"📊 Total vectors: {n_vectors}")
    print(f"📐 Dimension: {dimension}")
    print(f"\n💡 Open this in Vector Explorer to visualize your embeddings!")


# ============================================================================
# Legacy Metadata-Only Function
# ============================================================================, Optional


def read_text_chunks(input_path: str) -> List[Dict[str, Any]]:
    """Read text chunks from various file formats (legacy function)."""
    chunks = []
    
    with open(input_path, 'r', encoding='utf-8') as f:
        # Try to parse as JSON first
        try:
            data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                for i, item in enumerate(data):
                    if isinstance(item, str):
                        chunks.append({
                            'id': f'chunk_{i:04d}',
                            'text': item,
                            'source': input_path
                        })
                    elif isinstance(item, dict):
                        chunk = {
                            'id': item.get('id', f'chunk_{i:04d}'),
                            'text': item.get('text', item.get('content', item.get('document', ''))),
                            'source': item.get('source', item.get('file', input_path))
                        }
                        # Add any additional metadata
                        for key, value in item.items():
                            if key not in ['id', 'text', 'content', 'document', 'source', 'file']:
                                chunk[key] = value
                        chunks.append(chunk)
            elif isinstance(data, dict):
                # Handle nested structures
                if 'chunks' in data:
                    return read_text_chunks_from_list(data['chunks'], input_path)
                elif 'documents' in data:
                    return read_text_chunks_from_list(data['documents'], input_path)
                elif 'texts' in data:
                    return read_text_chunks_from_list(data['texts'], input_path)
        except json.JSONDecodeError:
            # Not JSON, treat as text file with one chunk per line
            f.seek(0)  # Reset file pointer
            for i, line in enumerate(f):
                line = line.strip()
                if line:
                    chunks.append({
                        'id': f'chunk_{i:04d}',
                        'text': line,
                        'source': input_path
                    })
    
    return chunks


def read_text_chunks_from_list(items: List[Any], source: str) -> List[Dict[str, Any]]:
    """Convert a list of items to standardized chunk format."""
    chunks = []
    for i, item in enumerate(items):
        if isinstance(item, str):
            chunks.append({
                'id': f'chunk_{i:04d}',
                'text': item,
                'source': source
            })
        elif isinstance(item, dict):
            chunk = {
                'id': item.get('id', f'chunk_{i:04d}'),
                'text': item.get('text', item.get('content', item.get('document', ''))),
                'source': item.get('source', item.get('file', source))
            }
            # Add any additional metadata
            for key, value in item.items():
                if key not in ['id', 'text', 'content', 'document', 'source', 'file']:
                    chunk[key] = value
            chunks.append(chunk)
    return chunks


def create_metadata_only(faiss_path: str, text_chunks_path: str):
    """Create metadata.json file next to existing FAISS index (legacy mode)."""
    
    # Determine output path
    if os.path.isdir(faiss_path):
        output_path = os.path.join(faiss_path, 'metadata.json')
    else:
        dir_path = os.path.dirname(faiss_path)
        output_path = os.path.join(dir_path, 'metadata.json')
    
    # Read text chunks
    print(f"Reading text chunks from: {text_chunks_path}")
    chunks = read_text_chunks(text_chunks_path)
    print(f"Found {len(chunks)} text chunks")
    
    # Create metadata structure
    metadata = {
        'chunks': chunks,
        'total': len(chunks),
        'source_file': text_chunks_path,
        'created_at': datetime.now().isoformat()
    }
    
    # Write metadata file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Created metadata file: {output_path}")
    print(f"✓ Total chunks: {len(chunks)}")
    
    # Show preview of first chunk
    if chunks:
        first_chunk = chunks[0]
        print(f"\nFirst chunk preview:")
        print(f"  ID: {first_chunk['id']}")
        print(f"  Text: {first_chunk['text'][:100]}...")
        print(f"  Source: {first_chunk['source']}")


# ============================================================================
# Main CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Create FAISS vector database with HuggingFace embeddings',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create complete FAISS database from directory
  python create_metadata.py --create-faiss ./documents --output ./my_vectors
  
  # Create from specific files with custom chunking
  python create_metadata.py --create-faiss file1.txt file2.py --output ./vectors --chunk-method code
  
  # Use OpenAI embeddings instead
  python create_metadata.py --create-faiss ./docs --output ./vectors --embedding-provider openai
  
  # Create metadata only for existing FAISS index (legacy mode)
  python create_metadata.py --metadata-only ./vectors/index.faiss ./chunks.json
  
  # Quick example with sample data
  python create_metadata.py --example
        """
    )
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group(required=False)
    mode_group.add_argument('--create-faiss', nargs='+', metavar='FILES',
                           help='Create complete FAISS database from files/directory')
    mode_group.add_argument('--metadata-only', nargs=2, metavar=('FAISS_PATH', 'CHUNKS_FILE'),
                           help='Create metadata.json only for existing FAISS index')
    mode_group.add_argument('--example', action='store_true',
                           help='Create example FAISS database with sample data')
    
    # Options for --create-faiss mode
    parser.add_argument('--output', '-o', help='Output directory for FAISS database')
    parser.add_argument('--chunk-method', choices=['fixed', 'tokens', 'sentences', 'code'],
                       default='fixed', help='Text chunking method (default: fixed)')
    parser.add_argument('--chunk-size', type=int, default=1000,
                       help='Chunk size parameter (default: 1000)')
    parser.add_argument('--embedding-provider', choices=['huggingface', 'openai'],
                       default='huggingface', help='Embedding provider (default: huggingface)')
    parser.add_argument('--model', help='Model name (HuggingFace or OpenAI)')
    parser.add_argument('--index-type', choices=['flat', 'ivf', 'hnsw'],
                       default='flat', help='FAISS index type (default: flat)')
    parser.add_argument('--api-key', help='API key for OpenAI (or set OPENAI_API_KEY env var)')
    parser.add_argument('--file-extensions', nargs='+',
                       default=['.txt', '.md', '.py', '.js', '.java', '.cpp', '.c', '.cs', '.go'],
                       help='File extensions to process from directories')
    
    args = parser.parse_args()
    
    # Handle example mode
    if args.example:
        create_example_database()
        return
    
    # Handle metadata-only mode (legacy)
    if args.metadata_only:
        faiss_path, chunks_path = args.metadata_only
        if not os.path.exists(faiss_path):
            print(f"Error: FAISS path not found: {faiss_path}")
            sys.exit(1)
        if not os.path.exists(chunks_path):
            print(f"Error: Chunks file not found: {chunks_path}")
            sys.exit(1)
        create_metadata_only(faiss_path, chunks_path)
        return
    
    # Handle create-faiss mode
    if args.create_faiss:
        if not args.output:
            print("Error: --output is required when using --create-faiss")
            sys.exit(1)
        
        # Collect all files to process
        input_paths = args.create_faiss
        files_to_process = []
        
        for path in input_paths:
            if not os.path.exists(path):
                print(f"Warning: Path not found: {path}")
                continue
            
            if os.path.isfile(path):
                files_to_process.append(path)
            elif os.path.isdir(path):
                # Recursively find files with matching extensions
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if any(file.lower().endswith(ext) for ext in args.file_extensions):
                            files_to_process.append(os.path.join(root, file))
        
        if not files_to_process:
            print("Error: No files found to process")
            sys.exit(1)
        
        print(f"\n{'='*60}")
        print(f"FAISS Database Creation")
        print(f"{'='*60}")
        print(f"Files to process: {len(files_to_process)}")
        print(f"Chunk method: {args.chunk_method}")
        print(f"Chunk size: {args.chunk_size}")
        print(f"Embedding provider: {args.embedding_provider}")
        print(f"Index type: {args.index_type}")
        print(f"{'='*60}\n")
        
        # Process files into chunks
        print("Processing files...")
        all_chunks = []
        for filepath in files_to_process:
            chunks = process_file(filepath, args.chunk_method, args.chunk_size)
            all_chunks.extend(chunks)
        
        if not all_chunks:
            print("Error: No chunks created from files")
            sys.exit(1)
        
        print(f"\n✓ Total chunks created: {len(all_chunks)}")
        
        # Generate embeddings
        texts = [chunk['text'] for chunk in all_chunks]
        
        if args.embedding_provider == 'huggingface':
            model_name = args.model or 'sentence-transformers/all-MiniLM-L6-v2'
            embeddings = generate_embeddings_huggingface(texts, model_name)
        else:  # openai
            model_name = args.model or 'text-embedding-3-small'
            embeddings = generate_embeddings_openai(texts, model_name, args.api_key)
        
        # Create FAISS database
        create_faiss_database(all_chunks, embeddings, args.output, args.index_type)
        
        return
    
    # No mode specified, show help
    parser.print_help()


def create_example_database():
    """Create an example FAISS database with sample data."""
    print("\n" + "="*60)
    print("Creating Example FAISS Database")
    print("="*60)
    
    # Sample documents
    sample_docs = [
        "Python is a high-level, interpreted programming language known for its simplicity and readability.",
        "Machine learning is a subset of artificial intelligence that focuses on learning from data.",
        "FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering.",
        "Vector embeddings represent text as dense numerical vectors in high-dimensional space.",
        "Natural language processing enables computers to understand and generate human language.",
        "Deep learning uses neural networks with multiple layers to learn complex patterns.",
        "Transformers are a type of neural network architecture widely used in NLP tasks.",
        "Semantic search finds results based on meaning rather than exact keyword matches.",
        "HuggingFace provides pre-trained models and tools for NLP and machine learning.",
        "Vector databases enable fast similarity search across large collections of embeddings."
    ]
    
    # Create chunks
    chunks = [
        {
            'text': doc,
            'source': 'example_documents.txt',
            'chunk_index': i,
            'topic': 'AI/ML' if 'learning' in doc.lower() or 'neural' in doc.lower() else 'Technology'
        }
        for i, doc in enumerate(sample_docs)
    ]
    
    print(f"Sample documents: {len(chunks)}")
    
    # Generate embeddings
    try:
        from sentence_transformers import SentenceTransformer
        print("\nGenerating embeddings with HuggingFace...")
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        texts = [c['text'] for c in chunks]
        embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    except ImportError:
        print("\nWarning: sentence-transformers not installed, using random embeddings")
        print("Install with: pip install sentence-transformers")
        embeddings = np.random.randn(len(chunks), 384).astype('float32')
    
    # Create database
    output_dir = './example_faiss_db'
    create_faiss_database(chunks, embeddings, output_dir, index_type='flat')
    
    print(f"\n{'='*60}")
    print("Example database created successfully!")
    print(f"Location: {output_dir}")
    print("\nTo view in Vector Explorer:")
    print("1. Press F5 in VS Code to launch the extension")
    print("2. Run 'Vector Explorer: Open Vector Database'")
    print(f"3. Select the folder: {os.path.abspath(output_dir)}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
