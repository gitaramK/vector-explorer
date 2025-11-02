import sys
import json

# Read JSON from stdin (piped from faiss_adapter.py)
data = json.loads(sys.stdin.read())

# Check first vector
first = data['vectors'][0]
print('First vector:')
print(f'  ID: {first["id"]}')
print(f'  Text length: {len(first["text"])} characters')
print(f'  Text preview: {first["text"][:200]}...')
print(f'  Source: {first["source"]}')
print(f'  Metadata: {first["metadata"]}')
print()

# Check how many vectors have text
with_text = sum(1 for v in data['vectors'] if len(v['text']) > 0)
print(f'Vectors with text: {with_text} / {len(data["vectors"])}')
