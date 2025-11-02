# 🚀 Vector Explorer Setup Guide

Complete guide to setting up and running the Vector Explorer VS Code extension.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Python Setup](#python-setup)
- [Building the Extension](#building-the-extension)
- [Running the Extension](#running-the-extension)
- [Creating Sample Data](#creating-sample-data)
- [Optional API Server](#optional-api-server)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Node.js** (v18 or higher): [Download](https://nodejs.org/)
- **Python** (3.8 or higher): [Download](https://www.python.org/)
- **Visual Studio Code**: [Download](https://code.visualstudio.com/)
- **Git**: [Download](https://git-scm.com/)

### Verify Installations
```bash
node --version    # Should show v18.x.x or higher
npm --version     # Should show 9.x.x or higher
python --version  # Should show 3.8.x or higher
code --version    # Should show VS Code version
```

---

## Installation

### 1. Clone or Navigate to the Project
```bash
cd "c:\Users\gitaram.kanawade\Projects\Gen-AI\Genai-POC\vscodeextension-readvecordb"
```

### 2. Install Node.js Dependencies
```bash
npm install
```

This will install:
- TypeScript compiler
- Webpack and loaders
- VS Code extension API types
- ESLint and other dev tools

---

## Python Setup

### 1. Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Python Dependencies
```bash
pip install -r python/requirements.txt
```

Or install individually:
```bash
pip install faiss-cpu>=1.7.4
pip install chromadb>=0.4.0
pip install numpy>=1.24.0
```

### 3. Verify Python Packages
```bash
python -c "import faiss; print('FAISS:', faiss.__version__)"
python -c "import chromadb; print('Chroma:', chromadb.__version__)"
python -c "import numpy; print('NumPy:', numpy.__version__)"
```

### 4. Test Python Adapters
```bash
# Test FAISS adapter
python python/faiss_adapter.py

# Test Chroma adapter
python python/chroma_adapter.py
```

---

## Building the Extension

### Development Build
```bash
# Compile TypeScript
npm run compile

# Or watch mode (auto-recompile on changes)
npm run watch
```

### Production Build
```bash
npm run package
```

This creates optimized bundle in `dist/extension.js`.

---

## Running the Extension

### Method 1: Using F5 (Recommended for Development)

1. Open the project in VS Code:
   ```bash
   code .
   ```

2. Press `F5` or select **Run > Start Debugging**

3. A new "Extension Development Host" window will open

4. In the new window:
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type: `Vector Explorer: Open Vector Database`
   - Select a database file/folder

### Method 2: Using npm script
```bash
npm run dev
```
Then press F5 in VS Code.

### Method 3: Manual Launch
1. Build the extension:
   ```bash
   npm run compile
   ```

2. Open VS Code Extension Dev Host:
   - Press F5 in VS Code
   - Or: Run > Start Debugging

---

## Creating Sample Data

### Generate Sample FAISS Database

```bash
# Using the provided script
python examples/create_sample_faiss.py
```

This creates:
- `examples/sample_faiss/index.faiss` - FAISS index with 100 vectors
- `examples/sample_faiss/metadata.json` - Text chunks and metadata

### Generate Sample Chroma Database

```bash
# Using the provided script
python examples/create_sample_chroma.py
```

This creates:
- `examples/sample_chroma/` - Chroma database with 100 documents

### Test with Sample Data

1. Run the extension (F5)
2. In the Extension Development Host window:
   - `Ctrl+Shift+P` → `Vector Explorer: Open Vector Database`
   - Navigate to `examples/sample_faiss/index.faiss` or `examples/sample_chroma/`
3. The Vector Explorer panel should open with the sample data

---

## Optional API Server

The project includes a FastAPI backend for serving vector data via REST API.

### Install API Dependencies

```bash
pip install -r api/requirements.txt
```

Or:
```bash
pip install fastapi uvicorn[standard] pydantic
```

### Run the API Server

```bash
python api/server.py
```

The server will start at: `http://localhost:8000`

### API Documentation

Visit: `http://localhost:8000/docs` for interactive API documentation

### Example API Usage

```bash
# Health check
curl http://localhost:8000/health

# Load FAISS database
curl "http://localhost:8000/api/faiss?path=examples/sample_faiss/index.faiss&max_records=10"

# Load Chroma database
curl "http://localhost:8000/api/chroma?path=examples/sample_chroma&max_records=10"

# Auto-detect and load
curl "http://localhost:8000/api/detect?path=examples/sample_faiss/index.faiss"
```

---

## Troubleshooting

### Issue: "Cannot find module 'vscode'"

**Solution**: Install dependencies and compile:
```bash
npm install
npm run compile
```

### Issue: "Python not found" or "python is not recognized"

**Solution**: 
1. Ensure Python is in your PATH
2. Or configure Python path in VS Code settings:
   ```json
   {
     "vectorExplorer.pythonPath": "C:\\Python39\\python.exe"
   }
   ```

### Issue: "ModuleNotFoundError: No module named 'faiss'"

**Solution**: Install FAISS:
```bash
pip install faiss-cpu
```

### Issue: "ModuleNotFoundError: No module named 'chromadb'"

**Solution**: Install ChromaDB:
```bash
pip install chromadb
```

### Issue: Extension doesn't show in Extension Development Host

**Solution**:
1. Ensure you're opening the Extension Development Host (new window)
2. Check if `dist/extension.js` exists
3. Rebuild: `npm run compile`
4. Check Output panel for errors

### Issue: "Failed to load vector database"

**Solutions**:
- Verify the database file/folder exists
- Check Python adapter can run directly:
  ```bash
  python python/faiss_adapter.py path/to/index.faiss
  ```
- Check for proper metadata.json file for FAISS
- Ensure database format is correct

### Issue: WebView doesn't display data

**Solutions**:
1. Open Developer Tools in Extension Dev Host:
   - `Help > Toggle Developer Tools`
2. Check Console for JavaScript errors
3. Verify `media/main.js` and `media/main.css` exist
4. Rebuild: `npm run compile`

### Issue: "FAISS index type doesn't support reconstruction"

**Solution**: Create FAISS index with `IndexFlatL2` or `IndexFlatIP`:
```python
import faiss
dimension = 1536
index = faiss.IndexFlatL2(dimension)  # Supports reconstruction
```

---

## Development Workflow

### 1. Make Code Changes
Edit files in:
- `src/` - TypeScript source
- `python/` - Python adapters
- `media/` - WebView UI

### 2. Rebuild
```bash
npm run compile
```

Or use watch mode:
```bash
npm run watch
```

### 3. Test in Extension Dev Host
Press `F5` to launch new window with updated extension

### 4. Check for Errors
- Terminal output during build
- Output panel in VS Code
- Developer Tools Console in Extension Dev Host

---

## Project Structure Overview

```
vscodeextension-readvecordb/
├── src/                    # TypeScript source
│   ├── extension.ts        # Main entry point
│   ├── panels/            # WebView panels
│   ├── services/          # Business logic
│   ├── types/             # Type definitions
│   └── utils/             # Utilities
├── python/                 # Python backend
│   ├── faiss_adapter.py   # FAISS loader
│   ├── chroma_adapter.py  # Chroma loader
│   └── requirements.txt   # Python deps
├── media/                  # WebView UI
│   ├── main.js            # UI logic
│   └── main.css           # Styles
├── api/                    # Optional FastAPI server
│   ├── server.py          # API server
│   └── requirements.txt   # API deps
├── examples/              # Sample data generators
│   ├── create_sample_faiss.py
│   └── create_sample_chroma.py
├── dist/                  # Compiled output
├── package.json           # Extension manifest
├── tsconfig.json          # TypeScript config
└── webpack.config.js      # Build config
```

---

## Next Steps

1. ✅ Verify all prerequisites are installed
2. ✅ Install Node.js and Python dependencies
3. ✅ Build the extension
4. ✅ Generate sample data
5. ✅ Test the extension with sample data
6. 🎯 Create your own vector databases
7. 🚀 Start exploring!

---

## Additional Resources

- [VS Code Extension API](https://code.visualstudio.com/api)
- [FAISS Documentation](https://github.com/facebookresearch/faiss/wiki)
- [Chroma Documentation](https://docs.trychroma.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## Support

For issues or questions:
- Check [Troubleshooting](#troubleshooting) section
- Review error messages in Output panel
- Test Python adapters directly
- Check browser console in Extension Dev Host

Happy Exploring! 🔍✨
