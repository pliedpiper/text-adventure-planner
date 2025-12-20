"""
Scene Editor - Side panel for editing scene properties.
"""

import tkinter as tk
from tkinter import ttk

# Colors
PANEL_BG = "#3c3c3c"
FIELD_BG = "#2b2b2b"
TEXT_COLOR = "#e0e0e0"
ACCENT_COLOR = "#5c9aff"
DELETE_COLOR = "#c75050"


class SceneEditor(ttk.Frame):
    def __init__(self, parent, on_update, on_delete_choice, on_add_choice):
        super().__init__(parent, style="Panel.TFrame")

        self.on_update = on_update
        self.on_delete_choice = on_delete_choice
        self.on_add_choice = on_add_choice

        self.current_scene = None
        self.all_scene_ids = []
        self.choice_widgets = []

        self._setup_styles()
        self._create_widgets()

    def _setup_styles(self):
        """Configure styles for editor widgets."""
        style = ttk.Style()
        style.configure("Panel.TFrame", background=PANEL_BG)
        style.configure("Panel.TLabel", background=PANEL_BG, foreground=TEXT_COLOR)
        style.configure("Panel.TEntry", fieldbackground=FIELD_BG, foreground=TEXT_COLOR)
        style.configure("Header.TLabel", background=PANEL_BG, foreground=TEXT_COLOR,
                       font=("Helvetica", 14, "bold"))
        style.configure("SubHeader.TLabel", background=PANEL_BG, foreground=TEXT_COLOR,
                       font=("Helvetica", 11, "bold"))

    def _create_widgets(self):
        """Create the editor form."""
        # Main container with padding
        container = ttk.Frame(self, style="Panel.TFrame", padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        # Header
        self.header_label = ttk.Label(container, text="No Scene Selected",
                                      style="Header.TLabel")
        self.header_label.pack(anchor="w", pady=(0, 15))

        # Scene ID
        ttk.Label(container, text="Scene ID:", style="Panel.TLabel").pack(anchor="w")
        self.id_var = tk.StringVar()
        self.id_entry = tk.Entry(container, textvariable=self.id_var,
                                 bg=FIELD_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                                 relief="flat", font=("Helvetica", 10))
        self.id_entry.pack(fill="x", pady=(2, 10))
        self.id_var.trace_add("write", self._on_id_change)

        # Background
        ttk.Label(container, text="Background:", style="Panel.TLabel").pack(anchor="w")
        self.bg_var = tk.StringVar()
        self.bg_entry = tk.Entry(container, textvariable=self.bg_var,
                                bg=FIELD_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                                relief="flat", font=("Helvetica", 10))
        self.bg_entry.pack(fill="x", pady=(2, 10))
        self.bg_var.trace_add("write", self._on_field_change)

        # Music
        ttk.Label(container, text="Music:", style="Panel.TLabel").pack(anchor="w")
        self.music_var = tk.StringVar()
        self.music_entry = tk.Entry(container, textvariable=self.music_var,
                                   bg=FIELD_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                                   relief="flat", font=("Helvetica", 10))
        self.music_entry.pack(fill="x", pady=(2, 10))
        self.music_var.trace_add("write", self._on_field_change)

        # Text (multiline)
        ttk.Label(container, text="Scene Text:", style="Panel.TLabel").pack(anchor="w")
        text_frame = ttk.Frame(container, style="Panel.TFrame")
        text_frame.pack(fill="x", pady=(2, 10))

        self.text_box = tk.Text(text_frame, height=5, wrap="word",
                               bg=FIELD_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                               relief="flat", font=("Helvetica", 10))
        self.text_box.pack(side="left", fill="both", expand=True)
        self.text_box.bind("<KeyRelease>", self._on_field_change)

        text_scroll = ttk.Scrollbar(text_frame, orient="vertical",
                                   command=self.text_box.yview)
        text_scroll.pack(side="right", fill="y")
        self.text_box.configure(yscrollcommand=text_scroll.set)

        # Choices section
        ttk.Label(container, text="Choices:", style="SubHeader.TLabel").pack(anchor="w", pady=(10, 5))

        # Choices container (scrollable)
        self.choices_frame = ttk.Frame(container, style="Panel.TFrame")
        self.choices_frame.pack(fill="both", expand=True)

        # Add choice button
        self.add_choice_btn = tk.Button(
            container, text="+ Add Choice",
            bg=ACCENT_COLOR, fg="white", relief="flat",
            font=("Helvetica", 10, "bold"),
            command=self._on_add_choice
        )
        self.add_choice_btn.pack(fill="x", pady=(10, 0))

        # Initially disable all fields
        self._set_enabled(False)

    def _set_enabled(self, enabled):
        """Enable or disable all input fields."""
        state = "normal" if enabled else "disabled"
        self.id_entry.config(state=state)
        self.bg_entry.config(state=state)
        self.music_entry.config(state=state)
        self.text_box.config(state=state)
        self.add_choice_btn.config(state=state)

    def load_scene(self, scene_data, all_scene_ids):
        """Load scene data into the editor."""
        self.current_scene = scene_data
        self.all_scene_ids = all_scene_ids

        # Temporarily disable trace to avoid triggering updates
        self._updating = True

        self.header_label.config(text=f"Scene: {scene_data.get('id', 'unknown')}")

        self.id_var.set(scene_data.get("id", ""))
        self.bg_var.set(scene_data.get("background", ""))
        self.music_var.set(scene_data.get("music", ""))

        self.text_box.delete("1.0", tk.END)
        self.text_box.insert("1.0", scene_data.get("text", ""))

        self._rebuild_choices()
        self._set_enabled(True)

        self._updating = False

    def clear(self):
        """Clear the editor (no scene selected)."""
        self.current_scene = None
        self._updating = True

        self.header_label.config(text="No Scene Selected")
        self.id_var.set("")
        self.bg_var.set("")
        self.music_var.set("")
        self.text_box.delete("1.0", tk.END)
        self._clear_choices()
        self._set_enabled(False)

        self._updating = False

    def _rebuild_choices(self):
        """Rebuild the choices widgets."""
        self._clear_choices()

        if not self.current_scene:
            return

        choices = self.current_scene.get("choices", [])
        for i, choice in enumerate(choices):
            self._add_choice_widget(i, choice)

    def _clear_choices(self):
        """Remove all choice widgets."""
        for widget in self.choice_widgets:
            widget.destroy()
        self.choice_widgets = []

    def _add_choice_widget(self, index, choice):
        """Add a widget for editing a single choice."""
        frame = ttk.Frame(self.choices_frame, style="Panel.TFrame")
        frame.pack(fill="x", pady=2)
        self.choice_widgets.append(frame)

        # Choice label entry
        label_var = tk.StringVar(value=choice.get("label", ""))
        label_entry = tk.Entry(frame, textvariable=label_var, width=20,
                              bg=FIELD_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                              relief="flat", font=("Helvetica", 9))
        label_entry.pack(side="left", padx=(0, 5))

        # Arrow
        arrow_label = ttk.Label(frame, text="→", style="Panel.TLabel")
        arrow_label.pack(side="left", padx=2)

        # Target scene dropdown
        target_var = tk.StringVar(value=choice.get("next_scene", ""))
        target_combo = ttk.Combobox(frame, textvariable=target_var, width=15,
                                   values=self.all_scene_ids)
        target_combo.pack(side="left", padx=(0, 5))

        # Delete button
        del_btn = tk.Button(frame, text="×", bg=DELETE_COLOR, fg="white",
                           relief="flat", width=2, font=("Helvetica", 10, "bold"),
                           command=lambda idx=index: self._on_delete_choice(idx))
        del_btn.pack(side="right")

        # Bind changes
        def on_choice_change(*args, idx=index, lv=label_var, tv=target_var):
            if hasattr(self, '_updating') and self._updating:
                return
            if self.current_scene:
                choices = self.current_scene.get("choices", [])
                if idx < len(choices):
                    choices[idx]["label"] = lv.get()
                    choices[idx]["next_scene"] = tv.get()
                    self._notify_update()

        label_var.trace_add("write", on_choice_change)
        target_var.trace_add("write", on_choice_change)

    def _on_field_change(self, *args):
        """Handle field value change."""
        if hasattr(self, '_updating') and self._updating:
            return
        self._notify_update()

    def _on_id_change(self, *args):
        """Handle scene ID change and auto-fill background/music."""
        if hasattr(self, '_updating') and self._updating:
            return

        scene_id = self.id_var.get().strip().lower().replace(" ", "_")

        if scene_id:
            # Auto-fill background if empty or following the pattern
            current_bg = self.bg_var.get()
            if not current_bg or self._matches_bg_pattern(current_bg):
                self._updating = True
                self.bg_var.set(f"backgrounds/{scene_id}.png")
                self._updating = False

            # Auto-fill music if empty or following the pattern
            current_music = self.music_var.get()
            if not current_music or self._matches_music_pattern(current_music):
                self._updating = True
                self.music_var.set(f"music/{scene_id}.wav")
                self._updating = False

        self._notify_update()

    def _matches_bg_pattern(self, value):
        """Check if value matches the auto-fill background pattern."""
        return value.startswith("backgrounds/") and value.endswith(".png")

    def _matches_music_pattern(self, value):
        """Check if value matches the auto-fill music pattern."""
        return value.startswith("music/") and value.endswith(".wav")

    def _notify_update(self):
        """Notify parent of scene update."""
        if not self.current_scene:
            return

        scene_data = {
            "id": self.id_var.get().strip().lower().replace(" ", "_"),
            "background": self.bg_var.get(),
            "music": self.music_var.get(),
            "text": self.text_box.get("1.0", tk.END).strip(),
            "choices": self.current_scene.get("choices", [])
        }
        self.on_update(scene_data)

    def _on_delete_choice(self, index):
        """Handle choice deletion."""
        if self.current_scene:
            self.on_delete_choice(self.current_scene.get("id"), index)
            # Reload to refresh indices
            if self.current_scene:
                self.load_scene(self.current_scene, self.all_scene_ids)

    def _on_add_choice(self):
        """Handle add choice button."""
        if self.current_scene:
            self.on_add_choice(self.current_scene.get("id"))
