# Vector Explorer - Development Quick Reference

## Quick Commands

### Development
```bash
# Install dependencies
npm install
pip install -r python/requirements.txt

# Development build (watch mode)
npm run dev

# Compile once
npm run compile

# Production build
npm run package

# Run extension
# Press F5 in VS Code
```

### Testing Python Adapters

```bash
# Test FAISS adapter
python python/faiss_adapter.py examples/sample_faiss/index.faiss

# Test Chroma adapter
python python/chroma_adapter.py examples/sample_chroma
```

### Create Sample Data

```bash
# FAISS sample
python examples/create_sample_faiss.py

# Chroma sample
python examples/create_sample_chroma.py
```

### Run API Server (Optional)

```bash
# Install API dependencies
pip install -r api/requirements.txt

# Start server
python api/server.py

# Server runs at: http://localhost:8000
# Docs at: http://localhost:8000/docs
```

## File Structure Quick Reference

```
src/
├── extension.ts              # Main entry - command registration
├── panels/
│   └── VectorExplorerPanel.ts # WebView panel manager
├── services/
│   └── VectorDBLoader.ts     # Loads FAISS/Chroma via Python
├── types/
│   └── index.ts              # TypeScript interfaces
└── utils/
    ├── csvExporter.ts        # Export functionality
    └── getNonce.ts           # Security helper

python/
├── faiss_adapter.py          # FAISS loader (prints JSON)
├── chroma_adapter.py         # Chroma loader (prints JSON)
└── requirements.txt          # faiss-cpu, chromadb, numpy

media/
├── main.js                   # WebView UI logic
└── main.css                  # WebView styling
```

## Common Tasks

### Add a New Command

1. Register in `package.json`:
```json
{
  "contributes": {
    "commands": [
      {
        "command": "vectorExplorer.myCommand",
        "title": "My Command"
      }
    ]
  }
}
```

2. Implement in `src/extension.ts`:
```typescript
const cmd = vscode.commands.registerCommand('vectorExplorer.myCommand', () => {
  // Your logic here
});
context.subscriptions.push(cmd);
```

### Modify WebView UI

1. Edit `media/main.js` for logic
2. Edit `media/main.css` for styling
3. Rebuild: `npm run compile`
4. Restart extension (F5)

### Add Support for New Vector DB

1. Create `python/newdb_adapter.py`:
```python
def load_newdb_vectors(path, max_records=1000):
    return {
        "type": "newdb",
        "count": num_vectors,
        "dimension": dimension,
        "vectors": [...]
    }
```

2. Update `src/services/VectorDBLoader.ts`:
```typescript
private detectDatabaseType(dbPath: string): 'faiss' | 'chroma' | 'newdb' | null {
  // Add detection logic
}
```

## Debugging

### Extension Host
- F5 to launch Extension Development Host
- Set breakpoints in TypeScript files
- View Output panel: View > Output > Select "Extension Host"

### WebView
- In Extension Dev Host: Help > Toggle Developer Tools
- Console tab shows WebView errors
- Can inspect WebView HTML/CSS

### Python Adapters
- Test directly from command line
- Add print statements (to stderr to avoid JSON corruption)
- Check Python errors in Extension Host output

## Environment Variables

```bash
# Python path (if not in PATH)
export PYTHON_PATH=/path/to/python

# VS Code Extension Dev
export VSCODE_DEBUG_MODE=true
```

## Useful VS Code Settings

```json
{
  // Configure Python path
  "vectorExplorer.pythonPath": "C:\\Python39\\python.exe",
  
  // Other extensions
  "python.defaultInterpreterPath": "C:\\Python39\\python.exe"
}
```

## Building for Distribution

```bash
# Install vsce
npm install -g @vscode/vsce

# Package extension
vsce package

# This creates: vector-explorer-1.0.0.vsix
```

## Performance Tips

- Limit max_records to 1000 for large databases
- Use pagination in UI (already implemented)
- Consider IndexIVF for very large FAISS indexes
- Use Chroma's filtering for targeted queries

## Common Errors

| Error | Solution |
|-------|----------|
| `Cannot find module 'vscode'` | Run `npm install` |
| `Python not found` | Add Python to PATH or configure in settings |
| `ModuleNotFoundError: faiss` | Run `pip install faiss-cpu` |
| `Failed to parse Python output` | Check Python script runs directly |
| WebView not showing | Check `media/` files exist, rebuild |

## Keyboard Shortcuts

In Extension Dev Host:
- `Ctrl+Shift+P` - Command Palette
- `Ctrl+R` - Reload Window
- `F12` - Developer Tools

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "Add my feature"

# Push and create PR
git push origin feature/my-feature
```

## Release Checklist

- [ ] Update version in `package.json`
- [ ] Update CHANGELOG.md
- [ ] Test with sample FAISS database
- [ ] Test with sample Chroma database
- [ ] Build production: `npm run package`
- [ ] Package: `vsce package`
- [ ] Test .vsix installation
- [ ] Create GitHub release
- [ ] Publish to marketplace

## Resources

- [VS Code API Docs](https://code.visualstudio.com/api)
- [WebView API](https://code.visualstudio.com/api/extension-guides/webview)
- [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki)
- [Chroma Docs](https://docs.trychroma.com/)
