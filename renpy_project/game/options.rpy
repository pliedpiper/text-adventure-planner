## options.rpy - Game configuration for "Beneath the House"

define config.name = _("Beneath the House")
define config.version = "1.0"

define gui.show_name = True
define gui.about = _p("""
A horror text adventure about loss, obsession, and what waits in the dark.

Your sibling has been chronically ill for years. When they join a mysterious
group called "The Threshold Assembly," you watch them change—becoming
healthier, happier, but somehow wrong. Then they disappear through a door
that shouldn't exist, beneath the house you grew up in.

Will you follow them into the dark?
""")

define build.name = "BeneathTheHouse"

## Sounds and music
define config.has_sound = True
define config.has_music = True
define config.has_voice = False

define config.main_menu_music = "music/ambient_dark.wav"

## Transitions
define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = dissolve
define config.end_game_transition = fade

## Window settings
define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

## Save/Load
define config.save_directory = "BeneathTheHouse-1657382947"
define config.has_autosave = True
define config.autosave_on_choice = True

## Skip settings
define config.allow_skipping = True
define config.fast_skipping = False
define config.skip_indicator = True

## Auto-forward
define config.has_autosave = True
define config.auto_forward_time = 15

## Rollback
define config.hard_rollback_limit = 100
define config.rollback_length = 128

## Layers
define config.layers = [ 'master', 'transient', 'screens', 'overlay' ]

## Image settings
define config.image_cache_size = 8
define config.predict_statements = 50

## Build configuration
init python:
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    build.classify('game/**.png', 'archive')
    build.classify('game/**.jpg', 'archive')
    build.classify('game/**.wav', 'archive')
    build.classify('game/**.mp3', 'archive')
    build.classify('game/**.ogg', 'archive')

    build.documentation('*.html')
    build.documentation('*.txt')
