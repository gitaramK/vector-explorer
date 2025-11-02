import sys
import json
try:
    import chromadb
    client = chromadb.PersistentClient(path="examples/sample_chroma")
    collections = client.list_collections()
    if collections:
        coll = collections[0]
        # Use get() instead of count()
        all_data = coll.get(include=["embeddings", "documents", "metadatas"])
        result = {
            "type": "chroma",
            "collection_name": coll.name,
            "count": len(all_data["ids"]),
            "dimension": len(all_data["embeddings"][0]) if all_data["embeddings"] else 0,
            "vectors": [
                {
                    "id": id,
                    "vector": emb,
                    "text": doc,
                    "source": meta.get("source", ""),
                    "metadata": meta
                }
                for id, emb, doc, meta in zip(
                    all_data["ids"][:10],  # Limit to first 10
                    all_data["embeddings"][:10],
                    all_data["documents"][:10],
                    all_data["metadatas"][:10]
                )
            ]
        }
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps({"error": "No collections found"}))
except Exception as e:
    print(json.dumps({"error": str(e)}))
    sys.exit(1)
