# Vector Explorer - Current Status & Next Steps

## ✅ What's Working

Your Vector Explorer extension is **fully functional** and can:

1. ✅ Load FAISS and Chroma vector databases
2. ✅ Display vectors (1000 items, 1536 dimensions in your case)
3. ✅ Show vector IDs (chunk_0000, chunk_0001, etc.)
4. ✅ Display vector numerical values
5. ✅ Search, sort, and paginate through results
6. ✅ Recursively search directories (including `.faiss_code` folders)
7. ✅ Handle paths with spaces correctly

## ⚠️ Current Issue: Text Chunks Showing "(0 chars)"

### Why This Happens

FAISS indexes **only store vector embeddings** (the numbers), not the original text. The text chunks need to be stored separately in a `metadata.json` file.

**Your current situation:**
- Index path: `c:\Users\gitaram.kanawade\Projects\Gen-AI\Genai-POC\Platform\repo_content\Legacy-Code-Sample\.faiss_code\code\code-primary\index.faiss`
- Vectors: ✅ 1000 vectors loaded successfully
- Text chunks: ❌ Empty because metadata.json is missing

### The Missing Link

```
Your Workflow:          What's Stored in FAISS:
┌─────────────────┐     ┌──────────────────┐
│ Original Text   │     │ Vector Numbers   │
│ "def hello():"  │ ──▶ │ [0.234, -0.567,  │
│ "print('hi')"   │     │  0.891, ...]     │
└─────────────────┘     └──────────────────┘
       ↓                        ↓
   metadata.json           index.faiss
   (missing!)              (exists!)
```

## 🔧 Solution: Create metadata.json

### Option 1: Use the Utility Script (Fastest)

If you have your original text chunks in a file:

```bash
# Navigate to extension directory
cd c:\Users\gitaram.kanawade\Projects\Gen-AI\Genai-POC\vscodeextension-readvecordb

# If chunks are in a text file (one chunk per line)
python python/create_metadata.py "c:\Users\gitaram.kanawade\Projects\Gen-AI\Genai-POC\Platform\repo_content\Legacy-Code-Sample\.faiss_code\code\code-primary\index.faiss" "path\to\your\chunks.txt"

# If chunks are in a JSON file
python python/create_metadata.py "c:\Users\gitaram.kanawade\Projects\Gen-AI\Genai-POC\Platform\repo_content\Legacy-Code-Sample\.faiss_code\code\code-primary\index.faiss" "path\to\your\chunks.json"
```

### Option 2: Manual Creation

Create a file named `metadata.json` in the same directory as your `index.faiss`:

**Location**: `c:\Users\gitaram.kanawade\Projects\Gen-AI\Genai-POC\Platform\repo_content\Legacy-Code-Sample\.faiss_code\code\code-primary\metadata.json`

**Format**:
```json
{
  "chunks": [
    {
      "id": "chunk_0000",
      "text": "Your original text for the first chunk...",
      "source": "source_file.py"
    },
    {
      "id": "chunk_0001",
      "text": "Your original text for the second chunk...",
      "source": "source_file.py"
    }
    // ... repeat for all 1000 chunks
  ]
}
```

### Option 3: Find Your Original Chunks

Your FAISS index was created from somewhere. Common locations:

1. **Check your embedding pipeline code**: Look for where `faiss.add()` or `index.add()` was called
2. **Look for text processing scripts**: Files that chunk code/documents before embedding
3. **Check for backup/cache files**: Many RAG systems save chunks before embedding
4. **Database tables**: Some systems store chunks in SQLite, PostgreSQL, etc.

### Option 4: Regenerate Metadata from Source

If you have the source code that was embedded:

```python
import json
import os

# Path to your source code
source_dir = r"c:\Users\gitaram.kanawade\Projects\Gen-AI\Genai-POC\Platform\repo_content\Legacy-Code-Sample"

chunks = []
chunk_id = 0

# Walk through all Python files
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Chunk the code (adjust size to match your embedding process)
            chunk_size = 1000  # characters per chunk
            for i in range(0, len(content), chunk_size):
                chunk_text = content[i:i+chunk_size]
                chunks.append({
                    'id': f'chunk_{chunk_id:04d}',
                    'text': chunk_text,
                    'source': filepath
                })
                chunk_id += 1

# Save metadata
output_path = r"c:\Users\gitaram.kanawade\Projects\Gen-AI\Genai-POC\Platform\repo_content\Legacy-Code-Sample\.faiss_code\code\code-primary\metadata.json"

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump({'chunks': chunks}, f, indent=2, ensure_ascii=False)

print(f"Created metadata for {len(chunks)} chunks")
```

