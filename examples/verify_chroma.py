"""Verify Chroma database was created correctly"""
import sys
import os

try:
    import chromadb
    print("✓ chromadb imported successfully")
    
    db_path = "examples/sample_chroma"
    if not os.path.exists(db_path):
        print(f"❌ Database path not found: {db_path}")
        sys.exit(1)
    
    print(f"✓ Database path exists: {db_path}")
    
    client = chromadb.PersistentClient(path=db_path)
    print("✓ Client created")
    
    collections = client.list_collections()
    print(f"✓ Found {len(collections)} collection(s)")
    
    if collections:
        collection = collections[0]
        print(f"✓ Collection name: {collection.name}")
        
        try:
            count = collection.count()
            print(f"✓ Document count: {count}")
            
            if count > 0:
                # Get first few documents
                results = collection.get(limit=3, include=["documents", "metadatas", "embeddings"])
                print(f"✓ Retrieved {len(results['ids'])} sample documents")
                
                for i, (id, doc, meta) in enumerate(zip(results['ids'], results['documents'], results['metadatas'])):
                    print(f"\n  Document {i+1}:")
                    print(f"    ID: {id}")
                    print(f"    Text: {doc[:60]}...")
                    print(f"    Metadata: {meta}")
                    if results['embeddings']:
                        print(f"    Embedding dimension: {len(results['embeddings'][i])}")
                
                print(f"\n✅ SUCCESS: Chroma database is fully functional with {count} documents!")
            else:
                print("⚠ Collection is empty")
        except Exception as e:
            print(f"❌ Error accessing collection: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ No collections found")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
