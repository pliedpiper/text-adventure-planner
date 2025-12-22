#!/usr/bin/env python3
"""
Emery - A Text Adventure Game
Built with Pygame
"""

import pygame
import json
import os
import sys
from pathlib import Path

# Initialize Pygame
pygame.init()
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.init()

# ============================================================================
# CONFIGURATION
# ============================================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors - Dark horror theme
COLOR_BLACK = (10, 10, 10)
COLOR_WHITE = (208, 208, 208)
COLOR_DARK_RED = (139, 0, 0)
COLOR_HOVER_RED = (196, 30, 58)
COLOR_DIM = (112, 112, 112)
COLOR_TEXT_BOX = (20, 20, 20, 100)  # More transparent text box
COLOR_CHOICE_BG = (30, 30, 30, 200)
COLOR_CHOICE_HOVER = (50, 30, 30, 220)

# Paths
BASE_DIR = Path(__file__).parent
GAME_DATA_PATH = BASE_DIR.parent / "game.tapln"
ASSETS_DIR = BASE_DIR / "assets"
BACKGROUNDS_DIR = ASSETS_DIR / "backgrounds"
MUSIC_DIR = ASSETS_DIR / "music"
SAVE_FILE = BASE_DIR / "savegame.json"

# Fonts
FONT_SIZE_TEXT = 24
FONT_SIZE_CHOICE = 22
FONT_SIZE_TITLE = 48
LINE_SPACING = 8

# Layout dimensions
IMAGE_AREA_HEIGHT = 400  # Height reserved for background image at top
TEXT_BOX_MARGIN = 50
TEXT_BOX_PADDING = 20

# Choice dimensions
CHOICE_WIDTH = 700
CHOICE_HEIGHT = 50
CHOICE_SPACING = 15
CHOICE_PADDING = 20


# ============================================================================
# GAME ENGINE
# ============================================================================

class TextRenderer:
    """Handles text wrapping and rendering."""

    def __init__(self, font, max_width, color=COLOR_WHITE):
        self.font = font
        self.max_width = max_width
        self.color = color

    def wrap_text(self, text):
        """Wrap text to fit within max_width."""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            # Handle newlines in text
            if '\n' in word:
                parts = word.split('\n')
                for i, part in enumerate(parts):
                    if i > 0:
                        lines.append(' '.join(current_line))
                        current_line = []
                    if part:
                        current_line.append(part)
            else:
                test_line = ' '.join(current_line + [word])
                if self.font.size(test_line)[0] <= self.max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def get_height(self, text, line_spacing=LINE_SPACING):
        """Calculate height of wrapped text without rendering."""
        lines = self.wrap_text(text)
        return len(lines) * (self.font.get_height() + line_spacing)

    def render(self, surface, text, x, y, line_spacing=LINE_SPACING):
        """Render wrapped text at position."""
        lines = self.wrap_text(text)
        current_y = y

        for line in lines:
            text_surface = self.font.render(line, True, self.color)
            surface.blit(text_surface, (x, current_y))
            current_y += self.font.get_height() + line_spacing

        return current_y - y  # Return total height


class Button:
    """A clickable button for choices."""

    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False

    def draw(self, surface):
        # Background
        bg_color = COLOR_CHOICE_HOVER if self.hovered else COLOR_CHOICE_BG
        bg_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        bg_surface.fill(bg_color)
        surface.blit(bg_surface, self.rect.topleft)

        # Border
        border_color = COLOR_HOVER_RED if self.hovered else COLOR_DARK_RED
        pygame.draw.rect(surface, border_color, self.rect, 2)

        # Text
        text_color = COLOR_WHITE if self.hovered else COLOR_DIM
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed


