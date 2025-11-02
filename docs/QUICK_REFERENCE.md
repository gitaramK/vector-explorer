# 🎯 Vector Explorer - Quick Reference Card

## ⚡ Getting Started (60 seconds)

```powershell
# 1. Install Python packages
pip install faiss-cpu chromadb numpy

# 2. Create sample data
python examples/create_sample_faiss.py

# 3. Press F5 in VS Code

# 4. In new window: Ctrl+Shift+P
#    Type: Vector Explorer: Open Vector Database
#    Select: examples/sample_faiss/index.faiss
```

---

## 🎮 Commands

| Command | Shortcut | Action |
|---------|----------|--------|
| Open Vector Database | `Ctrl+Shift+P` → type "Vector Explorer" | Opens database browser |
| Export as CSV | Command Palette | Exports current data to CSV |
| Refresh | Click button in UI | Reloads current database |

---

## 🖱️ UI Controls

### Main Table
- **Click column header** → Sort
- **Type in search box** → Filter by ID/text/source
- **Click text cell** → View full text
- **Click vector cell** → View full vector
- **Click 📋** → Copy text
- **Click 🔢** → Copy vector

### Navigation
- **← Previous / Next →** → Page through results
- **50 items per page** (default)

### Modals
- **Click × or outside** → Close modal
- **Click copy button** → Copy content

---

## 📊 Supported Databases

### FAISS
```
✓ .faiss or .index files
✓ Requires metadata.json in same directory
✓ Supports reconstruction for Flat indexes
```

**Expected structure:**
```
my_vectors/
├── index.faiss
└── metadata.json
```

### Chroma
```
✓ Directory with chroma.sqlite3
✓ Auto-loads first collection
✓ Retrieves embeddings + documents
```

**Expected structure:**
```
chroma_db/
└── chroma.sqlite3
```

---

## 🎨 Color Codes

| Color | Meaning | Text Length |
|-------|---------|-------------|
| 🟢 Green | Short | < 100 chars |
| 🟡 Yellow | Medium | 100-500 chars |
| 🔴 Red | Long | > 500 chars |

---

## 🔧 Common Tasks

### Create FAISS Database
```python
import faiss, numpy as np, json

# Create index
dimension = 1536
index = faiss.IndexFlatL2(dimension)
vectors = np.random.random((100, dimension)).astype('float32')
index.add(vectors)
faiss.write_index(index, "index.faiss")

# Create metadata
metadata = {
    "chunks": [
        {"id": f"chunk_{i}", "text": f"Text {i}", "source": "doc.txt"}
        for i in range(100)
    ]
}
with open("metadata.json", "w") as f:
    json.dump(metadata, f)
```

### Create Chroma Database
```python
import chromadb

client = chromadb.PersistentClient(path="./my_chroma_db")
collection = client.create_collection("docs")
collection.add(
    documents=["Text 1", "Text 2", ...],
    ids=["id1", "id2", ...],
    metadatas=[{"source": "doc.txt"}, ...]
)
```

### Export to CSV
1. Open database
2. `Ctrl+Shift+P` → "Export as CSV"
3. Choose location
4. ✓ Saved!

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Python not found | Add to PATH or set in settings |
| FAISS not installed | `pip install faiss-cpu` |
| Chroma not installed | `pip install chromadb` |
| Extension not loading | `npm run compile` then F5 |
| No data displayed | Check Python adapter runs directly |
| WebView blank | Check Developer Tools (Help → Toggle Dev Tools) |

---

## 📁 File Locations

| File | Purpose |
|------|---------|
| `src/extension.ts` | Main extension code |
| `python/faiss_adapter.py` | FAISS loader |
| `python/chroma_adapter.py` | Chroma loader |
| `media/main.js` | UI logic |
| `media/main.css` | UI styling |
| `examples/` | Sample generators |

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `F5` | Run extension |
| `Ctrl+Shift+P` | Command palette |
| `Ctrl+R` | Reload window |
| `F12` | Developer tools |
| `Esc` | Close modal |

---

## 🔍 Search Tips

- Search **ID**: Type exact or partial ID
- Search **text**: Type any word from text
- Search **source**: Type filename
- **Case insensitive**
- **Real-time filtering**

---

## 📊 Data Limits

| Item | Limit |
|------|-------|
| Max vectors per load | 1,000 |
| Items per page | 50 |
| Vector preview dimensions | 5 |
| Text preview length | 300 chars |

---

## 🚀 Performance Tips

1. **Large databases**: Use max_records parameter
2. **Slow loading**: Check Python installation
3. **Memory**: Close unused databases
4. **Search**: Be specific with queries

---

## 📞 Quick Help

| Need | Resource |
|------|----------|
| Overview | README.md |
| Setup guide | SETUP.md |
| Development | DEVELOPMENT.md |
| Architecture | ARCHITECTURE.md |
| Changes | CHANGELOG.md |

---

## 💡 Pro Tips

✨ **Did you know?**
- Click any table column to sort
- Search works across all fields
- Full vectors can be copied as JSON
- Export preserves all metadata
- Python path is configurable
- API server is optional but powerful

---

## 🎓 Common Workflows

### Research
```
1. Open vector DB
2. Search for topic keywords
3. View full text chunks
4. Copy relevant vectors
5. Export to CSV for analysis
```

### Development
```
1. Create test database
2. Open in Vector Explorer
3. Verify embeddings
4. Check metadata
5. Export for processing
```

### Debugging
```
1. Open database
2. Search by ID
3. Inspect vector values
4. Check text mapping
5. Verify source files
```

---

## 📈 Version Info

- **Current Version**: 1.0.0
- **Release Date**: 2024-11-01
- **License**: MIT
- **Node Version**: 18+
- **Python Version**: 3.8+

---

## 🔗 Useful Links

- Extension folder: `vscodeextension-readvecordb/`
- Sample data: `examples/`
- Documentation: `*.md files`
- API docs: `http://localhost:8000/docs` (when running)

---

**🎯 Remember**: Press **F5** to start exploring!

---

*Vector Explorer - Making vector databases visible* 🔍✨
