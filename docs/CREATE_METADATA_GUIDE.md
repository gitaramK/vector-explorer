# create_metadata.py - Complete FAISS Database Generator

## Overview

The `create_metadata.py` utility has been upgraded to create **complete FAISS vector databases** with text chunking and HuggingFace embeddings. This demonstrates a real-world use case of creating vector databases that can be visualized in Vector Explorer.

## Features

- ✅ **Text Chunking**: Multiple strategies (fixed-size, tokens, sentences, code-aware)
- ✅ **HuggingFace Embeddings**: Generate embeddings using sentence-transformers
- ✅ **OpenAI Embeddings**: Optional support for OpenAI embedding models
- ✅ **FAISS Index Creation**: Creates optimized FAISS indexes (flat, IVF, HNSW)
- ✅ **Metadata Generation**: Automatic metadata.json for text visualization
- ✅ **Multi-format Support**: Process text files, code files, JSON, etc.

## Installation

```bash
# Core dependencies (required)
pip install faiss-cpu numpy

# For HuggingFace embeddings (recommended)
pip install sentence-transformers torch

# For OpenAI embeddings (optional)
pip install openai

# Or install all at once
pip install -r python/requirements.txt
```

## Usage Examples

### 1. Quick Example (Recommended First Step)

Create an example database with sample data to test Vector Explorer:

```bash
python python/create_metadata.py --example
```

This creates `./example_faiss_db/` with:
- 10 sample documents about AI/ML
- 384-dimensional embeddings (HuggingFace all-MiniLM-L6-v2)
- Complete metadata for visualization

**Then open in Vector Explorer:**
1. Press F5 in VS Code
2. Run `Vector Explorer: Open Vector Database`
3. Select `./example_faiss_db`

### 2. Create from Directory

Process all compatible files in a directory:

```bash
python python/create_metadata.py \
  --create-faiss ./my_documents \
  --output ./my_vectors
```

Supported file types: `.txt`, `.md`, `.py`, `.js`, `.java`, `.cpp`, `.c`, `.cs`, `.go`

### 3. Create from Specific Files

Process only specified files:

```bash
python python/create_metadata.py \
  --create-faiss file1.txt file2.py README.md \
  --output ./vectors
```

### 4. Custom Chunking Methods

**Fixed-size chunking** (default):
```bash
python python/create_metadata.py \
  --create-faiss ./docs \
  --output ./vectors \
  --chunk-method fixed \
  --chunk-size 1000
```

**Token-based chunking**:
```bash
python python/create_metadata.py \
  --create-faiss ./docs \
  --output ./vectors \
  --chunk-method tokens \
  --chunk-size 512
```

**Sentence-based chunking**:
```bash
python python/create_metadata.py \
  --create-faiss ./docs \
  --output ./vectors \
  --chunk-method sentences \
  --chunk-size 5
```

**Code-aware chunking** (splits by functions/classes):
```bash
python python/create_metadata.py \
  --create-faiss ./src \
  --output ./code_vectors \
  --chunk-method code
```

### 5. Different Embedding Models

**HuggingFace models** (default):
```bash
# Small and fast (384 dimensions)
python python/create_metadata.py \
  --create-faiss ./docs \
  --output ./vectors \
  --model sentence-transformers/all-MiniLM-L6-v2

# Better quality (768 dimensions)
python python/create_metadata.py \
  --create-faiss ./docs \
  --output ./vectors \
  --model sentence-transformers/all-mpnet-base-v2

# Multilingual support
python python/create_metadata.py \
  --create-faiss ./docs \
  --output ./vectors \
  --model sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

**OpenAI embeddings**:
```bash
export OPENAI_API_KEY=your_key_here

python python/create_metadata.py \
  --create-faiss ./docs \
  --output ./vectors \
  --embedding-provider openai \
  --model text-embedding-3-small
```

### 6. Different FAISS Index Types

**Flat index** (exact search, best quality):
```bash
python python/create_metadata.py \
  --create-faiss ./docs \
  --output ./vectors \
  --index-type flat
```

**IVF index** (fast approximate search):
```bash
python python/create_metadata.py \
  --create-faiss ./docs \
  --output ./vectors \
  --index-type ivf
```

**HNSW index** (very fast approximate search):
```bash
python python/create_metadata.py \
  --create-faiss ./docs \
  --output ./vectors \
  --index-type hnsw
```

### 7. Legacy Mode (Metadata Only)

Create metadata.json for an existing FAISS index:

```bash
python python/create_metadata.py \
  --metadata-only ./vectors/index.faiss ./chunks.json
```

## Chunking Methods Explained

### Fixed-Size Chunking
- Splits text into fixed character chunks with overlap
- **Best for**: General documents, consistent chunk sizes
- **Parameters**: `--chunk-size 1000` (characters)

### Token-Based Chunking
- Splits by approximate token count (words)
- **Best for**: Controlling embedding input size
- **Parameters**: `--chunk-size 512` (tokens/words)

### Sentence-Based Chunking
- Groups sentences together
- **Best for**: Maintaining semantic coherence
- **Parameters**: `--chunk-size 5` (sentences per chunk)

### Code-Aware Chunking
- Detects functions and classes in code
- **Best for**: Source code repositories
- **Supported**: Python (.py), JavaScript (.js), Java (.java), C/C++ (.c, .cpp), C# (.cs)

## Complete Workflow Example

Here's a complete example processing a code repository:

```bash
# 1. Create FAISS database from your codebase
python python/create_metadata.py \
  --create-faiss ./my_project/src \
  --output ./my_project_vectors \
  --chunk-method code \
  --chunk-size 500 \
  --embedding-provider huggingface \
  --model sentence-transformers/all-MiniLM-L6-v2 \
  --index-type flat

