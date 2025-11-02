# Quick Reference: Vector Explorer Extension

## ✅ Extension Status: WORKING

**Compiled**: ✓ 52.8 KB bundle  
**Errors**: None (only minor linting warnings)  
**Your Database**: 1000 vectors @ 1536 dimensions loaded successfully

---

## 🔴 Current Issue

**Problem**: Text chunks showing "(0 chars)"  
**Cause**: Missing `metadata.json` file  
**Impact**: You can see vectors but not the original text

---

## 🚀 Quick Fix (Choose One)

### Method 1: Use the Utility Script ⭐ RECOMMENDED

```bash
cd vscodeextension-readvecordb
python python/create_metadata.py "path\to\index.faiss" "path\to\chunks.txt"
```

### Method 2: Manual JSON File

Create: `metadata.json` next to `index.faiss`

```json
{
  "chunks": [
    {
      "id": "chunk_0000",
      "text": "your original text here",
      "source": "source_file.py"
    }
  ]
}
```

### Method 3: Find Original Chunks

Look for files created during embedding:
- `*.txt` files with chunked text
- `*.json` files with documents
- `*.csv` files with text data
- Database tables with chunk data

---

## 📂 File Locations

**Your FAISS Index**:
```
c:\Users\gitaram.kanawade\Projects\Gen-AI\Genai-POC\Platform\repo_content\Legacy-Code-Sample\.faiss_code\code\code-primary\index.faiss
```

**Where to Put metadata.json**:
```
c:\Users\gitaram.kanawade\Projects\Gen-AI\Genai-POC\Platform\repo_content\Legacy-Code-Sample\.faiss_code\code\code-primary\metadata.json
```
*(Same directory as index.faiss)*

---

## 🔍 Verify Setup

```python
import faiss
import json
import os

# Check if index exists
index_path = r"c:\Users\gitaram.kanawade\Projects\Gen-AI\Genai-POC\Platform\repo_content\Legacy-Code-Sample\.faiss_code\code\code-primary\index.faiss"
print(f"Index exists: {os.path.exists(index_path)}")

# Check vector count
index = faiss.read_index(index_path)
print(f"Vectors in index: {index.ntotal}")

# Check if metadata exists
metadata_path = index_path.replace('.faiss', '.json')
if not os.path.exists(metadata_path):
    metadata_path = os.path.join(os.path.dirname(index_path), 'metadata.json')

print(f"Metadata exists: {os.path.exists(metadata_path)}")

if os.path.exists(metadata_path):
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    print(f"Chunks in metadata: {len(metadata.get('chunks', []))}")
```

---

## 📋 Supported Metadata Formats

| Format | Structure | Use Case |
|--------|-----------|----------|
| **Chunks** | `{"chunks": [{"id": "...", "text": "...", "source": "..."}]}` | ⭐ Best - full metadata |
| **Texts** | `{"texts": ["...", "..."], "sources": ["...", "..."]}` | Simple arrays |
| **Documents** | `{"documents": ["...", "..."]}` | Just text, no sources |
| **Flat Array** | `["...", "...", "..."]` | Simplest possible |

---

## 🎯 Expected Result After Fix

| Before | After |
|--------|-------|
| ID: chunk_0000<br>Text: (0 chars)<br>Vector: [0.234, ...] | ID: chunk_0000<br>Text: "def hello():\n  ..."<br>Vector: [0.234, ...] |

---

## 🛠️ Diagnostic Commands

**Test Python adapter directly**:
```bash
python python/faiss_adapter.py "path\to\index.faiss"
```

**Check extension output**:
1. View → Output
2. Select "Vector Explorer"
3. Look for metadata warnings

---

## 📚 Full Documentation

- **docs/CURRENT_STATUS.md** - Detailed status & solutions
- **docs/METADATA_GUIDE.md** - Complete metadata guide with examples
- **README.md** - Full extension documentation
- **python/create_metadata.py** - Utility script source code

---

## 🎉 Success Checklist

- [x] Extension compiles without errors
- [x] FAISS index loads (1000 vectors)
- [x] Vector values display correctly
- [x] Pagination works (50 per page)
- [x] Search and sort functions work
- [ ] **TODO**: Create metadata.json file
- [ ] **TODO**: Reload database to see text chunks

---

**Once metadata.json is created, you'll have a complete visual representation: text → chunks → embeddings! 🚀**
