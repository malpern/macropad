# May 29th. Fully functional encoders, push encoders, and buttons. Re-adding youtube turns

# Imports
import json
import supervisor
import microcontroller
from kb import KMKKeyboard
from kmk.modules.tapdance import TapDance
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.hid import HIDModes
from kmk.handlers.sequences import simple_key_sequence
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.RGB import RGB

# Initialization
keyboard = KMKKeyboard()
layers_ext = Layers()
tapdance = TapDance()

keyboard.modules.extend([layers_ext, tapdance])

# Enable debugging
keyboard.debug_enabled = True

# RGB setup
rgb = RGB(
    pixel_pin=keyboard.rgb_pixel_pin, 
    num_pixels=keyboard.rgb_num_pixel, 
    hue_default=microcontroller.nvm[0]
)

# Load custom keycodes into a dictionary
ck = {}
with open('custom-keycodes.json', 'r') as f:
    custom_keycodes_list = json.load(f)
    for kc in custom_keycodes_list:
        if 'simple_key_sequence' in kc['code']:
            # Parse the string to extract the actual keycodes
            key_sequence = eval(kc['code'].replace('simple_key_sequence', ''))
            # Apply the simple_key_sequence function
            ck[kc['display']] = simple_key_sequence(key_sequence)
        else:
            ck[kc['display']] = getattr(KC, kc['code'], None)  # Safer alternative to eval

# Encoder handler setup
def on_move_do(state):
    if state is not None and state['direction'] == -1:
        rgb.decrease_hue()
    else:
        rgb.increase_hue()
    microcontroller.nvm[0] = rgb.hue

encoder_handler = EncoderHandler()
encoder_handler.pins = ((keyboard.rgb_encoder_a, keyboard.rgb_encoder_b, None, False),)
encoder_handler.on_move_do = lambda x, y, state: on_move_do(state)

encoder_handler.map = [
    (
        [
            KC.RGB_HUD, KC.RGB_HUI, KC.RGB_TOG,
        ],
    )
]

keyboard.extensions.extend([MediaKeys(), rgb, encoder_handler])

# Keymap
keyboard.keymap = [
    [
        # Encoder 1 & 2 button push
        KC.AUDIO_MUTE,
        simple_key_sequence([KC.RGB_TOG, KC.LCTRL, KC.LCMD, KC.K]),

        # Row 1
        KC.TD(ck['ARCH'], ck['GMAIL']),
        KC.TD(ck['EVERNOTE'], ck['IAWRITTER'], ck['GOOGLE_DOCS']),
        KC.TD(ck['CALENDAR'], ck['GOOGLE_CALENDAR']),
        KC.TD(ck['CHATGPT'], ck['CHATGPT-WEB']),
        # Row 2
        KC.TD(ck['CURSOR'], ck['GITHUB'], ck['APPLESCRIPT-EDITOR']),
        KC.TD(ck['DOWNLOADS'], ck['FLASH-GORDON-STORAGE'], ck['DOCUMENTS'], ck['PREFERENCES']),
        KC.TD(ck['MESSAGES'], ck['DISCORD'], ck['SLACK']),
        KC.TD(ck['ZOOM'], ck['GOOGLE_MEET']),
        # Row 3
        KC.TD(ck['FIGMA'], simple_key_sequence([KC.LCTRL, KC.LCMD, KC.J])),
        KC.TD(ck['TECHMEME'], simple_key_sequence([KC.LCTRL, KC.LCMD, KC.L])),
        KC.TD(ck['TWITTER'], ck['REDDIT']),
        KC.TD(ck['YOUTUBE'], simple_key_sequence([KC.LCTRL, KC.LCMD, KC.K])),

        # Encoder 1: Turn up/down 
        KC.AUDIO_VOL_DOWN,
        KC.AUDIO_VOL_UP,
    ]
]

if __name__ == '__main__': 
    keyboard.go(hid_type=HIDModes.USB)
