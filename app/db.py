import json
from pathlib import Path

from tinydb import TinyDB


ROOT_DIR = Path(__file__).resolve().parents[1]
DB_DIR = ROOT_DIR / "db"
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "leads.json"

# Open DB
db = TinyDB(DB_PATH.as_posix())

# If the file contains a top-level {"leads": [ ... ]} payload (per PRD),
# import those rows into the default table on first run.
try:
    raw_text = DB_PATH.read_text(encoding="utf-8") if DB_PATH.exists() else ""
    if raw_text.strip().startswith("{"):
        data = json.loads(raw_text)
        if isinstance(data, dict) and "leads" in data and isinstance(data["leads"], list):
            table = db.table("_default")  # default table alias
            # Only import if empty to avoid duplicating on restarts
            if len(table) == 0:
                for row in data["leads"]:
                    if isinstance(row, dict):
                        table.insert(row)
except Exception:
    # Best-effort import; continue with an empty DB if parsing fails
    pass


