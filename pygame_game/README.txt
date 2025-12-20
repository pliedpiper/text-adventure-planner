================================================================================
                    BENEATH THE HOUSE - PYGAME VERSION
================================================================================

A text adventure horror game about loss, obsession, and what waits in the dark.

================================================================================
                              INSTALLATION
================================================================================

1. Install Python 3.8 or higher

2. Install dependencies:
   pip install -r requirements.txt

3. Run the game:
   python game.py

================================================================================
                              CONTROLS
================================================================================

MOUSE:
  - Click on choices to select them
  - Hover over choices to highlight

KEYBOARD:
  - 1-9: Quick select choices by number
  - S: Save game
  - ESC: Return to main menu (auto-saves)

================================================================================
                              ASSET SETUP
================================================================================

The game will run without assets (showing placeholder backgrounds), but for
the full experience, add images and music to the assets folder.

DIRECTORY STRUCTURE:
  pygame_game/
  ├── game.py
  ├── requirements.txt
  ├── savegame.json (created automatically)
  └── assets/
      ├── backgrounds/
      │   └── (put .png or .jpg files here)
      └── music/
          └── (put .wav, .mp3, or .ogg files here)

ASSET NAMING:
  The game references assets by the names in game.tapln. For example:
  - "backgrounds/driveway_night.png" → assets/backgrounds/driveway_night.png
  - "music/ambient_home.wav" → assets/music/ambient_home.wav

See ASSETS_NEEDED.txt for the complete list of required assets.

================================================================================
                              SAVE FILES
================================================================================

Save data is stored in savegame.json in the game directory. This includes:
  - Current scene
  - Endings discovered
  - Scene history

The game auto-saves when you return to the main menu or reach an ending.

================================================================================
                              TROUBLESHOOTING
================================================================================

Q: The game won't start
A: Make sure pygame is installed: pip install pygame

Q: No sound is playing
A: Add music files to assets/music/ or check your system volume

Q: Text is cut off
A: The game is designed for 1280x720. Resize the window if needed.

Q: How do I reset my progress?
A: Delete the savegame.json file

================================================================================