class AssetManager:
    """Handles loading and caching of assets."""

    def __init__(self):
        self.backgrounds = {}
        self.current_music = None
        self.placeholder_bg = None
        self._create_placeholder()

    def _create_placeholder(self):
        """Create a dark placeholder background for image area."""
        self.placeholder_bg = pygame.Surface((SCREEN_WIDTH, IMAGE_AREA_HEIGHT))
        self.placeholder_bg.fill(COLOR_BLACK)

        # Add subtle gradient
        for y in range(IMAGE_AREA_HEIGHT):
            alpha = int(20 * (1 - y / IMAGE_AREA_HEIGHT))
            pygame.draw.line(self.placeholder_bg, (alpha, alpha, alpha + 5),
                           (0, y), (SCREEN_WIDTH, y))

    def load_background(self, name):
        """Load a background image or return placeholder."""
        if name in self.backgrounds:
            return self.backgrounds[name]

        # Try to load the image
        possible_paths = [
            BACKGROUNDS_DIR / name,
            BACKGROUNDS_DIR / f"{name}.png",
            BACKGROUNDS_DIR / f"{name}.jpg",
        ]

        for path in possible_paths:
            if path.exists():
                try:
                    img = pygame.image.load(str(path))
                    # Scale to fit image area while preserving aspect ratio
                    img_w, img_h = img.get_size()
                    target_w, target_h = SCREEN_WIDTH, IMAGE_AREA_HEIGHT

                    # Scale to fill width, then crop height if needed
                    scale = target_w / img_w
                    new_w = target_w
                    new_h = int(img_h * scale)

                    img = pygame.transform.scale(img, (new_w, new_h))

                    # Crop to fit image area (center crop if taller)
                    if new_h > target_h:
                        crop_y = (new_h - target_h) // 2
                        img = img.subsurface((0, crop_y, target_w, target_h))

                    self.backgrounds[name] = img
                    return img
                except pygame.error:
                    pass

        # Return placeholder
        return self.placeholder_bg

    def play_music(self, name):
        """Play background music."""
        if name == self.current_music:
            return

        possible_paths = [
            MUSIC_DIR / name,
            MUSIC_DIR / f"{name}.wav",
            MUSIC_DIR / f"{name}.mp3",
            MUSIC_DIR / f"{name}.ogg",
        ]

        for path in possible_paths:
            if path.exists():
                try:
                    pygame.mixer.music.load(str(path))
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)  # Loop
                    self.current_music = name
                    return
                except pygame.error:
                    pass

    def stop_music(self):
        """Stop current music."""
        pygame.mixer.music.stop()
        self.current_music = None


class GameState:
    """Manages game state and save/load."""

    def __init__(self):
        self.current_scene = "start"
        self.endings_seen = []
        self.history = []

    def save(self):
        """Save game state to file."""
        data = {
            "current_scene": self.current_scene,
            "endings_seen": self.endings_seen,
            "history": self.history[-50:]  # Keep last 50 scenes
        }
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Save failed: {e}")
            return False

    def load(self):
        """Load game state from file."""
        if not SAVE_FILE.exists():
            return False

        try:
            with open(SAVE_FILE, 'r') as f:
                data = json.load(f)
            self.current_scene = data.get("current_scene", "start")
            self.endings_seen = data.get("endings_seen", [])
            self.history = data.get("history", [])
            return True
        except Exception as e:
            print(f"Load failed: {e}")
            return False

    def visit_scene(self, scene_id):
        """Record visiting a scene."""
        self.current_scene = scene_id
        if scene_id not in self.history:
            self.history.append(scene_id)

        # Check for endings
        if scene_id.startswith("ending_") and scene_id not in self.endings_seen:
            self.endings_seen.append(scene_id)


