"""
library_manager.py
CRUD engine for the Library folder — tools & categories stored as JSON files.
"""

import os
import json
import re

_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
_LIBRARY_DIR = os.path.join(_MODULE_DIR, "Library")
_CATEGORIES_FILE = os.path.join(_LIBRARY_DIR, "categories.json")

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def _next_id() -> int:
    """Return max existing tool id + 1."""
    ids = [t["id"] for t in load_tools()]
    return max(ids) + 1 if ids else 1


def _tool_filename(tool_id: int) -> str:
    return os.path.join(_LIBRARY_DIR, f"tool_{tool_id:03d}.json")


# ─────────────────────────────────────────────
#  CATEGORIES
# ─────────────────────────────────────────────
def load_categories() -> dict:
    """Return { category_name: [tool_labels] } from Library/categories.json."""
    if os.path.exists(_CATEGORIES_FILE):
        try:
            with open(_CATEGORIES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"All Tools": None}


def save_categories(categories: dict) -> None:
    """Write categories dict to Library/categories.json.
    Values are stored as empty lists (tools carry their own category field).
    """
    os.makedirs(_LIBRARY_DIR, exist_ok=True)
    # Normalise: store as empty list for non-null entries
    cleaned = {}
    for k, v in categories.items():
        if k == "All Tools":
            cleaned[k] = None
        else:
            cleaned[k] = []
    with open(_CATEGORIES_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────
#  TOOLS  (CRUD)
# ─────────────────────────────────────────────
def load_tools() -> list[dict]:
    """Load all tool JSON files from Library/ as a list of dicts."""
    tools = []
    if not os.path.isdir(_LIBRARY_DIR):
        return tools
    pattern = re.compile(r"tool_\d{3}\.json$")
    for fname in sorted(os.listdir(_LIBRARY_DIR)):
        if pattern.match(fname):
            fpath = os.path.join(_LIBRARY_DIR, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    tools.append(json.load(f))
            except (json.JSONDecodeError, OSError):
                continue
    return tools


def save_tool(tool: dict) -> None:
    """Create or update a single tool JSON file by its id."""
    os.makedirs(_LIBRARY_DIR, exist_ok=True)
    fpath = _tool_filename(tool["id"])
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(tool, f, indent=2, ensure_ascii=False)


def add_tool(tool: dict) -> dict:
    """Insert a new tool (auto-assigns id if missing). Returns the tool with id set."""
    if "id" not in tool or not tool["id"]:
        tool["id"] = _next_id()
    save_tool(tool)
    return tool


def update_tool(tool_id: int, updates: dict) -> bool:
    """Update fields of an existing tool. Returns True if succeeded."""
    tools = load_tools()
    for t in tools:
        if t["id"] == tool_id:
            t.update(updates)
            save_tool(t)
            return True
    return False


def delete_tool(tool_id: int) -> bool:
    """Remove a tool JSON file by id. Returns True if removed."""
    fpath = _tool_filename(tool_id)
    if os.path.exists(fpath):
        os.remove(fpath)
        return True
    return False


# ─────────────────────────────────────────────
#  REBUILD tools_data.py   (optional sync)
# ─────────────────────────────────────────────
def _tools_as_tuples() -> list[tuple]:
    """Return tools list in the (id, label, category, icon, tooltip, script) format."""
    result = []
    for t in load_tools():
        result.append((
            t.get("id", 0),
            t.get("label", ""),
            t.get("category", ""),
            t.get("icon", "●"),
            t.get("tooltip", ""),
            t.get("script", ""),
        ))
    return result

