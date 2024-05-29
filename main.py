import json
import microcontroller

from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.hid import HIDModes
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.encoder import EncoderHandler
from kmk.modules.tapdance import TapDance
from kmk.extensions.RGB import RGB

# Load custom keycodes into a dictionary.
ck = {}
try:
    with open('custom-keycodes.json', 'r') as f:
        custom_keycodes_list = json.load(f)
        for kc in custom_keycodes_list:
            # Use a safer alternative to eval if possible
            ck[kc['display']] = eval(kc['code'])  # Be cautious with eval
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading custom keycodes: {e}")

# Initialize keyboard and modules
keyboard = KMKKeyboard()
modtap = ModTap()
layers_ext = Layers()
tapdance = TapDance()

tapdance.tap_time = 400  # was org 750
keyboard.debug_enabled = False

# Extensions
rgb = RGB(
    pixel_pin=keyboard.rgb_pixel_pin, 
    num_pixels=keyboard.rgb_num_pixel, 
    hue_default=microcontroller.nvm[0]
)

def on_move_do(state):
    print(f"Encoder moved: {state}")  # Debug statement
    if state is not None and state['direction'] == -1:
        rgb.decrease_hue()
        keyboard.tap_key(KC.LCMD(KC.LCTL(KC.J)))
    else:
        rgb.increase_hue()
        keyboard.tap_key(KC.LCMD(KC.LCTL(KC.L)))
    microcontroller.nvm[0] = rgb.hue

def rgb_encoder_button_press():
    print("Encoder button pressed")  # Debug statement
    keyboard.tap_key(KC.RGB_TOG)
    keyboard.tap_key(KC.K)

# Initialize encoder handler
encoder_handler = EncoderHandler(keyboard)
encoder_handler.pins = ((keyboard.rgb_encoder_a, keyboard.rgb_encoder_b, None, False),)
encoder_handler.on_move_do = lambda state: on_move_do(state)

# Append extensions and modules before using their keycodes
keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(rgb)
keyboard.extensions.append(encoder_handler)
keyboard.modules.append(layers_ext)
keyboard.modules.append(modtap)
keyboard.modules.append(tapdance)

# Ensure the keycodes are valid
try:
    encoder_handler.map = [
        ((KC.VOLD, KC.VOLU, KC.MUTE,),),  # Encoder 1: Volume control
        ((KC.RGB_HUD, KC.RGB_HUI, rgb_encoder_button_press,),)  # Encoder 2: RGB control
    ]  # Pressing the encoder button will toggle RGB and press "K"
except ValueError as e:
    print(f"Invalid key in encoder map: {e}")

_______ = KC.TRNS
xxxxxxx = KC.NO

# Define keymap
keyboard.keymap = [
    # Layer 0.
    [
        # Encoder press buttons
        xxxxxxx, xxxxxxx,
        # Row 1
        KC.TD(ck['ARCH'], ck['GMAIL']),
        KC.TD(ck['EVERNOTE'], ck['IAWRITTER'], ck['GOOGLE_DOCS']),
        KC.TD(ck['CALENDAR'], ck['GOOGLE_CALENDAR']),
        KC.TD(ck['CHATGPT'], ck['CHATGPT-WEB']),
        # Row 2
        KC.TD(ck['CURSOR'], ck['GITHUB'],ck['APPLESCRIPT-EDITOR']),
        KC.TD(ck['DOWNLOADS'], ck['FLASH-GORDON-STORAGE'], ck['DOCUMENTS'], ck['PREFERENCES']),
        KC.TD(ck['MESSAGES'], ck['DISCORD'], ck['SLACK']),
        KC.TD(ck['ZOOM'], ck['GOOGLE_MEET']),
        # Row 3
        ck['FIGMA'],
        ck['TECHMEME'],
        KC.TD(ck['TWITTER'], ck['REDDIT']),
        ck['YOUTUBE'],
    ],
    # Layer 1
    [
        # Encoder press buttons
        xxxxxxx, xxxxxxx,
        # Row 1
        KC.KP_7, KC.KP_8, KC.KP_9, KC.KP_ASTERISK,
        # Row 2
        KC.KP_4, KC.KP_5, KC.KP_6, KC.KP_MINUS,
        # Row 3
        KC.KP_1, KC.KP_2, KC.KP_3, KC.KP_PLUS,
    ],

    # Layer 2
    [
        # Encoder press buttons
        xxxxxxx, xxxxxxx,
        # Row 1
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Row 2
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Row 3
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Encoder turn options
        xxxxxxx, xxxxxxx
    ],
    # Layer 3
    #     # MIDI
    # [
    #     KC.MIDI(30),    KC.MIDI(69),      KC.MIDI(70),       xxxxxxx,
    #     KC.MIDI(67),    KC.MIDI(66),      KC.MIDI(65),       KC.MIDI(64),
    #     KC.MIDI(60),    KC.MIDI(61),      KC.MIDI(62),       KC.MIDI(63),
    # ],
    # Layer 4
    [
        # Encoder press buttons
        xxxxxxx, xxxxxxx,
        # Row 1
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Row 2
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Row 3
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Encoder turn options
        xxxxxxx, xxxxxxx
    ],
    # Layer 5
    [
        # Encoder press buttons
        xxxxxxx, xxxxxxx,
        # Row 1
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Row 2
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Row 3
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Encoder turn options
        xxxxxxx, xxxxxxx
    ],
    # Layer 6
    [
        # Encoder press buttons
        xxxxxxx, xxxxxxx,
        # Row 1
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Row 2
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Row 3
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Encoder turn options
        xxxxxxx, xxxxxxx
    ],
    # Layer 7
    [
        # Encoder press buttons
        xxxxxxx, xxxxxxx,
        # Row 1
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Row 2
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Row 3
        xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx,
        # Encoder turn options
        xxxxxxx, xxxxxxx
    ]
]

if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.USB)
