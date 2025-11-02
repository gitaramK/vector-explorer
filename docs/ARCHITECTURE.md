# Vector Explorer - Architecture Overview

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         VS Code                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    Extension Host                          │ │
│  │  ┌─────────────────────────────────────────────────────┐  │ │
│  │  │              extension.ts                            │  │ │
│  │  │  - Command Registration                              │  │ │
│  │  │  - "Open Vector Database"                            │  │ │
│  │  │  - "Export CSV"                                      │  │ │
│  │  └──────────────────┬───────────────────────────────────┘  │ │
│  │                     │                                       │ │
│  │  ┌──────────────────▼──────────────────────────────────┐  │ │
│  │  │         VectorExplorerPanel.ts                       │  │ │
│  │  │  - WebView Management                                │  │ │
│  │  │  - Message Handling                                  │  │ │
│  │  │  - HTML Generation                                   │  │ │
│  │  └──────────────────┬───────────────────────────────────┘  │ │
│  │                     │                                       │ │
│  │  ┌──────────────────▼──────────────────────────────────┐  │ │
│  │  │         VectorDBLoader.ts                            │  │ │
│  │  │  - DB Type Detection                                 │  │ │
│  │  │  - Python Process Management                         │  │ │
│  │  │  - JSON Parsing                                      │  │ │
│  │  └──────────────────┬───────────────────────────────────┘  │ │
│  │                     │                                       │ │
│  └─────────────────────┼───────────────────────────────────────┘ │
│                        │                                         │
│  ┌─────────────────────▼───────────────────────────────────┐   │
│  │                  WebView (Sandboxed)                     │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │           media/main.js                            │ │   │
│  │  │  - Table Rendering                                 │ │   │
│  │  │  - Search/Filter Logic                             │ │   │
│  │  │  - Pagination                                      │ │   │
│  │  │  - Modal Dialogs                                   │ │   │
│  │  │  - User Interactions                               │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │           media/main.css                           │ │   │
│  │  │  - Dark Theme                                      │ │   │
│  │  │  - Responsive Layout                               │ │   │
│  │  │  - Animations                                      │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                               │
                               │ Spawn Process
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Python Backend                              │
│  ┌──────────────────────────┐  ┌──────────────────────────┐    │
│  │   faiss_adapter.py       │  │   chroma_adapter.py      │    │
│  │  - Load FAISS Index      │  │  - Load Chroma DB        │    │
│  │  - Read Metadata         │  │  - Extract Documents     │    │
│  │  - Reconstruct Vectors   │  │  - Get Embeddings        │    │
│  │  - Output JSON           │  │  - Output JSON           │    │
│  └────────────┬─────────────┘  └──────────────┬───────────┘    │
│               │                               │                 │
│               ▼                               ▼                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                  JSON Output                            │    │
│  │  {                                                      │    │
│  │    "type": "faiss|chroma",                              │    │
│  │    "count": 100,                                        │    │
│  │    "dimension": 1536,                                   │    │
│  │    "vectors": [                                         │    │
│  │      {                                                  │    │
│  │        "id": "chunk_001",                               │    │
│  │        "vector": [0.1, 0.2, ...],                       │    │
│  │        "text": "Sample text...",                        │    │
│  │        "source": "doc.txt"                              │    │
│  │      }                                                  │    │
│  │    ]                                                    │    │
│  │  }                                                      │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                               │
                               │ Parse & Return
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Vector Database Files                          │
│  ┌──────────────────────────┐  ┌──────────────────────────┐    │
│  │   FAISS                  │  │   Chroma                 │    │
│  │  - index.faiss           │  │  - chroma.sqlite3        │    │
│  │  - metadata.json         │  │  - collections/          │    │
│  └──────────────────────────┘  └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### Opening a Vector Database

```
User Action
    │
    ├─→ Press F5 (Launch Extension)
    │       │
    │       └─→ Extension Host loads extension.ts
    │
    ├─→ Ctrl+Shift+P → "Open Vector Database"
    │       │
    │       └─→ extension.ts: registerCommand()
    │               │
    │               └─→ VectorExplorerPanel.create()
    │                       │
    │                       └─→ VectorDBLoader.loadVectorDB()
    │                               │
    │                               ├─→ Detect DB type (FAISS/Chroma)
    │                               │
    │                               ├─→ Spawn Python process
    │                               │       │
    │                               │       └─→ faiss_adapter.py or chroma_adapter.py
    │                               │               │
    │                               │               ├─→ Load vector database
    │                               │               ├─→ Extract metadata
    │                               │               └─→ Output JSON to stdout
    │                               │
    │                               └─→ Parse JSON response
    │                                       │
    │                                       └─→ Send to WebView
    │
    └─→ WebView receives data
            │
            ├─→ Update header (type, count, dimension)
            ├─→ Store vectors in JavaScript array
            ├─→ Apply search filter (if any)
            ├─→ Sort data (if column selected)
            ├─→ Paginate (50 items per page)
            └─→ Render table rows
```

### User Interactions

