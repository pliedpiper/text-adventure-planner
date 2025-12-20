"""
Graph Canvas - Visual node/edge rendering and interaction for scene graph.
"""

import tkinter as tk
from tkinter import simpledialog
import math

# Node dimensions
NODE_WIDTH = 140
NODE_HEIGHT = 60
NODE_RADIUS = 8

# Colors
CANVAS_BG = "#1e1e1e"
NODE_FILL = "#3c5a7a"
NODE_FILL_SELECTED = "#5c8abf"
NODE_FILL_START = "#4a7a4a"
NODE_FILL_DEAD_END = "#7a4a4a"
NODE_OUTLINE = "#6a8aa8"
NODE_OUTLINE_SELECTED = "#8ab8e8"
NODE_TEXT = "#e0e0e0"
EDGE_COLOR = "#6a8aa8"
EDGE_ARROW_COLOR = "#8ab8e8"
GRID_COLOR = "#2a2a2a"
CONNECTION_PREVIEW_COLOR = "#ffaa00"


class GraphCanvas(tk.Canvas):
    def __init__(self, parent, scenes, on_select, on_create, on_connect, on_move, on_change):
        super().__init__(parent, bg=CANVAS_BG, highlightthickness=0)

        self.scenes = scenes
        self.on_select = on_select
        self.on_create = on_create
        self.on_connect = on_connect
        self.on_move = on_move
        self.on_change = on_change

        # View transform
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0

        # Interaction state
        self.selected_id = None
        self.dragging = False
        self.drag_start = None
        self.drag_node_start = None
        self.panning = False
        self.pan_start = None

        # Connection creation state
        self.connecting = False
        self.connect_from_id = None
        self.connect_preview_end = None

        # Bind events
        self.bind("<Button-1>", self.on_click)
        self.bind("<Double-Button-1>", self.on_double_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Button-2>", self.on_middle_click)  # Middle mouse
        self.bind("<B2-Motion>", self.on_pan)
        self.bind("<ButtonRelease-2>", self.on_pan_release)
        self.bind("<Button-3>", self.on_right_click)  # Right click
        self.bind("<MouseWheel>", self.on_scroll)  # Windows/Mac
        self.bind("<Button-4>", lambda e: self.zoom(1.1))  # Linux scroll up
        self.bind("<Button-5>", lambda e: self.zoom(0.9))  # Linux scroll down
        self.bind("<Shift-Button-1>", self.on_shift_click)
        self.bind("<Shift-B1-Motion>", self.on_pan)
        self.bind("<Shift-ButtonRelease-1>", self.on_pan_release)

        # Keyboard
        self.bind("<Delete>", self.on_delete_key)
        self.bind("<BackSpace>", self.on_delete_key)
        self.focus_set()

    def refresh(self):
        """Redraw the entire canvas."""
        self.delete("all")
        self._draw_grid()
        self._draw_edges()
        self._draw_nodes()

    def _draw_grid(self):
        """Draw background grid."""
        # Calculate visible area
        width = self.winfo_width() or 800
        height = self.winfo_height() or 600

        grid_size = 50 * self.scale
        if grid_size < 20:
            grid_size = 100 * self.scale
        if grid_size < 20:
            return  # Too zoomed out for grid

        # Draw vertical lines
        start_x = (self.offset_x % grid_size) - grid_size
        x = start_x
        while x < width:
            self.create_line(x, 0, x, height, fill=GRID_COLOR, tags="grid")
            x += grid_size

        # Draw horizontal lines
        start_y = (self.offset_y % grid_size) - grid_size
        y = start_y
        while y < height:
            self.create_line(0, y, width, y, fill=GRID_COLOR, tags="grid")
            y += grid_size

    def _draw_edges(self):
        """Draw connection edges between nodes."""
        for scene_id, scene in self.scenes.items():
            start_x, start_y = self._world_to_screen(
                scene.get("x", 0) + NODE_WIDTH // 2,
                scene.get("y", 0) + NODE_HEIGHT // 2
            )

            for choice in scene.get("choices", []):
                target_id = choice.get("next_scene")
                if target_id and target_id in self.scenes:
                    target = self.scenes[target_id]
                    end_x, end_y = self._world_to_screen(
                        target.get("x", 0) + NODE_WIDTH // 2,
                        target.get("y", 0) + NODE_HEIGHT // 2
                    )

                    # Draw edge with arrow
                    self._draw_arrow(start_x, start_y, end_x, end_y, EDGE_COLOR)

        # Draw connection preview if connecting
        if self.connecting and self.connect_from_id and self.connect_preview_end:
            scene = self.scenes.get(self.connect_from_id)
            if scene:
                start_x, start_y = self._world_to_screen(
                    scene.get("x", 0) + NODE_WIDTH // 2,
                    scene.get("y", 0) + NODE_HEIGHT // 2
                )
                self._draw_arrow(
                    start_x, start_y,
                    self.connect_preview_end[0], self.connect_preview_end[1],
                    CONNECTION_PREVIEW_COLOR
                )

    def _draw_arrow(self, x1, y1, x2, y2, color):
        """Draw a line with an arrow at the end."""
        # Calculate direction
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        if length < 1:
            return

        # Normalize
        dx /= length
        dy /= length

        # Shorten line to not overlap nodes
        node_radius = (NODE_WIDTH // 2) * self.scale
        x1 += dx * node_radius
        y1 += dy * node_radius
        x2 -= dx * node_radius
        y2 -= dy * node_radius

        # Draw line
        self.create_line(x1, y1, x2, y2, fill=color, width=2, tags="edge")

        # Draw arrowhead
        arrow_size = 10 * self.scale
        angle = math.atan2(dy, dx)
        ax1 = x2 - arrow_size * math.cos(angle - 0.4)
        ay1 = y2 - arrow_size * math.sin(angle - 0.4)
        ax2 = x2 - arrow_size * math.cos(angle + 0.4)
        ay2 = y2 - arrow_size * math.sin(angle + 0.4)
        self.create_polygon(x2, y2, ax1, ay1, ax2, ay2, fill=color, tags="edge")

    def _draw_nodes(self):
        """Draw all scene nodes."""
        for scene_id, scene in self.scenes.items():
            self._draw_node(scene_id, scene)

    def _draw_node(self, scene_id, scene):
        """Draw a single node."""
        x, y = self._world_to_screen(scene.get("x", 0), scene.get("y", 0))
        w = NODE_WIDTH * self.scale
        h = NODE_HEIGHT * self.scale
        r = NODE_RADIUS * self.scale

        # Determine fill color
        if scene_id == self.selected_id:
            fill = NODE_FILL_SELECTED
            outline = NODE_OUTLINE_SELECTED
        elif scene_id == "start":
            fill = NODE_FILL_START
            outline = NODE_OUTLINE
        elif not scene.get("choices"):
            fill = NODE_FILL_DEAD_END
            outline = NODE_OUTLINE
        else:
            fill = NODE_FILL
            outline = NODE_OUTLINE

        # Draw rounded rectangle
        self._draw_rounded_rect(x, y, w, h, r, fill, outline, f"node_{scene_id}")

        # Draw text (scene id)
        text_size = max(8, int(12 * self.scale))
        self.create_text(
            x + w/2, y + h/2,
            text=scene_id,
            fill=NODE_TEXT,
            font=("Helvetica", text_size, "bold"),
            tags=f"node_{scene_id}"
        )

        # Draw choice count indicator
        num_choices = len(scene.get("choices", []))
        if num_choices > 0:
            indicator_size = max(12, int(16 * self.scale))
            self.create_oval(
                x + w - indicator_size, y - indicator_size/2,
                x + w, y + indicator_size/2,
                fill="#5c9aff", outline="",
                tags=f"node_{scene_id}"
            )
            self.create_text(
                x + w - indicator_size/2, y,
                text=str(num_choices),
                fill="white",
                font=("Helvetica", max(6, int(8 * self.scale)), "bold"),
                tags=f"node_{scene_id}"
            )

    def _draw_rounded_rect(self, x, y, w, h, r, fill, outline, tags):
        """Draw a rounded rectangle."""
        # Create rounded rectangle using polygon
        points = [
            x + r, y,
            x + w - r, y,
            x + w, y + r,
            x + w, y + h - r,
            x + w - r, y + h,
            x + r, y + h,
            x, y + h - r,
            x, y + r,
        ]
        self.create_polygon(points, fill=fill, outline=outline, width=2, smooth=True, tags=tags)

    def _world_to_screen(self, wx, wy):
        """Convert world coordinates to screen coordinates."""
        sx = wx * self.scale + self.offset_x
        sy = wy * self.scale + self.offset_y
        return sx, sy

    def _screen_to_world(self, sx, sy):
        """Convert screen coordinates to world coordinates."""
        wx = (sx - self.offset_x) / self.scale
        wy = (sy - self.offset_y) / self.scale
        return wx, wy

    def _get_node_at(self, sx, sy):
        """Get scene_id of node at screen position, or None."""
        wx, wy = self._screen_to_world(sx, sy)
        for scene_id, scene in self.scenes.items():
            nx = scene.get("x", 0)
            ny = scene.get("y", 0)
            if nx <= wx <= nx + NODE_WIDTH and ny <= wy <= ny + NODE_HEIGHT:
                return scene_id
        return None

    # === Event handlers ===

    def on_click(self, event):
        """Handle left click - select node or start drag."""
        self.focus_set()
        node_id = self._get_node_at(event.x, event.y)

        if self.connecting:
            # Complete connection
            if node_id and node_id != self.connect_from_id:
                self.on_connect(self.connect_from_id, node_id)
            self.connecting = False
            self.connect_from_id = None
            self.connect_preview_end = None
            self.refresh()
            return

        if node_id:
            self.selected_id = node_id
            self.on_select(node_id)
            self.dragging = True
            self.drag_start = (event.x, event.y)
            scene = self.scenes[node_id]
            self.drag_node_start = (scene.get("x", 0), scene.get("y", 0))
        else:
            self.selected_id = None
            self.on_select(None)

        self.refresh()

    def on_double_click(self, event):
        """Handle double click - create new node."""
        node_id = self._get_node_at(event.x, event.y)
        if node_id:
            return  # Double-clicked existing node

        # Prompt for new scene ID
        new_id = simpledialog.askstring("New Scene", "Enter scene ID:", parent=self)
        if new_id:
            new_id = new_id.strip().lower().replace(" ", "_")
            if new_id in self.scenes:
                return  # Already exists
            wx, wy = self._screen_to_world(event.x, event.y)
            # Center the node on click position
            wx -= NODE_WIDTH // 2
            wy -= NODE_HEIGHT // 2
            self.on_create(new_id, wx, wy)
            self.selected_id = new_id

    def on_drag(self, event):
        """Handle mouse drag - move node or pan."""
        if self.connecting:
            self.connect_preview_end = (event.x, event.y)
            self.refresh()
            return

        if self.dragging and self.selected_id and self.drag_start:
            dx = (event.x - self.drag_start[0]) / self.scale
            dy = (event.y - self.drag_start[1]) / self.scale
            new_x = self.drag_node_start[0] + dx
            new_y = self.drag_node_start[1] + dy
            self.scenes[self.selected_id]["x"] = new_x
            self.scenes[self.selected_id]["y"] = new_y
            self.refresh()

    def on_release(self, event):
        """Handle mouse release."""
        if self.dragging and self.selected_id:
            scene = self.scenes[self.selected_id]
            self.on_move(self.selected_id, scene.get("x", 0), scene.get("y", 0))
        self.dragging = False
        self.drag_start = None
        self.drag_node_start = None

    def on_shift_click(self, event):
        """Handle shift+click - start panning."""
        self.panning = True
        self.pan_start = (event.x, event.y)

    def on_middle_click(self, event):
        """Handle middle mouse - start panning."""
        self.panning = True
        self.pan_start = (event.x, event.y)

    def on_pan(self, event):
        """Handle pan drag."""
        if self.panning and self.pan_start:
            dx = event.x - self.pan_start[0]
            dy = event.y - self.pan_start[1]
            self.offset_x += dx
            self.offset_y += dy
            self.pan_start = (event.x, event.y)
            self.refresh()

    def on_pan_release(self, event):
        """Handle pan release."""
        self.panning = False
        self.pan_start = None

    def on_right_click(self, event):
        """Handle right click - start connection from node."""
        node_id = self._get_node_at(event.x, event.y)
        if node_id:
            self.connecting = True
            self.connect_from_id = node_id
            self.connect_preview_end = (event.x, event.y)

    def on_scroll(self, event):
        """Handle scroll wheel - zoom."""
        if event.delta > 0:
            self.zoom(1.1, event.x, event.y)
        else:
            self.zoom(0.9, event.x, event.y)

    def on_delete_key(self, event):
        """Handle delete key - delete selected node."""
        # This is handled by the main app through menu
        pass

    def zoom(self, factor, center_x=None, center_y=None):
        """Zoom the view by factor, optionally centered on a point."""
        if center_x is None:
            center_x = self.winfo_width() // 2
        if center_y is None:
            center_y = self.winfo_height() // 2

        # Get world position under cursor before zoom
        wx, wy = self._screen_to_world(center_x, center_y)

        # Apply zoom
        new_scale = self.scale * factor
        if 0.2 <= new_scale <= 3.0:  # Limit zoom range
            self.scale = new_scale

            # Adjust offset to keep world position under cursor
            self.offset_x = center_x - wx * self.scale
            self.offset_y = center_y - wy * self.scale

            self.refresh()

    def reset_view(self):
        """Reset zoom and pan to defaults."""
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.refresh()
