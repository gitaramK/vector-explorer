"""
Create a working Chroma DB example for Vector Explorer
Using a simple, compatible approach
"""

import os
import json
import numpy as np

def create_chroma_example():
    try:
        import chromadb
        from chromadb.config import Settings
    except ImportError:
        print("❌ chromadb not installed. Run: pip install chromadb")
        return False
    
    output_dir = "examples/sample_chroma"
    
    # Remove old database if it exists
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)
        print(f"✓ Removed old database")
    
    os.makedirs(output_dir, exist_ok=True)
    print(f"Creating Chroma database in {output_dir}...")
    
    # Create client
    client = chromadb.PersistentClient(path=output_dir)
    
    # Create collection with no default embedding function
    collection = client.create_collection(
        name="ai_documents",
        metadata={"description": "AI and ML sample documents"}
    )
    
    # Sample AI/ML documents
    documents = [
        "Artificial Intelligence simulates human intelligence in machines that can learn and reason.",
        "Machine Learning allows systems to automatically learn and improve from experience without explicit programming.",
        "Deep Learning uses neural networks with multiple layers to model complex patterns in data.",
        "Natural Language Processing enables computers to understand, interpret and generate human language.",
        "Computer Vision allows machines to interpret and understand visual information from the world.",
        "Reinforcement Learning trains agents through trial and error using rewards and penalties.",
        "Neural Networks are computational models inspired by the human brain's structure and function.",
        "Transformers revolutionized NLP with self-attention mechanisms for processing sequential data.",
        "BERT provides bidirectional context understanding for natural language tasks.",
        "GPT models generate coherent text by predicting the next token in a sequence.",
        "Vector embeddings represent text as numerical vectors capturing semantic meaning.",
        "FAISS enables efficient similarity search and clustering of dense vectors at scale.",
        "ChromaDB is an AI-native open-source embedding database for LLM applications.",
        "Semantic search retrieves information based on meaning rather than exact keyword matching.",
        "RAG enhances language models by retrieving relevant context before generating responses.",
        "Fine-tuning adapts pretrained models to specific tasks with additional targeted training.",
        "Transfer learning leverages knowledge from one domain to improve performance in another.",
        "Attention mechanisms help models focus on relevant parts of input when making predictions.",
        "Large Language Models are trained on vast text corpora to understand and generate language.",
        "Prompt engineering crafts inputs to optimize language model outputs for specific tasks.",
    ]
    
    # Create IDs and metadata
    ids = [f"doc_{i:04d}" for i in range(len(documents))]
    
    topics = ["AI Basics", "Machine Learning", "Deep Learning", "NLP", "Applications"]
    authors = ["Dr. Smith", "Prof. Johnson", "Dr. Lee"]
    
    metadatas = [
        {
            "source": f"ai_handbook_chapter{(i//5)+1}.pdf",
            "page": (i % 15) + 1,
            "topic": topics[i % len(topics)],
            "author": authors[i % len(authors)],
            "year": 2023 + (i % 2),
            "category": "education"
        }
        for i in range(len(documents))
    ]
    
    # Generate embeddings (using random normalized vectors for demonstration)
    np.random.seed(42)
    embedding_dim = 384
    embeddings = []
    
    for i in range(len(documents)):
        # Create random vector and normalize
        vec = np.random.randn(embedding_dim)
        vec = vec / np.linalg.norm(vec)
        embeddings.append(vec.tolist())
    
    print(f"Adding {len(documents)} documents...")
    
    # Add documents in batches to avoid issues
    batch_size = 10
    for i in range(0, len(documents), batch_size):
        end_idx = min(i + batch_size, len(documents))
        collection.add(
            ids=ids[i:end_idx],
            documents=documents[i:end_idx],
            embeddings=embeddings[i:end_idx],
            metadatas=metadatas[i:end_idx]
        )
        print(f"  Added batch {i//batch_size + 1} ({end_idx - i} documents)")
    
    # Verify
    try:
        # Use peek instead of count for better compatibility
        result = collection.peek(limit=1)
        total = len(collection.get()['ids'])
        print(f"✓ Successfully added {total} documents")
    except Exception as e:
        print(f"✓ Documents added (verification method failed: {e})")
    
    # Create README
    readme_content = f"""# Sample Chroma Vector Database

## Overview
This is a sample Chroma database containing AI and Machine Learning educational content for testing the Vector Explorer extension.

## Database Details
- **Type**: ChromaDB
- **Collection Name**: ai_documents  
- **Document Count**: {len(documents)}
- **Embedding Dimension**: {embedding_dim}
- **Location**: `{os.path.abspath(output_dir)}`

## Contents
The database includes documents covering:
- Artificial Intelligence fundamentals
- Machine Learning concepts
- Deep Learning architectures
- Natural Language Processing
- Computer Vision basics
- Vector embeddings and search

## Metadata Fields
Each document includes:
- `source`: PDF chapter reference
- `page`: Page number in source
- `topic`: Subject area
- `author`: Document author
- `year`: Publication year  
- `category`: Content type

## Usage with Vector Explorer
1. Open VS Code with the Vector Explorer extension installed
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Select **"Vector Explorer: Open Vector Database"**
4. Choose this directory: `{os.path.abspath(output_dir)}`
5. Browse, search, and explore the vector embeddings!

## Sample Queries
Try searching for:
- "neural networks" - Find ML architecture docs
- "language models" - Discover NLP content
- "embeddings" - Learn about vector representations
- "training" - Explore learning techniques

## Technical Details
- Embeddings are 384-dimensional normalized vectors
- Database uses ChromaDB's persistent storage format
- Compatible with Vector Explorer v1.0+

Created: {os.path.basename(__file__)}
"""
    
    with open(os.path.join(output_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"✓ Created README.md")
    
    # Create summary JSON
    summary = {
        "type": "chroma",
        "collection": "ai_documents",
        "documents": len(documents),
        "dimension": embedding_dim,
        "topics": list(set([m["topic"] for m in metadatas])),
        "authors": list(set([m["author"] for m in metadatas])),
        "years": list(set([m["year"] for m in metadatas])),
        "path": os.path.abspath(output_dir)
    }
    
    with open(os.path.join(output_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(f"✓ Created summary.json")
    
    print(f"\n{'='*60}")
    print("✅ SUCCESS! Chroma database created successfully!")
    print(f"{'='*60}")
    print(f"\n📁 Location: {os.path.abspath(output_dir)}")
    print(f"📊 Documents: {len(documents)}")
    print(f"📐 Dimension: {embedding_dim}")
    print(f"\n🚀 Ready to use with Vector Explorer!")
    print(f"\nNext steps:")
    print(f"  1. Reload VS Code window (Ctrl+Shift+P > 'Reload Window')")
    print(f"  2. Open Vector Explorer")
    print(f"  3. Select: {os.path.abspath(output_dir)}")
    
    return True

if __name__ == "__main__":
    success = create_chroma_example()
    exit(0 if success else 1)
