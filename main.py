import supervisor
import json
import microcontroller
import time

from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.hid import HIDModes
from kmk.handlers.sequences import send_string, simple_key_sequence
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.encoder import EncoderHandler
from kmk.modules.tapdance import TapDance
from kmk.extensions.RGB import RGB

# Load custom keycodes into a dictionary.
ck = {}
with open('custom-keycodes.json', 'r') as f:
    custom_keycodes_list = json.load(f)
    for kc in custom_keycodes_list:
        # Use safer alternative to eval if possible
        ck[kc['display']] = eval(kc['code'])  # Ensure the JSON content is safe and trusted

# Initialize keyboard and modules
keyboard = KMKKeyboard()
modtap = ModTap()
layers_ext = Layers()
tapdance = TapDance()

tapdance.tap_time = 400  # was org 750
keyboard.debug_enabled = True

# Extensions
rgb = RGB(
    pixel_pin=keyboard.rgb_pixel_pin, 
    num_pixels=keyboard.rgb_num_pixel, 
    hue_default=microcontroller.nvm[0] if len(microcontroller.nvm) > 0 else 0  # Ensure nvm[0] is accessible
)

def on_move_do(state):
    if state is not None:
        print(f"Encoder moved: {state['direction']}")
        if state['direction'] == -1:
            rgb.decrease_hue()
        else:
            rgb.increase_hue()
        if len(microcontroller.nvm) > 0:
            microcontroller.nvm[0] = rgb.hue

# Initialize encoder handler
import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.scanners.keypad import MatrixScanner
from kmk.scanners.encoder import RotaryioEncoder
from kmk.scanners.keypad import KeysScanner

class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        # create and register the scanner
        self.matrix = [
            KeysScanner(
                pins=[board.A0, board.MOSI],
            ),
            MatrixScanner(
                # required arguments:
                column_pins = self.col_pins,
                row_pins = self.row_pins,
                # optional arguments with defaults:
                columns_to_anodes=DiodeOrientation.COL2ROW,
            ),
            RotaryioEncoder(
                pin_a=board.A2,
                pin_b=board.A1,
            ),
            RotaryioEncoder(
                pin_a=board.SCK,  # Pin for the second encoder
                pin_b=board.MISO,  # Pin for the second encoder
            )
        ]

    row_pins = (board.D7, board.D8, board.D9)
    col_pins = (board.D3, board.D4, board.D5, board.D6)
    diode_orientation = DiodeOrientation.COL2ROW
    rgb_pixel_pin = board.D10
    rgb_num_pixel = 4
    rgb_encoder_a = board.SCK
    rgb_encoder_b = board.MISO
    # Uncomment the following lines if you want to use the RGB encoder in the future
    rgb_encoder = RGBEncoder(
         pin_a=rgb_encoder_a,
         pin_b=rgb_encoder_b,
     )
encoder_handler = EncoderHandler()
encoder_handler.pins = ((keyboard.rgb_encoder_a, keyboard.rgb_encoder_b, None, False),)
encoder_handler.on_move_do = lambda x, y, state: on_move_do(state)
encoder_handler.map = [((KC.RGB_HUD, KC.RGB_HUI, KC.RGB_TOG),),]

# Append extensions and modules
keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(rgb)
keyboard.extensions.append(encoder_handler)
keyboard.modules.append(layers_ext)
keyboard.modules.append(modtap)
keyboard.modules.append(tapdance)

_______ = KC.TRNS
xxxxxxx = KC.NO

def button_press_feedback():
    rgb.set_hsv_fill(85, 255, 50)  # Dark green color in HSV (hue=85, saturation=255, value=50)

def reset_color():
    # Revert to the previous color
    current_hue = rgb.hue
    current_sat = rgb.sat
    current_val = rgb.val
    rgb.set_hsv_fill(current_hue, current_sat, current_val)

# Define a flag to track key press state
key_pressed = False

def before_matrix_scan():
    global key_pressed
    if keyboard.keys_pressed and not key_pressed:
        key_pressed = True
        button_press_feedback()

def after_matrix_scan():
    global key_pressed
    if not keyboard.keys_pressed and key_pressed:
        key_pressed = False
        reset_color()

keyboard.before_matrix_scan = before_matrix_scan
keyboard.after_matrix_scan = after_matrix_scan

# Define keymap
keyboard.keymap = [
    # Layer 0
    [
        # Encoder press buttons
        KC.AUDIO_MUTE, KC.RGB_TOG,
        # Row 1
        ck['ARCH'],
        KC.TD(ck['EVERNOTE'], ck['IAWRITTER'], ck['GOOGLE_DOCS'],),
        KC.TD(ck['CALANDER'], ck['GOOGLE_CALANDER']),
        ck['CHATGPT'],
        # Row 2
        ck['CURSOR'],
        KC.TD(ck['DOWNLOADS'], ck['PREFERENCES']),
        KC.TD(ck['MESSAGES'], ck['DISCORD'], ck['SLACK']),
        KC.TD(ck['ZOOM'], ck['GOOGLE_MEET']),
        # Row 3
        ck['FIGMA'],
        ck['TECHMEME'],
        ck['TWITTER'],
        ck['YOUTUBE'],
        # Encoder turn options
        KC.AUDIO_VOL_DOWN, KC.AUDIO_VOL_UP,
    ],
    # Layer 1
    [
        # Encoder press buttons
        KC.AUDIO_MUTE, KC.RGB_TOG,
        # Row 1
        KC.KP_7, KC.KP_8, KC.KP_9, KC.KP_ASTERISK,
        # Row 2
        KC.KP_4, KC.KP_5, KC.KP_6, KC.KP_MINUS,
        # Row 3
        KC.KP_1, KC.KP_2, KC.KP_3, KC.KP_PLUS,
        # Encoder turn options
        KC.AUDIO_VOL_DOWN, KC.AUDIO_VOL_UP
    ],
]

if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.USB)