# 2. Open in Vector Explorer
# - Press F5 in VS Code
# - Run "Vector Explorer: Open Vector Database"
# - Select ./my_project_vectors

# 3. Explore your embeddings!
# - Search for specific code patterns
# - See which code chunks are similar
# - Visualize the complete text → chunks → embeddings pipeline
```

## Output Structure

After running `create_metadata.py`, you'll get:

```
my_vectors/
├── index.faiss        # FAISS vector index
├── metadata.json      # Text chunks with metadata
└── summary.json       # Database statistics
```

**metadata.json format**:
```json
{
  "chunks": [
    {
      "id": "chunk_0000",
      "text": "Your chunked text here...",
      "source": "path/to/source/file.py",
      "metadata": {
        "chunk_index": 0,
        "chunk_type": "function",
        "chunk_name": "process_data"
      }
    }
  ],
  "total": 100,
  "dimension": 384,
  "index_type": "flat",
  "created_at": "2025-11-02T10:30:00"
}
```

## HuggingFace Model Recommendations

| Model | Dimensions | Speed | Quality | Use Case |
|-------|-----------|-------|---------|----------|
| `all-MiniLM-L6-v2` | 384 | ⚡⚡⚡ | ⭐⭐ | Fast, general purpose |
| `all-mpnet-base-v2` | 768 | ⚡⚡ | ⭐⭐⭐ | Best quality, English |
| `paraphrase-multilingual-MiniLM-L12-v2` | 384 | ⚡⚡ | ⭐⭐ | Multilingual support |
| `all-MiniLM-L12-v2` | 384 | ⚡⚡ | ⭐⭐ | Balanced performance |

## Troubleshooting

### "sentence-transformers not installed"
```bash
pip install sentence-transformers torch
```

### "CUDA out of memory" (GPU issues)
```bash
# Force CPU usage
export CUDA_VISIBLE_DEVICES=-1
python python/create_metadata.py --create-faiss ...
```

### "Too many chunks" (performance)
- Increase `--chunk-size` to create fewer, larger chunks
- Use `--index-type ivf` or `hnsw` for faster search
- Process files in batches

### "Encoding errors" when reading files
The utility automatically tries multiple encodings (UTF-8, Latin-1, CP1252). If a file still fails, convert it to UTF-8 first.

## Advanced Features

### Custom File Extensions
```bash
python python/create_metadata.py \
  --create-faiss ./docs \
  --output ./vectors \
  --file-extensions .txt .md .rst .adoc
```

### Processing Large Repositories
```bash
# Process in smaller batches
python python/create_metadata.py \
  --create-faiss ./large_repo/src/module1 \
  --output ./vectors_part1

python python/create_metadata.py \
  --create-faiss ./large_repo/src/module2 \
  --output ./vectors_part2
```

## Integration with Vector Explorer

Once you've created a FAISS database:

1. **Launch Extension**: Press F5 in VS Code
2. **Open Database**: `Ctrl+Shift+P` → `Vector Explorer: Open Vector Database`
3. **Select Folder**: Choose your output directory (e.g., `./my_vectors`)
4. **Explore**:
   - View original text chunks
   - See vector embeddings
   - Search and filter
   - Export to CSV

## Performance Tips

- **Start small**: Test with `--example` first
- **Choose appropriate chunk size**: 
  - Small chunks (256-512): Better for precise search
  - Large chunks (1000-2000): Better context
- **Select right model**:
  - Fast: all-MiniLM-L6-v2
  - Quality: all-mpnet-base-v2
- **Index type**:
  - <10K vectors: Use `flat`
  - 10K-1M vectors: Use `ivf`
  - >1M vectors: Use `hnsw`

## Example Use Cases

### 1. Documentation Search
```bash
python python/create_metadata.py \
  --create-faiss ./documentation \
  --output ./doc_vectors \
  --chunk-method sentences \
  --chunk-size 3
```

### 2. Code Analysis
```bash
python python/create_metadata.py \
  --create-faiss ./codebase \
  --output ./code_vectors \
  --chunk-method code \
  --embedding-provider huggingface
```

### 3. Research Papers
```bash
python python/create_metadata.py \
  --create-faiss ./papers \
  --output ./paper_vectors \
  --chunk-method tokens \
  --chunk-size 512
```

### 4. Customer Support Tickets
```bash
python python/create_metadata.py \
  --create-faiss ./tickets.json \
  --output ./ticket_vectors \
  --chunk-method fixed \
  --chunk-size 500
```

## Complete Command Reference

```bash
python python/create_metadata.py [MODE] [OPTIONS]

Modes:
  --create-faiss FILES...    Create complete FAISS database
  --metadata-only FAISS CHUNKS  Create metadata only (legacy)
  --example                  Create example database

Options:
  --output DIR              Output directory (required for --create-faiss)
  --chunk-method METHOD     Chunking: fixed|tokens|sentences|code
  --chunk-size SIZE         Chunk size parameter
  --embedding-provider PROVIDER  huggingface|openai
  --model MODEL             Model name
  --index-type TYPE         FAISS index: flat|ivf|hnsw
  --api-key KEY             OpenAI API key
  --file-extensions EXT...  File types to process
```

## See Also

- [Vector Explorer README](../README.md)
- [LangChain FAISS Support](./LANGCHAIN_SUPPORT.md)
- [Metadata Guide](./METADATA_GUIDE.md)

---

**Now you can create production-ready FAISS databases with complete text-to-embedding visualization! 🚀**
