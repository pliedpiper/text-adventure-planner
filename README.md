# Text Adventure Planner

A visual tool for designing branching narrative structures for text adventure games. Create, connect, and organize scenes using an intuitive node-based graph interface.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)

## Features

- **Visual Scene Graph** - Drag-and-drop node editor with zoom and pan controls
- **Scene Editor Panel** - Edit scene properties including background, music, text, and choices
- **Connection Management** - Right-click to create connections between scenes
- **Auto Layout** - Automatically arrange nodes in a hierarchical tree layout
- **Validation** - Detect orphaned scenes, dead ends, and broken links
- **Import/Export** - Save in planner format (`.tapln`) or export to game-ready `scenes.json`

## Installation

Requires Python 3.x with Tkinter (included with most Python installations).

```bash
# Clone or download the repository
cd text-adventure-planner

# Run the application
python planner.py
```

## Usage

### Creating Scenes

- **Double-click** on the canvas to create a new scene
- Enter a unique scene ID when prompted
- The first scene should have ID `start` (created by default)

### Editing Scenes

Select a scene to edit its properties in the right panel:

- **Scene ID** - Unique identifier for the scene
- **Background** - Path to background image (e.g., `backgrounds/forest.png`)
- **Music** - Path to music file (e.g., `music/ambient.ogg`)
- **Scene Text** - The narrative text displayed to the player
- **Choices** - Player options that link to other scenes

### Connecting Scenes

- **Right-click** on a scene and drag to another scene to create a connection
- Connections appear as arrows showing the flow of choices
- Edit choice labels in the scene editor panel

### Navigation

| Action | Control |
|--------|---------|
| Pan | Middle-click drag or Shift+click drag |
| Zoom | Scroll wheel |
| Select | Left-click on node |
| Create node | Double-click on canvas |
| Connect nodes | Right-click drag from source to target |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New file |
| Ctrl+O | Open file |
| Ctrl+S | Save file |

## File Formats

### Planner Format (`.tapln`)

Includes node positions for the visual editor:

```json
{
  "start": {
    "id": "start",
    "background": "backgrounds/start.png",
    "music": "music/intro.ogg",
    "text": "Your adventure begins here...",
    "choices": [
      {"label": "Go north", "next_scene": "forest"},
      {"label": "Go south", "next_scene": "village"}
    ],
    "x": 400,
    "y": 300
  }
}
```

### Game Format (`scenes.json`)

Export format for use in your game engine:

```json
[
  {
    "id": "start",
    "background": "backgrounds/start.png",
    "music": "music/intro.ogg",
    "text": "Your adventure begins here...",
    "choices": [
      {"label": "Go north", "next_scene": "forest"},
      {"label": "Go south", "next_scene": "village"}
    ]
  }
]
```

## Validation

Click the **Validate** button to check for common issues:

- **Orphaned scenes** - Scenes not reachable from `start`
- **Dead ends** - Scenes with no choices (may be intentional endings)
- **Broken links** - Choices pointing to non-existent scenes
- **Missing text** - Scenes with placeholder or empty text

## Project Structure

```
text-adventure-planner/
├── planner.py        # Main application and UI
├── graph_canvas.py   # Visual node/edge rendering
├── scene_editor.py   # Side panel for editing scenes
└── file_io.py        # JSON load/save utilities
```

## License

MIT License
