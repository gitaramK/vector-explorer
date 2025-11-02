"""
Sample script to generate a test FAISS vector database with metadata
"""

import faiss
import numpy as np
import json
import os

def create_sample_faiss_db(output_dir="examples/sample_faiss"):
    """Create a sample FAISS database for testing"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Parameters
    dimension = 1536  # OpenAI embedding dimension
    num_vectors = 100
    
    print(f"Creating FAISS database with {num_vectors} vectors of dimension {dimension}...")
    
    # Generate random embeddings (normalized for realistic behavior)
    vectors = np.random.random((num_vectors, dimension)).astype('float32')
    # Normalize vectors (common practice for embeddings)
    faiss.normalize_L2(vectors)
    
    # Create FAISS index (using Flat L2 for reconstruction support)
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)
    
    # Save index
    index_path = os.path.join(output_dir, "index.faiss")
    faiss.write_index(index, index_path)
    print(f"✓ Saved FAISS index to {index_path}")
    
    # Create sample text chunks
    sample_texts = [
        "Artificial Intelligence is transforming how we interact with technology.",
        "Machine learning models can recognize patterns in vast amounts of data.",
        "Natural Language Processing enables computers to understand human language.",
        "Deep learning has revolutionized computer vision and image recognition.",
        "Vector databases store high-dimensional embeddings for semantic search.",
        "FAISS provides efficient similarity search for large-scale applications.",
        "Embeddings capture semantic meaning in numerical form.",
        "Transformer models have become the foundation of modern NLP.",
        "Retrieval Augmented Generation combines search with language models.",
        "Semantic search goes beyond keyword matching to understand intent."
    ]
    
    # Create metadata
    metadata = {
        "chunks": []
    }
    
    for i in range(num_vectors):
        chunk = {
            "id": f"chunk_{i:04d}",
            "text": sample_texts[i % len(sample_texts)] + f" (Document {i})",
            "source": f"document_{i % 10}.txt",
            "metadata": {
                "page": (i % 50) + 1,
                "section": f"Section {(i % 5) + 1}",
                "timestamp": f"2024-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}"
            }
        }
        metadata["chunks"].append(chunk)
    
    # Save metadata
    metadata_path = os.path.join(output_dir, "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Saved metadata to {metadata_path}")
    
    # Create README for this example
    readme_content = f"""# Sample FAISS Database

This is a sample FAISS vector database for testing Vector Explorer.

## Contents
- `index.faiss`: FAISS index with {num_vectors} vectors
- `metadata.json`: Associated text chunks and metadata

## Specifications
- Vectors: {num_vectors}
- Dimension: {dimension}
- Index Type: IndexFlatL2 (supports reconstruction)

## Usage
1. Open VS Code
2. Press Ctrl+Shift+P (Cmd+Shift+P on Mac)
3. Type "Vector Explorer: Open Vector Database"
4. Select the `index.faiss` file in this directory

## Data
The database contains sample text about AI and machine learning topics,
distributed across 10 simulated documents with page and section metadata.
"""
    
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"✓ Saved README to {readme_path}")
    
    print("\n✅ Sample FAISS database created successfully!")
    print(f"📁 Location: {os.path.abspath(output_dir)}")
    print("\nTo use with Vector Explorer:")
    print("1. Open VS Code")
    print("2. Run 'Vector Explorer: Open Vector Database'")
    print(f"3. Select: {os.path.abspath(index_path)}")


if __name__ == "__main__":
    create_sample_faiss_db()
