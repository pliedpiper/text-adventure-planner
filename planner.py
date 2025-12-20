#!/usr/bin/env python3
"""
Text Adventure Planner
A visual tool for designing branching narrative structures.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from graph_canvas import GraphCanvas
from scene_editor import SceneEditor
from file_io import load_scenes, save_scenes, scenes_to_graph, graph_to_scenes

# Window dimensions
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CANVAS_MIN_WIDTH = 700
EDITOR_WIDTH = 350

# Colors
BG_COLOR = "#2b2b2b"
PANEL_BG = "#3c3c3c"
TEXT_COLOR = "#e0e0e0"
ACCENT_COLOR = "#5c9aff"


class TextAdventurePlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Adventure Planner")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG_COLOR)

        # Current file path (None if unsaved)
        self.current_file = None
        self.unsaved_changes = False

        # Scene data: {scene_id: {id, background, music, text, choices, x, y}}
        self.scenes = {}
        self.selected_scene_id = None

        self._setup_styles()
        self._create_menu()
        self._create_main_layout()
        self._create_status_bar()

        # Bind keyboard shortcuts
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-n>", lambda e: self.new_file())

        # Start with a default scene
        self._create_default_scene()

    def _setup_styles(self):
        """Configure ttk styles for dark theme."""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Dark.TFrame", background=BG_COLOR)
        style.configure("Panel.TFrame", background=PANEL_BG)
        style.configure("Dark.TLabel", background=BG_COLOR, foreground=TEXT_COLOR)
        style.configure("Panel.TLabel", background=PANEL_BG, foreground=TEXT_COLOR)
        style.configure("Dark.TButton", background=PANEL_BG, foreground=TEXT_COLOR)
        style.configure("Accent.TButton", background=ACCENT_COLOR, foreground="white")

    def _create_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root, bg=PANEL_BG, fg=TEXT_COLOR)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=PANEL_BG, fg=TEXT_COLOR)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Export to scenes.json...", command=self.export_scenes)
        file_menu.add_command(label="Import from scenes.json...", command=self.import_scenes)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_app)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0, bg=PANEL_BG, fg=TEXT_COLOR)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Delete Selected Scene", command=self.delete_selected_scene)
        edit_menu.add_command(label="Duplicate Selected Scene", command=self.duplicate_selected_scene)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg=PANEL_BG, fg=TEXT_COLOR)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=lambda: self.graph_canvas.zoom(1.2))
        view_menu.add_command(label="Zoom Out", command=lambda: self.graph_canvas.zoom(0.8))
        view_menu.add_command(label="Reset View", command=lambda: self.graph_canvas.reset_view())
        view_menu.add_separator()
        view_menu.add_command(label="Auto Layout", command=self.auto_layout)

    def _create_main_layout(self):
        """Create the main paned layout with canvas and editor."""
        # Main container
        main_frame = ttk.Frame(self.root, style="Dark.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Horizontal paned window
        self.paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left side: Graph canvas
        canvas_frame = ttk.Frame(self.paned, style="Dark.TFrame")
        self.graph_canvas = GraphCanvas(
            canvas_frame,
            scenes=self.scenes,
            on_select=self.on_scene_selected,
            on_create=self.on_scene_created,
            on_connect=self.on_scenes_connected,
            on_move=self.on_scene_moved,
            on_change=self.mark_unsaved
        )
        self.graph_canvas.pack(fill=tk.BOTH, expand=True)
        self.paned.add(canvas_frame, weight=3)

        # Right side: Scene editor
        editor_frame = ttk.Frame(self.paned, style="Panel.TFrame", width=EDITOR_WIDTH)
        self.scene_editor = SceneEditor(
            editor_frame,
            on_update=self.on_scene_updated,
            on_delete_choice=self.on_choice_deleted,
            on_add_choice=self.on_choice_added
        )
        self.scene_editor.pack(fill=tk.BOTH, expand=True)
        self.paned.add(editor_frame, weight=1)

    def _create_status_bar(self):
        """Create the status bar at bottom."""
        self.status_frame = ttk.Frame(self.root, style="Panel.TFrame")
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_labels = {}
        stats = [
            ("scenes", "Scenes: 0"),
            ("connections", "Connections: 0"),
            ("orphaned", "Orphaned: 0"),
            ("dead_ends", "Dead ends: 0"),
        ]

        for key, text in stats:
            label = ttk.Label(self.status_frame, text=text, style="Panel.TLabel", padding=(10, 5))
            label.pack(side=tk.LEFT)
            self.status_labels[key] = label

        # Validate button on right
        validate_btn = ttk.Button(
            self.status_frame,
            text="Validate",
            command=self.validate_graph,
            style="Dark.TButton"
        )
        validate_btn.pack(side=tk.RIGHT, padx=10, pady=3)

    def _create_default_scene(self):
        """Create a default starting scene."""
        self.scenes["start"] = {
            "id": "start",
            "background": "backgrounds/start.png",
            "music": "music/intro.ogg",
            "text": "Your adventure begins here...",
            "choices": [],
            "x": 400,
            "y": 300
        }
        self.graph_canvas.refresh()
        self.update_status()

    def mark_unsaved(self):
        """Mark that there are unsaved changes."""
        if not self.unsaved_changes:
            self.unsaved_changes = True
            self._update_title()

    def _update_title(self):
        """Update window title with file name and unsaved indicator."""
        title = "Text Adventure Planner"
        if self.current_file:
            title += f" - {self.current_file}"
        if self.unsaved_changes:
            title += " *"
        self.root.title(title)

    def update_status(self):
        """Update the status bar with current stats."""
        num_scenes = len(self.scenes)
        num_connections = sum(len(s.get("choices", [])) for s in self.scenes.values())

        # Find orphaned scenes (not reachable from start)
        reachable = set()
        if "start" in self.scenes:
            to_visit = ["start"]
            while to_visit:
                current = to_visit.pop()
                if current in reachable:
                    continue
                reachable.add(current)
                scene = self.scenes.get(current, {})
                for choice in scene.get("choices", []):
                    next_id = choice.get("next_scene")
                    if next_id and next_id not in reachable:
                        to_visit.append(next_id)
        orphaned = num_scenes - len(reachable)

        # Find dead ends (scenes with no choices)
        dead_ends = sum(1 for s in self.scenes.values() if not s.get("choices"))

        self.status_labels["scenes"].config(text=f"Scenes: {num_scenes}")
        self.status_labels["connections"].config(text=f"Connections: {num_connections}")
        self.status_labels["orphaned"].config(text=f"Orphaned: {orphaned}")
        self.status_labels["dead_ends"].config(text=f"Dead ends: {dead_ends}")

    # === Event handlers from canvas ===

    def on_scene_selected(self, scene_id):
        """Handle scene selection from canvas."""
        self.selected_scene_id = scene_id
        if scene_id and scene_id in self.scenes:
            self.scene_editor.load_scene(self.scenes[scene_id], list(self.scenes.keys()))
        else:
            self.scene_editor.clear()

    def on_scene_created(self, scene_id, x, y):
        """Handle new scene creation from canvas."""
        self.scenes[scene_id] = {
            "id": scene_id,
            "background": f"backgrounds/{scene_id}.png",
            "music": f"music/{scene_id}.wav",
            "text": "Enter scene text...",
            "choices": [],
            "x": x,
            "y": y
        }
        self.graph_canvas.refresh()
        self.on_scene_selected(scene_id)
        self.update_status()
        self.mark_unsaved()

    def on_scenes_connected(self, from_id, to_id):
        """Handle connection created between scenes."""
        if from_id in self.scenes:
            choices = self.scenes[from_id].get("choices", [])
            # Check if connection already exists
            for choice in choices:
                if choice.get("next_scene") == to_id:
                    return
            choices.append({"label": "Continue", "next_scene": to_id})
            self.scenes[from_id]["choices"] = choices
            self.graph_canvas.refresh()
            if self.selected_scene_id == from_id:
                self.scene_editor.load_scene(self.scenes[from_id], list(self.scenes.keys()))
            self.update_status()
            self.mark_unsaved()

    def on_scene_moved(self, scene_id, x, y):
        """Handle scene position change."""
        if scene_id in self.scenes:
            self.scenes[scene_id]["x"] = x
            self.scenes[scene_id]["y"] = y
            self.mark_unsaved()

    # === Event handlers from editor ===

    def on_scene_updated(self, scene_data):
        """Handle scene data update from editor."""
        scene_id = scene_data.get("id")
        old_id = self.selected_scene_id

        if old_id and old_id != scene_id:
            # ID changed, need to rename
            if scene_id in self.scenes:
                messagebox.showerror("Error", f"Scene ID '{scene_id}' already exists!")
                return
            # Update all references to old ID
            for s in self.scenes.values():
                for choice in s.get("choices", []):
                    if choice.get("next_scene") == old_id:
                        choice["next_scene"] = scene_id
            # Move data to new key
            self.scenes[scene_id] = self.scenes.pop(old_id)
            self.selected_scene_id = scene_id

        if scene_id in self.scenes:
            # Preserve position
            x, y = self.scenes[scene_id].get("x", 0), self.scenes[scene_id].get("y", 0)
            self.scenes[scene_id].update(scene_data)
            self.scenes[scene_id]["x"] = x
            self.scenes[scene_id]["y"] = y

        self.graph_canvas.refresh()
        self.update_status()
        self.mark_unsaved()

    def on_choice_deleted(self, scene_id, choice_index):
        """Handle choice deletion from editor."""
        if scene_id in self.scenes:
            choices = self.scenes[scene_id].get("choices", [])
            if 0 <= choice_index < len(choices):
                choices.pop(choice_index)
                self.graph_canvas.refresh()
                self.update_status()
                self.mark_unsaved()

    def on_choice_added(self, scene_id):
        """Handle new choice added from editor."""
        if scene_id in self.scenes:
            choices = self.scenes[scene_id].get("choices", [])
            choices.append({"label": "New choice", "next_scene": ""})
            self.scene_editor.load_scene(self.scenes[scene_id], list(self.scenes.keys()))
            self.graph_canvas.refresh()
            self.mark_unsaved()

    # === Menu actions ===

    def new_file(self):
        """Create a new file."""
        if self.unsaved_changes:
            if not messagebox.askyesno("Unsaved Changes", "Discard unsaved changes?"):
                return
        self.scenes.clear()
        self.current_file = None
        self.unsaved_changes = False
        self._create_default_scene()
        self.on_scene_selected(None)
        self._update_title()

    def open_file(self):
        """Open a planner file."""
        if self.unsaved_changes:
            if not messagebox.askyesno("Unsaved Changes", "Discard unsaved changes?"):
                return
        filepath = filedialog.askopenfilename(
            filetypes=[("Planner files", "*.tapln"), ("All files", "*.*")]
        )
        if filepath:
            try:
                self.scenes = load_scenes(filepath, include_positions=True)
                self.current_file = filepath
                self.unsaved_changes = False
                self.graph_canvas.refresh()
                self.update_status()
                self._update_title()
                self.on_scene_selected(None)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def save_file(self):
        """Save current file."""
        if self.current_file:
            try:
                save_scenes(self.current_file, self.scenes, include_positions=True)
                self.unsaved_changes = False
                self._update_title()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        """Save to a new file."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".tapln",
            filetypes=[("Planner files", "*.tapln"), ("All files", "*.*")]
        )
        if filepath:
            self.current_file = filepath
            self.save_file()

    def export_scenes(self):
        """Export to game's scenes.json format."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile="scenes.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            try:
                save_scenes(filepath, self.scenes, include_positions=False)
                messagebox.showinfo("Export", f"Exported to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")

    def import_scenes(self):
        """Import from game's scenes.json format."""
        if self.unsaved_changes:
            if not messagebox.askyesno("Unsaved Changes", "Discard unsaved changes?"):
                return
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            try:
                self.scenes = load_scenes(filepath, include_positions=False)
                # Auto-layout since positions weren't saved
                self.auto_layout()
                self.current_file = None
                self.unsaved_changes = True
                self.graph_canvas.refresh()
                self.update_status()
                self._update_title()
                self.on_scene_selected(None)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {e}")

    def delete_selected_scene(self):
        """Delete the currently selected scene."""
        if not self.selected_scene_id:
            return
        if self.selected_scene_id == "start":
            messagebox.showwarning("Warning", "Cannot delete the start scene!")
            return
        if messagebox.askyesno("Delete Scene", f"Delete scene '{self.selected_scene_id}'?"):
            # Remove references to this scene
            for s in self.scenes.values():
                s["choices"] = [c for c in s.get("choices", [])
                               if c.get("next_scene") != self.selected_scene_id]
            del self.scenes[self.selected_scene_id]
            self.selected_scene_id = None
            self.scene_editor.clear()
            self.graph_canvas.refresh()
            self.update_status()
            self.mark_unsaved()

    def duplicate_selected_scene(self):
        """Duplicate the currently selected scene."""
        if not self.selected_scene_id:
            return
        scene = self.scenes[self.selected_scene_id]
        new_id = f"{scene['id']}_copy"
        counter = 1
        while new_id in self.scenes:
            new_id = f"{scene['id']}_copy{counter}"
            counter += 1
        new_scene = dict(scene)
        new_scene["id"] = new_id
        new_scene["x"] = scene.get("x", 0) + 50
        new_scene["y"] = scene.get("y", 0) + 50
        new_scene["choices"] = [dict(c) for c in scene.get("choices", [])]
        self.scenes[new_id] = new_scene
        self.graph_canvas.refresh()
        self.update_status()
        self.mark_unsaved()

    def validate_graph(self):
        """Run validation and show results."""
        issues = []

        # Check for orphaned scenes
        reachable = set()
        if "start" in self.scenes:
            to_visit = ["start"]
            while to_visit:
                current = to_visit.pop()
                if current in reachable:
                    continue
                reachable.add(current)
                scene = self.scenes.get(current, {})
                for choice in scene.get("choices", []):
                    next_id = choice.get("next_scene")
                    if next_id and next_id not in reachable:
                        to_visit.append(next_id)
        orphaned = [sid for sid in self.scenes if sid not in reachable]
        if orphaned:
            issues.append(f"Orphaned scenes (unreachable): {', '.join(orphaned)}")

        # Check for dead ends
        dead_ends = [sid for sid, s in self.scenes.items() if not s.get("choices")]
        if dead_ends:
            issues.append(f"Dead ends (no choices): {', '.join(dead_ends)}")

        # Check for broken links
        broken = []
        for sid, scene in self.scenes.items():
            for choice in scene.get("choices", []):
                next_id = choice.get("next_scene")
                if next_id and next_id not in self.scenes:
                    broken.append(f"{sid} → {next_id}")
        if broken:
            issues.append(f"Broken links: {', '.join(broken)}")

        # Check for empty text
        empty_text = [sid for sid, s in self.scenes.items()
                     if not s.get("text") or s.get("text") == "Enter scene text..."]
        if empty_text:
            issues.append(f"Missing text: {', '.join(empty_text)}")

        if issues:
            messagebox.showwarning("Validation Issues", "\n\n".join(issues))
        else:
            messagebox.showinfo("Validation", "No issues found!")

    def auto_layout(self):
        """Auto-arrange nodes in a tree layout."""
        if not self.scenes:
            return

        # Simple layered layout starting from 'start'
        if "start" not in self.scenes:
            # Just arrange in a grid
            x, y = 100, 100
            for scene in self.scenes.values():
                scene["x"] = x
                scene["y"] = y
                x += 200
                if x > 1000:
                    x = 100
                    y += 150
        else:
            # BFS from start to assign layers
            layers = {}
            visited = set()
            queue = [("start", 0)]
            while queue:
                scene_id, layer = queue.pop(0)
                if scene_id in visited or scene_id not in self.scenes:
                    continue
                visited.add(scene_id)
                if layer not in layers:
                    layers[layer] = []
                layers[layer].append(scene_id)
                for choice in self.scenes[scene_id].get("choices", []):
                    next_id = choice.get("next_scene")
                    if next_id and next_id not in visited:
                        queue.append((next_id, layer + 1))

            # Position by layer
            y = 100
            for layer in sorted(layers.keys()):
                scene_ids = layers[layer]
                total_width = len(scene_ids) * 200
                start_x = max(100, (1000 - total_width) // 2)
                for i, scene_id in enumerate(scene_ids):
                    self.scenes[scene_id]["x"] = start_x + i * 200
                    self.scenes[scene_id]["y"] = y
                y += 150

            # Handle orphaned scenes
            for scene_id in self.scenes:
                if scene_id not in visited:
                    self.scenes[scene_id]["x"] = 100
                    self.scenes[scene_id]["y"] = y
                    y += 150

        self.graph_canvas.refresh()
        self.mark_unsaved()

    def quit_app(self):
        """Quit the application."""
        if self.unsaved_changes:
            if not messagebox.askyesno("Unsaved Changes", "Quit without saving?"):
                return
        self.root.quit()


def main():
    root = tk.Tk()
    app = TextAdventurePlanner(root)
    root.protocol("WM_DELETE_WINDOW", app.quit_app)
    root.mainloop()


if __name__ == "__main__":
    main()
