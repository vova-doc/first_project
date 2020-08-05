import os
from pathlib import Path

PORT = int (os.getenv("PORT", 8000))
print(PORT)

CACHE_AGE = 60 * 60 * 24

PROJECT_DIR = PATH(__file__).parent.resolv()


