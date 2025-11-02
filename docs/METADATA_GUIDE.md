# Metadata Guide for Vector Explorer

## Why Metadata Matters

When you create embeddings for your text, the **text chunks are not stored in the FAISS index** - only the numerical vectors are saved. To see your original text chunks in Vector Explorer, you need a separate metadata file that maps vectors back to their source text.

**Without metadata**: You'll see vectors (numbers) but no text chunks  
**With metadata**: You'll see the complete picture - text → chunks → embeddings

## Quick Start

### Step 1: Check if Metadata Exists

Navigate to your FAISS directory and look for these files:
```
your_vectors/
├── index.faiss         ← Your FAISS index
└── metadata.json       ← Your metadata (may be missing)
```

The extension searches for metadata in this order:
1. `index.json` (same name as .faiss file)
2. `index_metadata.json`
3. `metadata.json` (in same directory)
4. `chunks.json`
5. `documents.json`

### Step 2: Create Metadata if Missing

Use the included utility script:

```bash
# Navigate to your extension directory
cd vscodeextension-readvecordb

# If you have a text file with one chunk per line
python python/create_metadata.py "path/to/index.faiss" "path/to/chunks.txt"

# If you have a JSON file with chunks
python python/create_metadata.py "path/to/index.faiss" "path/to/chunks.json"
```

## Metadata File Formats

### Format 1: Chunks Array (Recommended)

This is the most flexible format with full support for metadata:

```json
{
  "chunks": [
    {
      "id": "chunk_0000",
      "text": "Your original text chunk here. This is the text that was embedded.",
      "source": "path/to/source/document.txt",
      "metadata": {
        "line_number": 42,
        "category": "code",
        "language": "python"
      }
    },
    {
      "id": "chunk_0001",
      "text": "Another text chunk...",
      "source": "path/to/another/file.txt",
      "metadata": {
        "line_number": 100,
        "category": "documentation"
      }
    }
  ],
  "total": 2,
  "embedding_model": "text-embedding-ada-002",
  "dimension": 1536
}
```

**Required fields**:
- `chunks`: Array of chunk objects
- `chunks[].text`: The original text that was embedded

**Optional fields**:
- `chunks[].id`: Unique identifier (defaults to chunk_XXXX)
- `chunks[].source`: Source file or document name
- `chunks[].metadata`: Any additional custom metadata
- `total`: Total number of chunks
- `embedding_model`: Model used for embeddings
- `dimension`: Vector dimensionality

### Format 2: Simple Arrays

For basic use cases without complex metadata:

```json
{
  "texts": [
    "First text chunk",
    "Second text chunk",
    "Third text chunk"
  ],
  "sources": [
    "file1.txt",
    "file2.txt",
    "file3.txt"
  ],
  "ids": [
    "custom_id_1",
    "custom_id_2",
    "custom_id_3"
  ]
}
```

**Note**: All arrays must be the same length and aligned by index.

### Format 3: Documents Array

Simplified format for document storage:

```json
{
  "documents": [
    "Complete first document text...",
    "Complete second document text...",
    "Complete third document text..."
  ]
}
```

### Format 4: Flat Array

Simplest format - just an array of text strings:

```json
[
  "First text chunk",
  "Second text chunk",
  "Third text chunk"
]
```

## Creating Metadata: Step-by-Step

### Scenario 1: You Have Original Text Files

If you have the original text files that were chunked and embedded:

```python
import json
import os

def create_metadata_from_files(text_dir, output_path):
    """Create metadata from directory of text files."""
    chunks = []
    chunk_id = 0
    
    for filename in os.listdir(text_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(text_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Split into chunks (adjust chunk_size as needed)
            chunk_size = 1000
            for i in range(0, len(content), chunk_size):
                chunk_text = content[i:i+chunk_size]
                chunks.append({
                    'id': f'chunk_{chunk_id:04d}',
                    'text': chunk_text,
                    'source': filename,
                    'metadata': {
                        'start_pos': i,
                        'end_pos': i + len(chunk_text)
                    }
                })
                chunk_id += 1
    
    # Save metadata
    metadata = {
        'chunks': chunks,
        'total': len(chunks)
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"Created metadata for {len(chunks)} chunks")

# Usage
create_metadata_from_files('./source_texts', './vectors/metadata.json')
```

### Scenario 2: You Have a CSV/TSV File

If your chunks are in a spreadsheet or CSV:

```python
import csv
import json

def create_metadata_from_csv(csv_path, output_path):
    """Create metadata from CSV file."""
    chunks = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            chunks.append({
                'id': row.get('id', f'chunk_{i:04d}'),
                'text': row['text'],  # Assumes 'text' column exists
                'source': row.get('source', 'unknown'),
                'metadata': {k: v for k, v in row.items() 
                           if k not in ['id', 'text', 'source']}
            })
    
    metadata = {
        'chunks': chunks,
        'total': len(chunks)
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"Created metadata for {len(chunks)} chunks")

# Usage
create_metadata_from_csv('./chunks.csv', './vectors/metadata.json')
```

