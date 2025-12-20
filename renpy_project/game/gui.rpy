## gui.rpy - Dark horror theme for "Beneath the House"

init python:
    gui.init(1920, 1080)

## Colors - Dark, unsettling palette
define gui.accent_color = '#8b0000'  # Dark red
define gui.idle_color = '#707070'
define gui.idle_small_color = '#606060'
define gui.hover_color = '#c41e3a'  # Brighter red on hover
define gui.selected_color = '#ffffff'
define gui.insensitive_color = '#3030307f'
define gui.muted_color = '#404040'
define gui.hover_muted_color = '#505050'
define gui.text_color = '#d0d0d0'
define gui.interface_text_color = '#d0d0d0'

## Fonts
define gui.text_font = "DejaVuSans.ttf"
define gui.name_text_font = "DejaVuSans.ttf"
define gui.interface_text_font = "DejaVuSans.ttf"

## Font sizes
define gui.text_size = 28
define gui.name_text_size = 36
define gui.interface_text_size = 28
define gui.label_text_size = 32
define gui.notify_text_size = 22
define gui.title_text_size = 64

## Main and Game Menus
define gui.main_menu_background_color = '#0a0a0a'
define gui.game_menu_background_color = '#0a0a0aee'

## Dialogue
define gui.textbox_height = 278
define gui.textbox_yalign = 1.0

define gui.name_xpos = 360
define gui.name_ypos = 0
define gui.name_xalign = 0.0

define gui.namebox_width = None
define gui.namebox_height = None
define gui.namebox_borders = Borders(5, 5, 5, 5)
define gui.namebox_tile = False

define gui.dialogue_xpos = 402
define gui.dialogue_ypos = 75
define gui.dialogue_width = 1116
define gui.dialogue_text_xalign = 0.0

## Buttons
define gui.button_width = None
define gui.button_height = None
define gui.button_borders = Borders(6, 6, 6, 6)
define gui.button_tile = False
define gui.button_text_font = gui.interface_text_font
define gui.button_text_size = gui.interface_text_size
define gui.button_text_idle_color = gui.idle_color
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.selected_color
define gui.button_text_insensitive_color = gui.insensitive_color

## Choice buttons (the main gameplay element)
define gui.choice_button_width = 1185
define gui.choice_button_height = None
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(150, 8, 150, 8)
define gui.choice_button_text_font = gui.text_font
define gui.choice_button_text_size = gui.text_size
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = '#a0a0a0'
define gui.choice_button_text_hover_color = '#ffffff'
define gui.choice_button_text_insensitive_color = '#4040407f'

## File Slot Buttons
define gui.slot_button_width = 414
define gui.slot_button_height = 309
define gui.slot_button_borders = Borders(15, 15, 15, 15)
define gui.slot_button_text_size = 21
define gui.slot_button_text_xalign = 0.5
define gui.slot_button_text_idle_color = gui.idle_small_color
define gui.slot_button_text_selected_idle_color = gui.selected_color
define gui.slot_button_text_selected_hover_color = gui.hover_color

define config.thumbnail_width = 384
define config.thumbnail_height = 216

define gui.file_slot_cols = 3
define gui.file_slot_rows = 2

## Positioning and Spacing
define gui.navigation_xpos = 60
define gui.skip_ypos = 15
define gui.notify_ypos = 68

define gui.choice_spacing = 33
define gui.navigation_spacing = 6
define gui.pref_spacing = 15
define gui.pref_button_spacing = 0
define gui.page_spacing = 0
define gui.slot_spacing = 15

## Frames
define gui.frame_borders = Borders(6, 6, 6, 6)
define gui.confirm_frame_borders = Borders(60, 60, 60, 60)
define gui.skip_frame_borders = Borders(24, 8, 75, 8)
define gui.notify_frame_borders = Borders(24, 8, 60, 8)
define gui.frame_tile = False

## Bars, Scrollbars, and Sliders
define gui.bar_size = 38
define gui.scrollbar_size = 18
define gui.slider_size = 38
define gui.bar_tile = False
define gui.scrollbar_tile = False
define gui.slider_tile = False

define gui.bar_borders = Borders(6, 6, 6, 6)
define gui.scrollbar_borders = Borders(6, 6, 6, 6)
define gui.slider_borders = Borders(6, 6, 6, 6)
define gui.vbar_borders = Borders(6, 6, 6, 6)
define gui.vscrollbar_borders = Borders(6, 6, 6, 6)
define gui.vslider_borders = Borders(6, 6, 6, 6)

define gui.unscrollable = "hide"

## History
define gui.history_height = 210
define gui.history_name_xpos = 233
define gui.history_name_ypos = 0
define gui.history_name_width = 233
define gui.history_name_xalign = 1.0
define gui.history_text_xpos = 255
define gui.history_text_ypos = 3
define gui.history_text_width = 1110
define gui.history_text_xalign = 0.0

## NVL-Mode (for longer text passages)
define gui.nvl_borders = Borders(0, 15, 0, 30)
define gui.nvl_list_length = 6
define gui.nvl_height = 173
define gui.nvl_spacing = 15
define gui.nvl_name_xpos = 645
define gui.nvl_name_ypos = 0
define gui.nvl_name_width = 225
define gui.nvl_name_xalign = 1.0
define gui.nvl_text_xpos = 675
define gui.nvl_text_ypos = 12
define gui.nvl_text_width = 885
define gui.nvl_text_xalign = 0.0
define gui.nvl_thought_xpos = 360
define gui.nvl_thought_width = 1170
define gui.nvl_thought_xalign = 0.0
define gui.nvl_button_xpos = 675
define gui.nvl_button_xalign = 0.0

## Mobile adjustments
init python:
    @gui.variant
    def small():
        gui.text_size = 45
        gui.name_text_size = 54
        gui.notify_text_size = 38
        gui.interface_text_size = 45
        gui.button_text_size = 45
        gui.label_text_size = 51

        gui.textbox_height = 375
        gui.name_xpos = 120
        gui.dialogue_xpos = 135
        gui.dialogue_width = 1650

        gui.choice_button_width = 1860
        gui.choice_button_text_size = 45

        gui.navigation_spacing = 30
        gui.pref_button_spacing = 15

        gui.history_height = 285
        gui.history_text_width = 1035

        gui.quick_button_text_size = 30

        gui.nvl_height = 255
        gui.nvl_name_width = 458
        gui.nvl_name_xpos = 488
        gui.nvl_text_width = 1373
        gui.nvl_text_xpos = 518
        gui.nvl_text_ypos = 8
        gui.nvl_thought_width = 1860
        gui.nvl_thought_xpos = 30
        gui.nvl_button_width = 1860
        gui.nvl_button_xpos = 30
