"""Test script to verify Chroma database"""
import chromadb

client = chromadb.PersistentClient(path='examples/sample_chroma')
collections = client.list_collections()

print(f"Collections found: {len(collections)}")
if collections:
    collection = collections[0]
    print(f"Collection name: {collection.name}")
    print(f"Document count: {collection.count()}")
    
    # Get a sample
    results = collection.get(limit=3, include=["documents", "metadatas"])
    print(f"\nSample documents:")
    for i, (doc, meta) in enumerate(zip(results['documents'], results['metadatas'])):
        print(f"\n{i+1}. {doc[:80]}...")
        print(f"   Metadata: {meta}")
    
    print("\n✅ Chroma database is working correctly!")
else:
    print("❌ No collections found")