## 📊 What You'll See After Adding Metadata

Once you create the metadata file:

| Column | Before | After |
|--------|--------|-------|
| ID | chunk_0000 | chunk_0000 |
| Text | (0 chars) | ✅ "def hello_world():\n    print('Hello!')" |
| Vector | [0.234, -0.567, ...] | [0.234, -0.567, ...] |
| Source | | ✅ "example.py" |

## 🔍 Diagnostic Output

The updated extension now provides helpful diagnostics. When you load a database, check the **Output** panel:

1. Open Output panel: `View → Output`
2. Select "Vector Explorer" from the dropdown
3. Look for messages like:

```
✓ Good: "Found metadata file: C:\...\metadata.json"
✓ Good: "Successfully loaded metadata from: C:\...\metadata.json"

⚠️ Problem: "Warning: No metadata file found. Searched for:"
⚠️ Problem: "  - C:\...\index.json"
⚠️ Problem: "  - C:\...\index_metadata.json"
⚠️ Problem: "  - C:\...\metadata.json"
⚠️ Problem: "No metadata available - text chunks will be empty"
```

## 📖 Additional Resources

Detailed guides created for you:

1. **METADATA_GUIDE.md** - Complete guide to creating and managing metadata
   - Location: `docs/METADATA_GUIDE.md`
   - Covers: All formats, common issues, best practices, complete examples

2. **create_metadata.py** - Utility script to generate metadata
   - Location: `python/create_metadata.py`
   - Usage: `python python/create_metadata.py <index.faiss> <chunks_file>`

3. **README.md** - Extension documentation
   - Location: `README.md`
   - Full extension features and usage

## 🎯 Quick Test

To verify everything is working, let's create a small test database:

```python
import faiss
import numpy as np
import json

# Create test data
dimension = 1536
test_texts = [
    "This is the first test chunk",
    "This is the second test chunk",
    "This is the third test chunk"
]

# Create random vectors
vectors = np.random.random((len(test_texts), dimension)).astype('float32')

# Create FAISS index
index = faiss.IndexFlatL2(dimension)
index.add(vectors)

# Save index
test_dir = "test_vectors"
os.makedirs(test_dir, exist_ok=True)
faiss.write_index(index, f"{test_dir}/index.faiss")

# Create metadata
metadata = {
    "chunks": [
        {"id": f"chunk_{i:04d}", "text": text, "source": "test.txt"}
        for i, text in enumerate(test_texts)
    ]
}

with open(f"{test_dir}/metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("✓ Test database created in ./test_vectors/")
print("  Open this in Vector Explorer to see text chunks!")
```

## 🚀 Next Steps

1. **Locate your original text chunks** - Check your embedding pipeline code
2. **Create metadata.json** - Use one of the methods above
3. **Reload in Vector Explorer** - Click the refresh button
4. **Verify complete visualization** - You should now see: text → chunks → embeddings

## 💡 Pro Tips

1. **Metadata structure must match vector order**: The first chunk in metadata must correspond to the first vector in the FAISS index
2. **Use UTF-8 encoding**: Especially important for code with special characters
3. **Keep metadata.json with index.faiss**: Always in the same directory
4. **Back up your metadata**: It's as important as the index itself

## ❓ Still Need Help?

If text chunks are still empty after creating metadata.json:

1. Check the Output panel for diagnostic messages
2. Verify metadata.json is in the correct location
3. Ensure chunk count matches vector count:
   ```python
   import faiss
   import json
   
   index = faiss.read_index("index.faiss")
   print(f"Vectors: {index.ntotal}")
   
   with open("metadata.json", "r") as f:
       metadata = json.load(f)
   print(f"Chunks: {len(metadata['chunks'])}")
   ```
4. Review the complete METADATA_GUIDE.md for troubleshooting steps

---

**Your extension is ready - you just need to connect the text chunks to complete the visualization! 🎉**
