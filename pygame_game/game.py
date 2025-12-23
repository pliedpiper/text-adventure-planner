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

# Epilogue text for each ending
EPILOGUE_TEXT = {
    "ending_communion": "Six months later.\n\nYou've become one with something ancient and unknowable... but the bills still need paying.\n\nTime to find a job.",
    "ending_escape": "Six months later.\n\nYou escaped the darkness below, but you can't escape capitalism.\n\nTime to find a job.",
    "ending_defiance": "Six months later.\n\nYou defied an eldritch horror... but your landlord is somehow scarier.\n\nTime to find a job.",
    "ending_understanding": "Six months later.\n\nYou understand the cosmic truth now... and the truth is you need a paycheck.\n\nTime to find a job."
}

# Loading messages for job application
LOADING_MESSAGES = [
    "Submitting application...",
    "Reviewing qualifications...",
    "Checking availability...",
    "Consulting hiring manager...",
    "Processing background check...",
    "Finalizing decision..."
]


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


class TextInput:
    """An editable text input field."""

    def __init__(self, x, y, width, height, label, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.font = font
        self.text = ""
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0

    def draw(self, surface):
        # Label above the input
        label_surface = self.font.render(self.label, True, COLOR_DIM)
        surface.blit(label_surface, (self.rect.x, self.rect.y - 25))

        # Background
        bg_color = (40, 40, 40) if self.active else (25, 25, 25)
        pygame.draw.rect(surface, bg_color, self.rect)

        # Border
        border_color = COLOR_HOVER_RED if self.active else COLOR_DARK_RED
        pygame.draw.rect(surface, border_color, self.rect, 2)

        # Text
        display_text = self.text
        if self.active and self.cursor_visible:
            display_text += "|"
        text_surface = self.font.render(display_text, True, COLOR_WHITE)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))

        # Clip text to fit in box
        clip_rect = pygame.Rect(self.rect.x + 5, self.rect.y, self.rect.width - 10, self.rect.height)
        surface.set_clip(clip_rect)
        surface.blit(text_surface, text_rect)
        surface.set_clip(None)

    def update(self, dt):
        # Blink cursor
        if self.active:
            self.cursor_timer += dt
            if self.cursor_timer >= 500:  # Blink every 500ms
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            if self.active:
                self.cursor_visible = True
                self.cursor_timer = 0

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                return "next"  # Signal to move to next field
            elif event.unicode.isprintable() and len(self.text) < 50:
                self.text += event.unicode
        return None


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
        self.mode = "menu"  # menu, playing, epilogue, job_application, job_loading, job_result
        self.menu_buttons = []
        self._create_menu_buttons()

        # Epilogue/Job application state
        self.current_ending = None
        self.epilogue_button = None
        self.job_inputs = []
        self.job_submit_button = None
        self.loading_start_time = 0
        self.loading_message_index = 0
        self.applicant_name = ""
        self.result_button = None

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

            # Check if this is an ending - add epilogue button
            if scene_id.startswith("ending_"):
                self.current_ending = scene_id
                self.state.save()
                # Create epilogue choice instead of normal choices
                self.choice_buttons = []
                epilogue_button = Button(
                    SCREEN_WIDTH // 2 - CHOICE_WIDTH // 2,
                    IMAGE_AREA_HEIGHT + 50,
                    CHOICE_WIDTH, CHOICE_HEIGHT,
                    "Epilogue",
                    self.font_choice
                )
                epilogue_button.next_scene = "__epilogue__"
                self.choice_buttons.append(epilogue_button)
            else:
                self._create_choice_buttons(scene.get("choices", []))

            # Handle music
            music = scene.get("music", "")
            if music:
                self.assets.play_music(music.replace("music/", "").replace(".wav", ""))

        elif not scene_id:
            # Empty next_scene means return to menu
            self.mode = "menu"
            self.state.current_scene = "start"
        elif scene_id == "__epilogue__":
            # Special case: go to epilogue screen
            self.mode = "epilogue"
            self.epilogue_button = None  # Will be created in draw_epilogue

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

        # Debug info (scene, music, background) - commented out for cleaner look
        # bg_debug = scene.get("background", "") or "empty"
        # music_debug = self.assets.current_music or "empty"

        # debug_text = self.font_text.render(
        #     f"Scene: {self.state.current_scene} | Music: {music_debug} | BG: {bg_debug}",
        #     True, (50, 50, 50)
        # )
        # self.screen.blit(debug_text, (10, 10))

    def _create_job_form(self):
        """Create the job application form inputs."""
        self.job_inputs = []
        form_x = SCREEN_WIDTH // 2 - 300
        form_y = 200
        input_height = 40
        input_spacing = 70

        fields = ["Full Name", "Email Address", "Phone Number", "Street Address", "Previous Work Experience"]
        for i, label in enumerate(fields):
            text_input = TextInput(
                form_x, form_y + i * input_spacing,
                600, input_height,
                label, self.font_text
            )
            self.job_inputs.append(text_input)

        # Activate first input
        if self.job_inputs:
            self.job_inputs[0].active = True

        # Submit button
        self.job_submit_button = Button(
            SCREEN_WIDTH // 2 - 150,
            form_y + len(fields) * input_spacing + 30,
            300, 50,
            "Submit Application",
            self.font_choice
        )

    def draw_epilogue(self):
        """Draw the epilogue screen."""
        self.screen.fill(COLOR_BLACK)

        # Title
        title = self.font_title.render("EPILOGUE", True, COLOR_DARK_RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Epilogue text
        epilogue_text = EPILOGUE_TEXT.get(self.current_ending, EPILOGUE_TEXT["ending_escape"])
        self.text_renderer.render(
            self.screen, epilogue_text,
            SCREEN_WIDTH // 2 - 350,
            200
        )

        # Continue button
        if not self.epilogue_button:
            self.epilogue_button = Button(
                SCREEN_WIDTH // 2 - 150,
                SCREEN_HEIGHT - 150,
                300, 50,
                "Search for Jobs",
                self.font_choice
            )
        self.epilogue_button.draw(self.screen)

    def draw_job_application(self):
        """Draw the job application form."""
        self.screen.fill(COLOR_BLACK)

        # McDonald's header
        title = self.font_title.render("McDonald's", True, (255, 199, 0))  # McDonald's yellow
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 60))
        self.screen.blit(title, title_rect)

        subtitle = self.font_text.render("Employment Application", True, COLOR_WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 110))
        self.screen.blit(subtitle, subtitle_rect)

        tagline = self.font_text.render("I'm Lovin' It", True, (255, 199, 0))
        tagline_rect = tagline.get_rect(center=(SCREEN_WIDTH // 2, 140))
        self.screen.blit(tagline, tagline_rect)

        # Draw form inputs
        for text_input in self.job_inputs:
            text_input.draw(self.screen)

        # Submit button
        if self.job_submit_button:
            self.job_submit_button.draw(self.screen)

    def draw_loading(self):
        """Draw the loading screen with fake processing."""
        self.screen.fill(COLOR_BLACK)

        # McDonald's header
        title = self.font_title.render("McDonald's", True, (255, 199, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title, title_rect)

        # Current loading message
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.loading_start_time

        # Update message every 800ms
        self.loading_message_index = min(
            int(elapsed / 800),
            len(LOADING_MESSAGES) - 1
        )

        message = LOADING_MESSAGES[self.loading_message_index]
        message_surface = self.font_text.render(message, True, COLOR_WHITE)
        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(message_surface, message_rect)

        # Animated dots
        dots = "." * ((int(elapsed / 300) % 4))
        dots_surface = self.font_text.render(dots, True, COLOR_WHITE)
        self.screen.blit(dots_surface, (message_rect.right + 5, message_rect.y))

        # Progress bar
        bar_width = 400
        bar_height = 20
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = SCREEN_HEIGHT // 2 + 50

        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        progress = min(elapsed / 5000, 1.0)  # 5 seconds total
        pygame.draw.rect(self.screen, (255, 199, 0), (bar_x, bar_y, int(bar_width * progress), bar_height))
        pygame.draw.rect(self.screen, COLOR_DARK_RED, (bar_x, bar_y, bar_width, bar_height), 2)

        # Check if loading is done
        if elapsed >= 5000:
            self.mode = "job_result"
            self._create_result_button()

    def _create_result_button(self):
        """Create the button for the result screen."""
        self.result_button = Button(
            SCREEN_WIDTH // 2 - 150,
            SCREEN_HEIGHT - 150,
            300, 50,
            "Return to Menu",
            self.font_choice
        )

    def draw_job_result(self):
        """Draw the rejection letter."""
        self.screen.fill(COLOR_BLACK)

        # Rejection letter
        letter_x = SCREEN_WIDTH // 2 - 350
        y = 100

        # Header
        header = self.font_title.render("McDonald's", True, (255, 199, 0))
        header_rect = header.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.screen.blit(header, header_rect)
        y += 80

        # Letter content
        name = self.applicant_name if self.applicant_name else "Applicant"
        letter_lines = [
            f"Dear {name},",
            "",
            "Thank you for your interest in joining the McDonald's team!",
            "",
            "After careful review of your application, we regret to inform",
            "you that we will not be moving forward with your candidacy",
            "at this time.",
            "",
            "We had many qualified applicants and unfortunately cannot",
            "offer positions to everyone.",
            "",
            "We encourage you to apply again in the future.",
            "",
            "Best regards,",
            "McDonald's Hiring Team",
            "",
            "",
            "P.S. - Have you considered applying at Wendy's?"
        ]

        for line in letter_lines:
            if line:
                line_surface = self.font_text.render(line, True, COLOR_WHITE)
                self.screen.blit(line_surface, (letter_x, y))
            y += 30

        # Return button
        if self.result_button:
            self.result_button.draw(self.screen)

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

    def handle_epilogue_input(self, event):
        """Handle input on epilogue screen."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.epilogue_button and self.epilogue_button.is_clicked(mouse_pos, True):
                self.mode = "job_application"
                self._create_job_form()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.mode = "job_application"
                self._create_job_form()

    def handle_job_application_input(self, event):
        """Handle input on job application form."""
        # Handle text input for all fields
        for i, text_input in enumerate(self.job_inputs):
            result = text_input.handle_event(event)
            if result == "next":
                # Move to next field
                text_input.active = False
                next_index = (i + 1) % len(self.job_inputs)
                self.job_inputs[next_index].active = True
                break

        # Handle submit button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.job_submit_button and self.job_submit_button.is_clicked(mouse_pos, True):
                # Save the applicant name for the rejection letter
                if self.job_inputs:
                    self.applicant_name = self.job_inputs[0].text
                self.mode = "job_loading"
                self.loading_start_time = pygame.time.get_ticks()
                self.loading_message_index = 0

    def handle_job_result_input(self, event):
        """Handle input on result screen."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.result_button and self.result_button.is_clicked(mouse_pos, True):
                self.mode = "menu"
                self.current_ending = None
                self.epilogue_button = None
                self.result_button = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.mode = "menu"
                self.current_ending = None
                self.epilogue_button = None
                self.result_button = None

    def update(self):
        """Update game state."""
        mouse_pos = pygame.mouse.get_pos()
        dt = self.clock.get_time()  # Time since last frame in ms

        if self.mode == "menu":
            for button in self.menu_buttons:
                button.check_hover(mouse_pos)
        elif self.mode == "playing":
            for button in self.choice_buttons:
                button.check_hover(mouse_pos)
        elif self.mode == "epilogue":
            if self.epilogue_button:
                self.epilogue_button.check_hover(mouse_pos)
        elif self.mode == "job_application":
            for text_input in self.job_inputs:
                text_input.update(dt)
            if self.job_submit_button:
                self.job_submit_button.check_hover(mouse_pos)
        elif self.mode == "job_result":
            if self.result_button:
                self.result_button.check_hover(mouse_pos)

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
                elif self.mode == "playing":
                    self.handle_game_input(event)
                elif self.mode == "epilogue":
                    self.handle_epilogue_input(event)
                elif self.mode == "job_application":
                    self.handle_job_application_input(event)
                elif self.mode == "job_result":
                    self.handle_job_result_input(event)
                # job_loading has no input - just waits

            # Update
            self.update()

            # Draw
            if self.mode == "menu":
                self.draw_menu()
            elif self.mode == "playing":
                self.draw_game()
            elif self.mode == "epilogue":
                self.draw_epilogue()
            elif self.mode == "job_application":
                self.draw_job_application()
            elif self.mode == "job_loading":
                self.draw_loading()
            elif self.mode == "job_result":
                self.draw_job_result()

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