### Scenario 3: You Have a Database

If your chunks are stored in a database:

```python
import sqlite3
import json

def create_metadata_from_db(db_path, output_path):
    """Create metadata from SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Adjust query to match your schema
    cursor.execute("""
        SELECT id, text, source, line_number 
        FROM chunks 
        ORDER BY id
    """)
    
    chunks = []
    for row in cursor.fetchall():
        chunks.append({
            'id': row[0],
            'text': row[1],
            'source': row[2],
            'metadata': {
                'line_number': row[3]
            }
        })
    
    conn.close()
    
    metadata = {
        'chunks': chunks,
        'total': len(chunks)
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"Created metadata for {len(chunks)} chunks")

# Usage
create_metadata_from_db('./chunks.db', './vectors/metadata.json')
```

## Common Issues

### Issue 1: "Text chunks showing (0 chars)"

**Cause**: No metadata file found  
**Solution**: Create a metadata.json file in the same directory as your index.faiss

### Issue 2: "Metadata file found but text still empty"

**Cause**: Mismatch between vector count and metadata count  
**Solution**: Ensure your metadata has the same number of entries as vectors in the index

```python
import faiss
import json

# Check vector count
index = faiss.read_index('index.faiss')
print(f"Vectors in index: {index.ntotal}")

# Check metadata count
with open('metadata.json', 'r') as f:
    metadata = json.load(f)
    chunk_count = len(metadata.get('chunks', []))
    print(f"Chunks in metadata: {chunk_count}")

# They should match!
```

### Issue 3: "Wrong text showing for vectors"

**Cause**: Metadata order doesn't match vector order in index  
**Solution**: Ensure chunks in metadata.json are in the same order as when you added vectors to FAISS

### Issue 4: "Special characters not displaying correctly"

**Cause**: Encoding issues  
**Solution**: Always use UTF-8 encoding:

```python
with open('metadata.json', 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)
```

## Best Practices

1. **Keep metadata in sync**: When you update your FAISS index, update metadata too
2. **Use meaningful IDs**: Use descriptive IDs like `doc_123_chunk_5` instead of just numbers
3. **Include source information**: Always track where chunks came from
4. **Add custom metadata**: Include useful info like timestamps, categories, etc.
5. **Version your metadata**: Add version field to track changes
6. **Validate before saving**: Check chunk count matches vector count
7. **Use compression for large files**: For very large metadata files, consider gzip compression

## Example: Complete Workflow

Here's a complete example showing text → chunks → embeddings → visualization:

```python
import faiss
import numpy as np
import json
from typing import List

# Step 1: Prepare your text
documents = [
    "Python is a high-level programming language.",
    "It supports multiple programming paradigms.",
    "Python has a comprehensive standard library."
]

# Step 2: Create embeddings (example with random vectors)
# In production, use OpenAI, Sentence Transformers, etc.
dimension = 1536
embeddings = np.random.random((len(documents), dimension)).astype('float32')

# Step 3: Create FAISS index
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
faiss.write_index(index, 'my_vectors.faiss')

# Step 4: Create metadata
metadata = {
    'chunks': [
        {
            'id': f'doc_{i:04d}',
            'text': text,
            'source': 'example_docs.txt',
            'metadata': {
                'length': len(text),
                'word_count': len(text.split())
            }
        }
        for i, text in enumerate(documents)
    ],
    'total': len(documents),
    'embedding_model': 'example-model',
    'dimension': dimension,
    'created_at': '2024-01-01T00:00:00Z'
}

with open('my_vectors.json', 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print("✓ Created FAISS index with metadata")
print(f"✓ {len(documents)} documents embedded")
print(f"✓ Vector dimension: {dimension}")
print("\nNow open 'my_vectors.faiss' in Vector Explorer!")
```

## Debugging Metadata Loading

The Python adapter prints diagnostic messages to help debug:

```bash
# Run the adapter directly to see what's happening
python python/faiss_adapter.py "path/to/index.faiss"
```

Look for these messages:
- `Found metadata file: <path>` - Metadata file was found
- `Warning: No metadata file found. Searched for:` - Lists all paths that were checked
- `Successfully loaded metadata from: <path>` - Metadata loaded successfully
- `No metadata available - text chunks will be empty` - No metadata file exists

## Additional Resources

- [FAISS Documentation](https://github.com/facebookresearch/faiss/wiki)
- [JSON Format Specification](https://www.json.org/)
- [UTF-8 Encoding Guide](https://docs.python.org/3/howto/unicode.html)

---

**Need help?** Open an issue on GitHub with:
1. Your FAISS index path
2. Output from running the Python adapter directly
3. Contents of your metadata.json (first few entries)