```
Search
    │
    └─→ User types in search box
            │
            └─→ Filter vectors by ID/text/source
                    │
                    └─→ Update filteredVectors array
                            │
                            └─→ Re-render table

Sort
    │
    └─→ User clicks column header
            │
            └─→ Toggle sort direction (asc/desc)
                    │
                    └─→ Sort filteredVectors array
                            │
                            └─→ Re-render table

View Full Text
    │
    └─→ User clicks text cell
            │
            └─→ Open modal with full text
                    │
                    └─→ Display ID, source, length, text

Copy Text
    │
    └─→ User clicks copy button
            │
            └─→ Send message to Extension Host
                    │
                    └─→ vscode.env.clipboard.writeText()

Export CSV
    │
    └─→ User clicks Export button
            │
            └─→ Command: vectorExplorer.exportCSV
                    │
                    └─→ csvExporter.ts
                            │
                            ├─→ Convert vectors to CSV
                            └─→ Save to file
```

---

## 📦 Component Responsibilities

### TypeScript Layer (Extension Host)

| Component | Responsibility |
|-----------|----------------|
| **extension.ts** | Command registration, lifecycle management |
| **VectorExplorerPanel.ts** | WebView creation, message handling, HTML generation |
| **VectorDBLoader.ts** | Database detection, Python process spawning, JSON parsing |
| **csvExporter.ts** | CSV conversion and file saving |
| **types/index.ts** | TypeScript interfaces and types |

### Python Layer (Backend)

| Component | Responsibility |
|-----------|----------------|
| **faiss_adapter.py** | FAISS index loading, metadata parsing, vector reconstruction |
| **chroma_adapter.py** | Chroma client initialization, document retrieval, embedding extraction |

### JavaScript Layer (WebView)

| Component | Responsibility |
|-----------|----------------|
| **media/main.js** | UI logic, search, sort, pagination, modals, event handling |
| **media/main.css** | Styling, dark theme, responsive layout, animations |

---

## 🔐 Security Model

```
Extension Host (Trusted)
    │
    ├─→ Full VS Code API access
    ├─→ File system access
    ├─→ Can spawn processes
    └─→ Clipboard access
            │
            │ Sandboxed Communication
            │
            ▼
WebView (Untrusted)
    │
    ├─→ Content Security Policy enforced
    ├─→ No direct file system access
    ├─→ No direct VS Code API access
    └─→ Communication via postMessage only
```

### Content Security Policy

```
default-src 'none';
style-src ${webview.cspSource} 'unsafe-inline';
script-src 'nonce-${nonce}';
```

- No external resources
- Inline styles allowed (for dynamic styling)
- Scripts only with matching nonce
- No eval() or inline event handlers

---

## 📊 Performance Considerations

### Load Time Optimization
- Maximum 1000 vectors per load
- Lazy rendering with pagination
- Efficient JSON parsing
- Minimal DOM manipulation

### Memory Management
- Vector data stored once in JS
- Filtered/sorted arrays are views
- Modal content generated on-demand
- Proper disposal of resources

### UI Responsiveness
- 50 items per page (configurable)
- Debounced search (implicit via input event)
- Virtual scrolling candidate for future
- CSS animations on GPU

---

## 🔌 Extension Points

### Adding New Database Support

1. **Create Python Adapter**
   ```python
   # python/newdb_adapter.py
   def load_newdb_vectors(path, max_records=1000):
       return {
           "type": "newdb",
           "count": n,
           "dimension": d,
           "vectors": [...]
       }
   ```

2. **Update Type Detection**
   ```typescript
   // src/services/VectorDBLoader.ts
   private detectDatabaseType(dbPath: string) {
       // Add detection logic
   }
   ```

3. **Test**
   ```bash
   python python/newdb_adapter.py path/to/db
   ```

### Adding New Commands

1. **Register in package.json**
   ```json
   {
     "command": "vectorExplorer.newCommand",
     "title": "New Command"
   }
   ```

2. **Implement in extension.ts**
   ```typescript
   vscode.commands.registerCommand('vectorExplorer.newCommand', () => {
       // Implementation
   });
   ```

### Extending UI

1. **Add UI Element** (VectorExplorerPanel.ts)
2. **Add Styles** (media/main.css)
3. **Add Logic** (media/main.js)
4. **Handle Messages** (VectorExplorerPanel.ts)

---

## 🧪 Testing Strategy

### Unit Tests (Future)
- TypeScript utility functions
- Python adapter functions
- JSON parsing logic

### Integration Tests (Future)
- End-to-end database loading
- WebView communication
- Export functionality

### Manual Testing
- Different database types
- Large datasets
- Edge cases (empty, malformed)
- UI interactions
- Error scenarios

---

## 🚀 Deployment Pipeline

```
Development
    │
    ├─→ Write code
    ├─→ npm run compile
    └─→ F5 to test
            │
            ▼
Testing
    │
    ├─→ Test with sample data
    ├─→ Test with real databases
    └─→ Verify all features
            │
            ▼
Build
    │
    ├─→ npm run package
    └─→ vsce package
            │
            ▼
Distribution
    │
    ├─→ GitHub Release
    ├─→ VS Code Marketplace
    └─→ .vsix file
```

---

## 📈 Future Architecture

### Planned Enhancements

1. **Visualization Layer**
   - t-SNE/UMAP dimensionality reduction
   - Canvas/WebGL rendering
   - Interactive scatter plots

2. **Search Layer**
   - Similarity search
   - Vector clustering
   - Query expansion

3. **Storage Layer**
   - Cache frequent queries
   - IndexedDB for large datasets
   - Offline support

4. **API Layer** (Optional)
   - REST API for external access
   - WebSocket for real-time updates
   - Authentication/authorization

---

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Security through sandboxing
- ✅ Extensibility for new databases
- ✅ Performance through optimization
- ✅ Maintainability through modularity
