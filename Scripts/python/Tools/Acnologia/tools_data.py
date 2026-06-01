"""
tools_data.py
Houdini Tools Panel — tool & category data loaded from Library/ folder.
Edit tools via the Administration Panel (Admin button in toolbar).
"""

from .library_manager import load_tools, load_categories, _tools_as_tuples

# ─────────────────────────────────────────────
#  CATEGORIES   (loaded from Library/categories.json)
# ─────────────────────────────────────────────
CATEGORIES = load_categories()
# ─────────────────────────────────────────────
#  TOOLS   (loaded from Library/tool_*.json)
#  Each tool: (id, label, category, icon_char, tooltip, script)
# ─────────────────────────────────────────────
TOOLS = _tools_as_tuples()

