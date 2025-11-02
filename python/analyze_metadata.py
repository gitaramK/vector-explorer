import json
import sys

if len(sys.argv) < 2:
    print("Usage: python analyze_metadata.py <path_to_metadata.json>")
    sys.exit(1)

metadata_path = sys.argv[1]

with open(metadata_path, 'r', encoding='utf-8') as f:
    metadata = json.load(f)

print("=" * 60)
print("METADATA STRUCTURE ANALYSIS")
print("=" * 60)

print(f"\nTop-level keys: {list(metadata.keys())}")

for key, value in metadata.items():
    value_type = type(value).__name__
    if isinstance(value, list):
        print(f"\n{key}: list with {len(value)} items")
        if len(value) > 0:
            print(f"  First item type: {type(value[0]).__name__}")
            if isinstance(value[0], dict):
                print(f"  First item keys: {list(value[0].keys())}")
            elif isinstance(value[0], str):
                print(f"  First item preview: {value[0][:100]}...")
    elif isinstance(value, dict):
        print(f"\n{key}: dict with {len(value)} keys")
        print(f"  Keys: {list(value.keys())[:10]}...")
    else:
        print(f"\n{key}: {value_type} = {value}")

print("\n" + "=" * 60)
print("CHECKING FOR CHUNK DATA")
print("=" * 60)

# Check common chunk locations
possible_keys = ['chunks', 'documents', 'texts', 'data', 'embeddings', 'items']
for key in possible_keys:
    if key in metadata:
        value = metadata[key]
        print(f"\n✓ Found '{key}' key")
        if isinstance(value, list):
            print(f"  Type: list with {len(value)} items")
            if len(value) > 0 and isinstance(value[0], dict):
                print(f"  Sample keys: {list(value[0].keys())}")
                if 'text' in value[0]:
                    print(f"  ✓ Has 'text' field: {value[0]['text'][:50]}...")
        elif isinstance(value, dict):
            print(f"  Type: dict with {len(value)} keys")

print("\n" + "=" * 60)
