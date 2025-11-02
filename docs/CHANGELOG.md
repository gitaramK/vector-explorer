# Changelog

All notable changes to the "Vector Explorer" extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-01

### 🎉 Initial Release

#### Added
- **Core Features**
  - Support for FAISS vector databases (.faiss files)
  - Support for Chroma vector databases (directory-based)
  - Automatic database type detection
  - Interactive WebView table for browsing vectors
  - Search functionality (filter by ID, text, or source)
  - Sortable columns (ID, Text, Source)
  - Pagination for large datasets (50 items per page)
  
- **Vector Inspection**
  - View full text chunks in modal dialog
  - View complete vector embeddings
  - Display vector dimensionality
  - Show first 5 dimensions in table preview
  
- **Data Export**
  - Export to CSV functionality
  - Copy individual text chunks
  - Copy vector arrays to clipboard
  
- **UI Features**
  - Dark theme optimized for VS Code
  - Color-coded text length indicators:
    - 🟢 Green: Short text (< 100 chars)
    - 🟡 Yellow: Medium text (100-500 chars)
    - 🔴 Red: Long text (> 500 chars)
  - Header showing database type, count, and dimension
  - Responsive modal dialogs for detailed views
  
- **Python Backend**
  - `faiss_adapter.py` - Loads FAISS indexes and metadata
  - `chroma_adapter.py` - Loads Chroma collections
  - Support for multiple metadata formats
  - Vector reconstruction for compatible FAISS indexes
  - Error handling and reporting
  
- **Commands**
  - `Vector Explorer: Open Vector Database` - Main command
  - `Vector Explorer: Export as CSV` - Export functionality
  - Context menu integration for files and folders
  
- **Documentation**
  - Comprehensive README.md with features and usage
  - Detailed SETUP.md with installation instructions
  - DEVELOPMENT.md for contributors
  - Example scripts for creating sample databases
  
- **Optional Features**
  - FastAPI REST API server for external integrations
  - API endpoints for FAISS, Chroma, and auto-detection
  - Interactive API documentation (Swagger)
  
- **Sample Data**
  - FAISS sample generator with 100 vectors
  - Chroma sample generator with 100 AI/ML documents
  - Example metadata formats
  
- **Development Tools**
  - TypeScript configuration
  - Webpack bundling
  - ESLint for code quality
  - VS Code debug configurations
  - Quick start PowerShell script

#### Technical Details
- **Frontend**: TypeScript, VS Code Extension API, WebView
- **Backend**: Python 3.8+, FAISS, ChromaDB
- **UI**: Vanilla JavaScript, CSS (no framework dependencies)
- **Build System**: Webpack, TypeScript Compiler
- **Package Dependencies**:
  - Node: @types/vscode, webpack, ts-loader, csv-stringify
  - Python: faiss-cpu, chromadb, numpy
  - Optional API: fastapi, uvicorn, pydantic

#### Supported Formats

**FAISS:**
- Index files: `.faiss`, `.index`
- Metadata: `.json` with chunks/documents/texts format
- Index types: All (reconstruction supported for Flat indexes)
- Max vectors: 1000 per load (configurable)

**Chroma:**
- Database: Directory with `chroma.sqlite3`
- Collections: Auto-loads first collection
- Features: Embeddings, documents, metadata extraction
- Max documents: 1000 per load (configurable)

#### Known Limitations
- Large databases (>1000 vectors) show first 1000 only
- FAISS indexes without reconstruction show placeholder vectors
- Single collection support for Chroma (uses first)
- Python must be available in PATH or configured

#### Browser Compatibility
- Designed for VS Code WebView (Chromium-based)
- Modern ES6+ JavaScript features
- CSS Grid and Flexbox layouts

### Security
- Content Security Policy for WebView
- Nonce-based script loading
- No external network calls from WebView
- Safe JSON parsing with error handling

---

## [Unreleased]

### Planned Features
- [ ] Support for Pinecone vector database
- [ ] Support for Milvus vector database
- [ ] Support for Weaviate vector database
- [ ] 2D/3D vector visualization with t-SNE/UMAP
- [ ] Similarity search between vectors
- [ ] Multiple collection support for Chroma
- [ ] Advanced filtering and query options
- [ ] Custom color themes
- [ ] Vector comparison view
- [ ] Batch operations on vectors
- [ ] Import from CSV functionality
- [ ] Database statistics and analytics
- [ ] Integration with embedding models
- [ ] Real-time database updates
- [ ] Vector clustering visualization
- [ ] Export to multiple formats (JSON, Parquet)

### Future Improvements
- [ ] Better error messages with suggestions
- [ ] Progress indicators for large loads
- [ ] Configurable page size
- [ ] Remember last opened database
- [ ] Recently opened databases list
- [ ] Bookmark favorite vectors
- [ ] Annotation/notes on vectors
- [ ] Collaborative features
- [ ] Performance optimizations
- [ ] Unit tests for TypeScript
- [ ] Integration tests for Python adapters
- [ ] Automated CI/CD pipeline
- [ ] Telemetry (opt-in)

---

## Version History

- **1.0.0** (2024-11-01) - Initial release with FAISS and Chroma support

---

## Contributing

See [DEVELOPMENT.md](DEVELOPMENT.md) for information on contributing to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