class Game:
    """Main game class."""

    def __init__(self):
        # Set up fullscreen display
        display_info = pygame.display.Info()
        global SCREEN_WIDTH, SCREEN_HEIGHT
        SCREEN_WIDTH = display_info.current_w
        SCREEN_HEIGHT = display_info.current_h
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Emery")
        self.clock = pygame.time.Clock()

        # Load fonts
        self.font_text = pygame.font.Font(None, FONT_SIZE_TEXT)
        self.font_choice = pygame.font.Font(None, FONT_SIZE_CHOICE)
        self.font_title = pygame.font.Font(None, FONT_SIZE_TITLE)

        # Initialize systems
        self.assets = AssetManager()
        self.state = GameState()
        self.text_renderer = TextRenderer(
            self.font_text,
            SCREEN_WIDTH - (TEXT_BOX_MARGIN * 2) - (TEXT_BOX_PADDING * 2)
        )

        # Load game data
        self.scenes = self._load_game_data()

        # UI state
        self.choice_buttons = []
        self.text_scroll = 0
        self.transition_alpha = 255
        self.transitioning = False

        # Game mode
        self.mode = "menu"  # menu, playing, ending
        self.menu_buttons = []
        self._create_menu_buttons()

    def _load_game_data(self):
        """Load game data from tapln file."""
        try:
            with open(GAME_DATA_PATH, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Game data not found at {GAME_DATA_PATH}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in game data: {e}")
            sys.exit(1)

    def _create_menu_buttons(self):
        """Create main menu buttons."""
        button_y = SCREEN_HEIGHT // 2

        self.menu_buttons = [
            Button(
                SCREEN_WIDTH // 2 - CHOICE_WIDTH // 2,
                button_y,
                CHOICE_WIDTH, CHOICE_HEIGHT,
                "New Game",
                self.font_choice
            ),
            Button(
                SCREEN_WIDTH // 2 - CHOICE_WIDTH // 2,
                button_y + CHOICE_HEIGHT + CHOICE_SPACING,
                CHOICE_WIDTH, CHOICE_HEIGHT,
                "Continue",
                self.font_choice
            ),
            Button(
                SCREEN_WIDTH // 2 - CHOICE_WIDTH // 2,
                button_y + (CHOICE_HEIGHT + CHOICE_SPACING) * 2,
                CHOICE_WIDTH, CHOICE_HEIGHT,
                "Quit",
                self.font_choice
            )
        ]

    def _create_choice_buttons(self, choices):
        """Create buttons for current scene choices."""
        self.choice_buttons = []

        if not choices:
            return

        # Calculate dynamic text box height for positioning
        scene = self.get_current_scene()
        text = scene.get("text", "")
        text_height = self.text_renderer.get_height(text)
        box_height = text_height + (TEXT_BOX_PADDING * 2)

        # Position buttons between image area and text box
        text_box_y = SCREEN_HEIGHT - box_height - 10
        total_button_height = len(choices) * CHOICE_HEIGHT + (len(choices) - 1) * CHOICE_SPACING

        # Center buttons vertically between image and text box
        available_space = text_box_y - IMAGE_AREA_HEIGHT
        start_y = IMAGE_AREA_HEIGHT + (available_space - total_button_height) // 2

        for i, choice in enumerate(choices):
            button = Button(
                SCREEN_WIDTH // 2 - CHOICE_WIDTH // 2,
                start_y + i * (CHOICE_HEIGHT + CHOICE_SPACING),
                CHOICE_WIDTH, CHOICE_HEIGHT,
                choice.get("label", "Continue"),
                self.font_choice
            )
            button.next_scene = choice.get("next_scene", "")
            self.choice_buttons.append(button)

    def get_current_scene(self):
        """Get the current scene data."""
        return self.scenes.get(self.state.current_scene, {})

    def go_to_scene(self, scene_id):
        """Transition to a new scene."""
        if scene_id and scene_id in self.scenes:
            self.state.visit_scene(scene_id)
            scene = self.get_current_scene()
            self._create_choice_buttons(scene.get("choices", []))

            # Handle music
            music = scene.get("music", "")
            if music:
                self.assets.play_music(music.replace("music/", "").replace(".wav", ""))

            # Check if this is an ending
            if scene_id.startswith("ending_"):
                self.state.save()
        elif not scene_id:
            # Empty next_scene means return to menu
            self.mode = "menu"
            self.state.current_scene = "start"

    def draw_menu(self):
        """Draw main menu."""
        # Play title music
        if self.assets.current_music != "title":
            self.assets.play_music("title")

        # Background
        self.screen.fill(COLOR_BLACK)

        # Title
        title = self.font_title.render("EMERY", True, COLOR_DARK_RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title, title_rect)

        # Subtitle
        subtitle = self.font_text.render("A Text Adventure", True, COLOR_DIM)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50))
        self.screen.blit(subtitle, subtitle_rect)

        # Endings counter
        if self.state.endings_seen:
            endings_text = f"Endings discovered: {len(self.state.endings_seen)}/4"
            endings_surface = self.font_text.render(endings_text, True, COLOR_DIM)
            self.screen.blit(endings_surface, (20, SCREEN_HEIGHT - 40))

        # Buttons
        for button in self.menu_buttons:
            button.draw(self.screen)

    def draw_game(self):
        """Draw the game screen with split layout: image on top, UI below."""
        scene = self.get_current_scene()

        # Fill background with dark color
        self.screen.fill(COLOR_BLACK)

        # Background image at top
        bg_name = scene.get("background", "").replace("backgrounds/", "").replace(".png", "")
        background = self.assets.load_background(bg_name)
        self.screen.blit(background, (0, 0))

        # Calculate text box height
        text = scene.get("text", "")
        text_height = self.text_renderer.get_height(text)
        box_height = text_height + (TEXT_BOX_PADDING * 2)

        # Text box at bottom
        text_box_y = SCREEN_HEIGHT - box_height - 10
        text_box = pygame.Surface(
            (SCREEN_WIDTH - TEXT_BOX_MARGIN * 2, box_height),
            pygame.SRCALPHA
        )
        text_box.fill(COLOR_TEXT_BOX)
        self.screen.blit(text_box, (TEXT_BOX_MARGIN, text_box_y))

        # Scene text
        self.text_renderer.render(
            self.screen, text,
            TEXT_BOX_MARGIN + TEXT_BOX_PADDING,
            text_box_y + TEXT_BOX_PADDING
        )

        # Choice buttons (between image and text box)
        for button in self.choice_buttons:
            button.draw(self.screen)

        # Debug info (scene, music, background)
        bg_debug = scene.get("background", "") or "empty"
        music_debug = self.assets.current_music or "empty"

        debug_text = self.font_text.render(
            f"Scene: {self.state.current_scene} | Music: {music_debug} | BG: {bg_debug}",
            True, (50, 50, 50)
        )
        self.screen.blit(debug_text, (10, 10))

    def handle_menu_input(self, event):
        """Handle input on menu screen."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            for i, button in enumerate(self.menu_buttons):
                if button.is_clicked(mouse_pos, True):
                    if i == 0:  # New Game
                        self.state = GameState()
                        self.go_to_scene("start")
                        self.mode = "playing"
                    elif i == 1:  # Continue
                        if self.state.load():
                            self.go_to_scene(self.state.current_scene)
                            self.mode = "playing"
                    elif i == 2:  # Quit
                        pygame.quit()
                        sys.exit()

    def handle_game_input(self, event):
        """Handle input during gameplay."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            for button in self.choice_buttons:
                if button.is_clicked(mouse_pos, True):
                    self.go_to_scene(button.next_scene)
                    break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state.save()
                self.mode = "menu"
            elif event.key == pygame.K_s:
                self.state.save()
                print("Game saved!")

            # Number keys for choices
            if pygame.K_1 <= event.key <= pygame.K_9:
                choice_num = event.key - pygame.K_1
                if choice_num < len(self.choice_buttons):
                    self.go_to_scene(self.choice_buttons[choice_num].next_scene)

    def update(self):
        """Update game state."""
        mouse_pos = pygame.mouse.get_pos()

        if self.mode == "menu":
            for button in self.menu_buttons:
                button.check_hover(mouse_pos)
        else:
            for button in self.choice_buttons:
                button.check_hover(mouse_pos)

    def run(self):
        """Main game loop."""
        running = True

        # Try to load save
        self.state.load()

        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state.save()
                    running = False

                if self.mode == "menu":
                    self.handle_menu_input(event)
                else:
                    self.handle_game_input(event)

            # Update
            self.update()

            # Draw
            if self.mode == "menu":
                self.draw_menu()
            else:
                self.draw_game()

            # Flip display
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    game = Game()
    game.run()
