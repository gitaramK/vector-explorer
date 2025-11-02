# Vector Explorer 🔍

**Vector Explorer** is a powerful VS Code extension for inspecting and visualizing vector databases. It provides an interactive interface to explore FAISS and Chroma vector databases, view embeddings, and analyze chunk mappings to original text.

## 📸 Screenshots

![Vector Explorer Interface](https://raw.githubusercontent.com/gitaramK/vector-explorer/main/images/vector-explorer-screenshot.png)

*The Vector Explorer interface showing a FAISS vector database with interactive table view, search capabilities, and vector inspection features.*

## 🚀 Quick Start

1. **Install the extension** from VS Code Marketplace
2. **Install Python dependencies**: `pip install faiss-cpu chromadb numpy`
3. **Open Command Palette** (`Ctrl+Shift+P` / `Cmd+Shift+P`)
4. **Run**: "Vector Explorer: Open Vector Database"
5. **Select** your FAISS `.faiss` file or Chroma database folder
6. **Explore** your vectors in an interactive table!

## ✨ Features

- 🗂️ **Multi-Database Support**: Works with FAISS and Chroma vector databases
- 📊 **Interactive Table View**: Browse vectors with sortable, searchable columns
- 🔎 **Advanced Search**: Filter by ID, text content, or source file
- 📝 **Full Text Preview**: View complete text chunks in a modal
- 🔢 **Vector Inspector**: Examine full vector embeddings
- 📋 **Copy Actions**: Quick copy for text and vectors
- 💾 **CSV Export**: Export vector data for external analysis
- 🎨 **Color-Coded Chunks**: Visual indicators for text length (short/medium/long)
- 📄 **Pagination**: Efficiently handle large datasets
- 🌙 **Dark Theme**: Optimized for VS Code's dark theme

## 📦 Installation

### Option 1: From VS Code Marketplace (Recommended)

1. Open VS Code
2. Go to Extensions view (`Ctrl+Shift+X` / `Cmd+Shift+X`)
3. Search for "Vector Explorer"
4. Click **Install**

### Option 2: Install from VSIX File

1. Download the `.vsix` file from the releases page
2. Open VS Code
3. Go to Extensions view (`Ctrl+Shift+X` / `Cmd+Shift+X`)
4. Click the `...` menu at the top of the Extensions view
5. Select **Install from VSIX...**
6. Choose the downloaded `.vsix` file

### Prerequisites

The extension requires Python with the following packages installed:

```bash
pip install faiss-cpu chromadb numpy
```

**Note**: Make sure Python is accessible from your command line or configure the Python path in extension settings.

## 🚀 Usage

### Opening a Vector Database

There are multiple ways to open a vector database:

1. **Command Palette**:
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type "Vector Explorer: Open Vector Database"
   - Select your FAISS index file (`.faiss`) or Chroma directory

2. **File Explorer**:
   - Right-click on a `.faiss` file or folder
   - Select "Vector Explorer: Open Vector Database"

3. **Direct Command**:
   - Use `Ctrl+Shift+P` → `Vector Explorer: Open Vector Database`

### Supported Database Formats

#### FAISS
- **Index File**: `.faiss` or `.index` file
- **Metadata File**: Accompanying `.json` file with the same base name
  
**Example structure**:
```
my_vectors/
├── index.faiss
└── metadata.json
```

**Metadata JSON format**:
```json
{
  "chunks": [
    {
      "id": "chunk_001",
      "text": "Your text content here",
      "source": "document.txt",
      "metadata": {}
    }
  ]
}
```

Alternative metadata formats are also supported:
```json
{
  "documents": ["text1", "text2", ...],
  "sources": ["file1.txt", "file2.txt", ...],
  "ids": ["id1", "id2", ...]
}
```

#### Chroma
- **Directory**: Folder containing `chroma.sqlite3`
- Automatically loads the first collection
- Retrieves embeddings, documents, and metadata

**Example structure**:
```
chroma_db/
├── chroma.sqlite3
└── [other chroma files]
```

### Interface Overview

#### Header
- **Type**: Database type (FAISS or Chroma)
- **Count**: Number of loaded vectors
- **Dimension**: Vector dimensionality

#### Toolbar
- **Search Box**: Filter vectors by ID, text, or source
- **Refresh**: Reload the current database
- **Export CSV**: Export all data to CSV format

#### Table Columns
- **ID**: Unique identifier for each vector
- **Text Chunk**: Truncated text preview (click to see full text)
- **Vector**: First 5 dimensions (click to see full vector)
- **Source**: Origin file or document
- **Actions**: Copy text or vector buttons

#### Features
- **Sorting**: Click column headers to sort
- **Text Length Indicators**:
  - 🟢 Green: Short text (< 100 chars)
  - 🟡 Yellow: Medium text (100-500 chars)
  - 🔴 Red: Long text (> 500 chars)
- **Pagination**: Navigate through large datasets
- **Modal Views**: Detailed view for text and vectors

## 🎯 Example: Creating a Sample FAISS Database

Here's how to create a sample FAISS database for testing:

```python
import faiss
import numpy as np
import json

# Create sample embeddings
dimension = 1536  # OpenAI embedding dimension
num_vectors = 100
vectors = np.random.random((num_vectors, dimension)).astype('float32')

# Create FAISS index
index = faiss.IndexFlatL2(dimension)
index.add(vectors)

# Save index
faiss.write_index(index, "sample_vectors.faiss")

# Create metadata
metadata = {
    "chunks": [
        {
            "id": f"chunk_{i:04d}",
            "text": f"This is sample text chunk number {i}. " * 10,
            "source": f"document_{i % 10}.txt",
            "metadata": {"page": i % 50}
        }
        for i in range(num_vectors)
    ]
}

# Save metadata
with open("sample_vectors.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("Sample FAISS database created!")
```

## 🎯 Example: Creating a Sample Chroma Database

```python
import chromadb
from chromadb.config import Settings

# Initialize Chroma client
client = chromadb.PersistentClient(path="./chroma_sample_db")

# Create collection
collection = client.create_collection(
    name="sample_collection",
    metadata={"description": "Sample vector database"}
)

# Add documents
documents = [f"This is sample document number {i}. " * 20 for i in range(100)]
ids = [f"doc_{i:04d}" for i in range(100)]
metadatas = [{"source": f"file_{i % 10}.txt", "page": i % 50} for i in range(100)]

collection.add(
    documents=documents,
    ids=ids,
    metadatas=metadatas
)

print("Sample Chroma database created!")
```

## ⚙️ Configuration

### Extension Settings

You can customize the extension behavior in VS Code settings (`File` → `Preferences` → `Settings` or `Ctrl+,`):

#### Python Path
If Python is not in your system PATH, specify the full path to your Python executable:

1. Open VS Code Settings (`Ctrl+,` / `Cmd+,`)
2. Search for "Vector Explorer"
3. Set **Python Path** to your Python executable path

**Example paths**:
- Windows: `C:\Python39\python.exe`
- Mac/Linux: `/usr/local/bin/python3`

Or add to your `settings.json`:
```json
{
  "vectorExplorer.pythonPath": "/path/to/your/python"
}
```

### Workspace Settings

You can also configure settings per workspace by creating a `.vscode/settings.json` file in your project folder.

## 🐛 Troubleshooting

### Python not found

**Problem**: Extension shows "Python not found" error.

**Solutions**:
1. Install Python from [python.org](https://python.org) if not already installed
2. Ensure Python is added to your system PATH during installation
3. Configure the Python path in extension settings (see Configuration section above)
4. Restart VS Code after setting the Python path

### FAISS/Chroma not installed

**Problem**: Error messages about missing Python packages.

**Solution**:
```bash
pip install faiss-cpu chromadb numpy
```

Or if using Python 3:
```bash
pip3 install faiss-cpu chromadb numpy
```

### Metadata file not found

**Problem**: FAISS index opens but shows no data.

**Solutions**:
- Ensure your `.json` metadata file has the same base name as the `.faiss` file
  - Example: `index.faiss` → `index.json`
- Or place a `metadata.json` file in the same directory
- Check that the metadata JSON file is properly formatted (see Supported Database Formats section)

### No vectors displayed

**Problem**: Database opens but table is empty.

**Solutions**:
- Verify your database contains data by checking the file size
- For FAISS: Ensure both the `.faiss` index and `.json` metadata exist
- For Chroma: Verify the directory contains `chroma.sqlite3` and collection data
- Check the VS Code Output panel (View → Output → Vector Explorer) for error messages
- Try creating a new sample database using the examples in this README

### Permission Errors

**Problem**: Cannot read database files.

**Solutions**:
- Ensure you have read permissions for the database files
- On Windows: Right-click file → Properties → Security → check permissions
- On Mac/Linux: Check file permissions with `ls -la`

### Extension Not Loading

**Problem**: Extension commands don't appear in Command Palette.

**Solutions**:
1. Check if extension is enabled in Extensions view
2. Restart VS Code
3. Check for VS Code updates
4. Reinstall the extension

## � Tips & Best Practices

### Working with Large Databases
- Use the search feature to filter vectors before browsing
- Pagination helps manage large datasets efficiently
- Export filtered results to CSV for offline analysis

### Organizing Vector Databases
- Use consistent naming for FAISS index and metadata files
- Keep related databases in dedicated folders
- Include descriptive source information in metadata

### Keyboard Shortcuts
- `Ctrl+Shift+P` / `Cmd+Shift+P`: Open Command Palette
- `Ctrl+Shift+X` / `Cmd+Shift+X`: Open Extensions view
- Use the search box to quickly filter vectors

### Performance
- The extension handles databases with thousands of vectors efficiently
- For very large databases (100k+ vectors), initial load may take a few seconds
- Consider using pagination to browse large datasets

## 🆘 Getting Help

### Support Channels
- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check the extension documentation for detailed guides
- **Community**: Join discussions on GitHub

### Before Reporting Issues
1. Check the Troubleshooting section above
2. Verify Python and required packages are installed
3. Check the VS Code Output panel for error messages
4. Try with a sample database to isolate the issue

## 🗺️ Planned Features

Future updates may include:
- Support for additional vector databases (Pinecone, Milvus, Weaviate)
- Vector similarity search capabilities
- 2D/3D visualization with t-SNE or UMAP
- Batch operations on multiple vectors
- Custom themes and UI customization
- Integration with popular embedding models
- Real-time database monitoring

## 🎓 Learning Resources

### Understanding Vector Databases
- Vector databases store high-dimensional embeddings for similarity search
- FAISS (Facebook AI Similarity Search) is optimized for efficient vector operations
- Chroma is a modern AI-native database for embedding storage

### Use Cases
- **RAG (Retrieval Augmented Generation)**: Inspect your knowledge base chunks
- **Semantic Search**: Visualize and debug search results
- **ML Model Development**: Analyze embedding quality
- **Data Science**: Explore vector representations of text or images

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **FAISS** by Facebook Research - High-performance similarity search
- **Chroma** - AI-native embedding database
- **VS Code Extension API** - Powerful extensibility platform
- The open-source AI/ML community

## 📧 Feedback & Support

We'd love to hear from you!

- **Issues & Bug Reports**: [GitHub Issues](https://github.com/yourusername/vector-explorer/issues)
- **Feature Requests**: Share your ideas on GitHub
- **Questions**: Check existing issues or create a new discussion

### Rating & Reviews
If you find this extension helpful, please consider:
- ⭐ Rating it on the VS Code Marketplace
- 📝 Writing a review
- 🔗 Sharing it with colleagues

---

**Made with ❤️ for the AI/ML community**

*Happy Vector Exploring! 🚀*
