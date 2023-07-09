from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MIGRATION_PATH = BASE_DIR.parent / "canarypy" / "alembic.ini"
