"""
Simple script to generate a test Chroma vector database with manual embeddings
"""

import os
import json

def create_simple_chroma_db(output_dir="examples/sample_chroma"):
    """Create a sample Chroma database for testing"""
    
    try:
        import chromadb
        import numpy as np
    except ImportError as e:
        print(f"❌ Required package is not installed: {e}")
        print("Install with: pip install chromadb numpy")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Creating Chroma database in {output_dir}...")
    
    # Initialize Chroma client with no default embedding function
    client = chromadb.PersistentClient(path=output_dir)
    
    # Create or get collection (without embedding function to avoid onnxruntime issues)
    try:
        collection = client.get_collection(name="ai_documents")
        client.delete_collection(name="ai_documents")
    except:
        pass
    
    collection = client.create_collection(
        name="ai_documents",
        metadata={"description": "Sample AI and ML documents for testing"}
    )
    
    # Sample documents
    documents = [
        "Artificial Intelligence (AI) is the simulation of human intelligence by machines.",
        "Machine Learning is a subset of AI that enables systems to learn from data.",
        "Deep Learning uses artificial neural networks with multiple layers.",
        "Natural Language Processing (NLP) focuses on computer-human language interaction.",
        "Computer Vision enables machines to derive meaningful information from images.",
        "Reinforcement Learning is where agents learn by interacting with an environment.",
        "Neural Networks are computing systems inspired by biological neural networks.",
        "Transformers are a type of neural network architecture for NLP tasks.",
        "BERT is a pre-trained model for Natural Language Processing tasks.",
        "GPT models can generate human-like text based on context.",
        "Vector embeddings represent data as points in high-dimensional space.",
        "FAISS is a library for efficient similarity search of dense vectors.",
        "ChromaDB is an open-source embedding database for AI applications.",
        "Semantic search finds results based on meaning rather than keywords.",
        "RAG combines information retrieval with text generation.",
        "Fine-tuning adapts pre-trained models to specific tasks.",
        "Transfer learning applies knowledge from one task to another.",
        "Attention mechanisms allow models to focus on relevant input parts.",
        "Large Language Models are trained on massive amounts of text data.",
        "Prompt engineering designs inputs to get desired AI outputs.",
        "Few-shot learning enables models to learn from a small number of examples.",
        "Zero-shot learning allows models to perform tasks without training examples.",
        "Embeddings compress information into fixed-size vectors.",
        "Cosine similarity measures similarity between vectors based on angle.",
        "Dimensionality reduction helps visualize high-dimensional data.",
        "Tokenization breaks text into smaller units for processing.",
        "Hyperparameters control the learning process of models.",
        "Overfitting occurs when a model learns training data too well.",
        "Regularization prevents overfitting by adding constraints.",
        "Backpropagation trains neural networks by computing gradients.",
    ]
    
    # Create IDs
    ids = [f"doc_{i:04d}" for i in range(len(documents))]
    
    # Create metadata
    topics = ["AI Basics", "Machine Learning", "Deep Learning", "NLP", "Computer Vision"]
    
    metadatas = [
        {
            "source": f"ai_textbook_chapter_{(i // 5) + 1}.pdf",
            "page": (i % 20) + 1,
            "topic": topics[i % len(topics)],
            "author": ["Dr. Smith", "Prof. Johnson", "Dr. Lee"][i % 3],
            "year": 2023 + (i % 2)
        }
        for i in range(len(documents))
    ]
    
    # Generate simple embeddings (using random vectors for this example)
    # In a real scenario, you would use a proper embedding model
    np.random.seed(42)  # For reproducibility
    embedding_dim = 384  # Standard dimension for many embedding models
    embeddings = []
    
    for i, doc in enumerate(documents):
        # Create a simple embedding based on document length and position
        # This is just for demonstration - real embeddings would be from a model
        base_vector = np.random.randn(embedding_dim)
        # Normalize to unit length
        embedding = base_vector / np.linalg.norm(base_vector)
        embeddings.append(embedding.tolist())
    
    print(f"Adding {len(documents)} documents to collection...")
    
    try:
        # Add to collection with explicit embeddings
        collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )
        
        # Verify
        count = collection.count()
        print(f"✓ Added {count} documents to collection '{collection.name}'")
    except Exception as e:
        print(f"❌ Error adding documents: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Create README for this example
    readme_content = f"""# Sample Chroma Database

This is a sample Chroma vector database for testing Vector Explorer.

## Contents
- Chroma database with {len(documents)} AI/ML-related documents
- Pre-generated embeddings (dimension: {embedding_dim})
- Rich metadata including source, topic, author, and year

## Collection Details
- Name: ai_documents
- Documents: {len(documents)}
- Embedding dimension: {embedding_dim}

## Topics Covered
- Artificial Intelligence basics
- Machine Learning fundamentals
- Deep Learning architectures
- Natural Language Processing
- Computer Vision
- Model training concepts

## Usage with Vector Explorer
1. Open VS Code
2. Press Ctrl+Shift+P (Cmd+Shift+P on Mac)
3. Type "Vector Explorer: Open Vector Database"
4. Select the `sample_chroma` directory: {os.path.abspath(output_dir)}

## Sample Queries
Try searching for:
- "transformers" - Find documents about transformer models
- "neural networks" - Discover neural network concepts
- "training" - Locate model training information
- "embeddings" - Find embedding-related content

## Directory Structure
```
{output_dir}/
├── chroma.sqlite3          # Chroma database file
└── README.md              # This file
```

## Notes
- This database uses pre-generated embeddings for demonstration
- The embeddings are normalized vectors of dimension {embedding_dim}
- All metadata fields are searchable through the Vector Explorer
"""
    
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"✓ Saved README to {readme_path}")
    
    # Create a summary JSON file
    summary = {
        "database_type": "chroma",
        "collection_name": "ai_documents",
        "document_count": len(documents),
        "embedding_dimension": embedding_dim,
        "topics": list(set([m["topic"] for m in metadatas])),
        "authors": list(set([m["author"] for m in metadatas])),
        "years": list(set([m["year"] for m in metadatas])),
        "created_at": "2024-11-02"
    }
    
    summary_path = os.path.join(output_dir, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"✓ Saved summary to {summary_path}")
    
    print("\n✅ Sample Chroma database created successfully!")
    print(f"📁 Location: {os.path.abspath(output_dir)}")
    print("\n🔍 To use with Vector Explorer:")
    print("1. Open VS Code")
    print("2. Press Ctrl+Shift+P")
    print("3. Run 'Vector Explorer: Open Vector Database'")
    print(f"4. Select directory: {os.path.abspath(output_dir)}")
    print("\n💡 You can now browse the vector database in VS Code!")


if __name__ == "__main__":
    create_simple_chroma_db()
