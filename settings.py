import os
from pathlib import Path

PORT = int (os.getenv("PORT", 8000))
print(PORT)

CACHE_AGE = 60 * 60 * 24

PROJECT_DIR = Path(__file__).parent.resolve()

STATIC_DIR = PROJECT_DIR / "static"
assert STATIC_DIR.is_dir(), f"missing directory: STATIC_DIR=`{STATIC_DIR}`"

STORAGE_DIR = PROJECT_DIR / "storage"
assert STORAGE_DIR.is_dir(), f"missing directory: STORAGE_DIR=`{STORAGE_DIR}`"

SITE = os.getenv("SITE", "localhost")
assert SITE, f"cookies won't be working with empty SITE"