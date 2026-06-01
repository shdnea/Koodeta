# Koodeta — Houdini Setup

Personal Houdini configuration environment.  
Contains custom tools, scripts, presets, and startup configuration for a streamlined VFX workflow.

---

## 📁 Structure

```
.
├── Config/              # Houdini configuration files
├── Desktop/             # Desktop layout presets
├── help/                # Help / docs
├── Otls/                # Houdini digital assets (HDAs)
├── Packages/            # Package .json definitions
├── Presets/             # Tool/operator presets
├── Scripts/
│   └── python/
│       ├── Tools/
│       │   ├── Acnologia/        # Tools panel application (see below)
│       │   └── PaletteExtractor/ # Palette extraction tool
│       ├── Utility/              # Shared utility modules
│       └── ...
├── Startup/             # Houdini startup scripts
├── Toolbar/             # Shelf tool definitions
└── ...
```

---

## 🔧 Acnologia — Tools Panel

A GUI tools launcher built with PySide6 for Houdini.  
Browse, search, and run Python scripts from a categorised grid interface — all editable directly from the app.

### Key Features

| Feature              | Description |
|----------------------|-------------|
| **Grid Layout**      | Tools displayed in a responsive grid that adapts columns when resized |
| **Category Filter**  | Filter tools by category via dropdown (Geometry, Shading, Rigging, FX) |
| **Search**           | Real-time search by tool name, category, or tooltip |
| **Administration**   | Built-in admin panel to add, edit, or delete tools and categories |
| **File-based Library** | Tools stored as individual JSON files in `Library/` — no hardcoding |
| **Re-run**           | Quick re-execute of the last-run tool |
| **Standalone or In-Houdini** | Works both inside Houdini and standalone |

### File Overview

| File                   | Purpose |
|------------------------|---------|
| `main.py`             | Main window, grid layout, search, toolbar, entry point |
| `widget.py`           | `ToolButton` widget — painted cards with hover/flash states |
| `stylesheet.py`       | Colour palette and Qt stylesheet (dark theme, Houdini orange accent) |
| `tools_data.py`       | Loads tools & categories from the `Library/` folder |
| `library_manager.py`  | CRUD engine for the JSON-based tool library |
| `admin_panel.py`      | Administration dialog — add/edit/delete tools & categories |
| `Library/categories.json` | Category definitions |
| `Library/tool_*.json` | Individual tool definitions (one file per tool) |

### Usage

**In Houdini:**
```python
import Scripts.python.Tools.Acnologia.main as acnologia
acnologia.launch()
```

**Standalone:**
```bash
cd Scripts/python/Tools/Acnologia
python main.py
```

### Editing Tools

Click the **⚙** button in the toolbar to open the Administration Panel.  
From there you can:

- **Add** a new tool (auto-assigns next ID)
- **Edit** any tool's label, icon, category, tooltip, or Python script
- **Delete** a tool permanently
- **Manage categories** — add new groups or remove unused ones

All changes are saved immediately to the `Library/` folder as JSON files.

---

## 🚀 Getting Started

1. Clone or symlink this repo into your Houdini user directory:
   ```
   ~/Documents/houdini20.5/
   ```
2. Launch Houdini — the configuration in `Packages/` and `Startup/` will load automatically.
3. Run the Acnologia panel as described above.

---

## 📦 Requirements

- **Houdini** 20.x (or later)
- **PySide6** (ships with Houdini)
- No additional pip packages required

---

## 📝 Notes

- `.gitignore` excludes `__pycache__`, `.pyc` files, and Houdini backup OTLS.
- All tool scripts run in a shared `exec` namespace — builtins are preserved across executions.
- The admin panel changes are live: no restart needed.
