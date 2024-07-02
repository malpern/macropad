# May 29th. Fully functional encoders, push encoders, and buttons. Re-adding youtube turns
# June 30. Added tap and hold on row 2, key 2 to close windows

# Imports
import json
import supervisor
import microcontroller
from kb import KMKKeyboard
from kmk.modules.tapdance import TapDance
from kmk.keys import KC, Key  # Import Key here
from kmk.modules.layers import Layers
from kmk.hid import HIDModes
from kmk.handlers.sequences import simple_key_sequence
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.RGB import RGB
from kmk.modules.holdtap import HoldTap
import kmk.handlers.stock as handlers  # Import handlers

# Initialization
keyboard = KMKKeyboard()
layers_ext = Layers()
tapdance = TapDance()
holdtap = HoldTap()

keyboard.modules.extend([layers_ext, tapdance, holdtap])

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

# Simplified activate_hazel_mode function
def activate_hazel_mode(key, keyboard, *args, **kwargs):
    # Trigger the HAZEL_MODE key sequence
    keyboard.tap_key(ck['HAZEL_MODE'])
    
    # Activate the HAZEL-MODE layer permanently
    if 1 not in keyboard.active_layers:
        keyboard.active_layers.insert(0, 1)  # Assuming HAZEL-MODE is layer 1
    
    # Print debug information
    print(f'Attempting to activate HAZEL-MODE layer')
    print(f'Active layers before: {keyboard.active_layers}')
    print(f'Current layer: {keyboard.active_layers[0]}')
    print(f'Layer 1 keymap: {keyboard.keymap[1]}')

# Define a custom key for activate_hazel_mode
ACTIVATE_HAZEL_MODE = Key(
    code=0xF001,  # Use a unique code that doesn't conflict with existing keycodes
    on_press=activate_hazel_mode,
    on_release=handlers.passthrough  # Use passthrough for release if no action is needed
)

# Define a function to deactivate HAZEL-MODE
def deactivate_hazel_mode(key, keyboard, *args, **kwargs):
    print(f"Deactivate HAZEL-MODE key pressed")
    print(f"Active layers before: {keyboard.active_layers}")
    if 1 in keyboard.active_layers:
        keyboard.active_layers.remove(1)
    print(f"Deactivated HAZEL-MODE layer")
    print(f"Active layers after: {keyboard.active_layers}")
    
    # Execute the EXIT-HAZEL custom keycode
    if 'EXIT-HAZEL' in ck:
        keyboard.tap_key(ck['EXIT-HAZEL'])
        print("Executed EXIT-HAZEL custom keycode")
    else:
        print("WARNING: EXIT-HAZEL custom keycode not found")

# Define a custom key for deactivate_hazel_mode
DEACTIVATE_HAZEL_MODE = Key(
    code=0xF002,  # Use a unique code that doesn't conflict with existing keycodes
    on_press=deactivate_hazel_mode,
    on_release=handlers.passthrough
)

# Keymap
keyboard.keymap = [
    [
        # Encoder 1 & 2 button push
        KC.AUDIO_MUTE,
        simple_key_sequence([KC.RGB_TOG, KC.LCTRL, KC.LCMD, KC.K]),

        # Row 1
        KC.TD(ck['ARCH'], ck['GMAIL']),
        KC.TD(
            KC.HT(ck['CURSOR'], ck['ZED'], prefer_hold=False),
            KC.HT(ck['MU-EDITOR'], ck['GITHUB'], prefer_hold=False),
            ck['APPLESCRIPT-EDITOR'],
            ck['VS_CODE']
        ),
        KC.TD(ck['CALENDAR'], ck['GOOGLE_CALENDAR']),
        KC.HT(
            ck['CHATGPT'],  # Tap action
            ACTIVATE_HAZEL_MODE,  # Hold action to activate HAZEL-MODE layer permanently
            prefer_hold=True
        ),

        # Row 2
        KC.TD(ck['EVERNOTE'], ck['IAWRITTER'], ck['GOOGLE_SLIDES']),
        KC.TD(
            KC.HT(ck['DOWNLOADS'], ck['CLOSE_WINDOW'], prefer_hold=False),
            ck['FLASH-GORDON-STORAGE'],
            ck['DOCUMENTS'],
            ck['PREFERENCES'],
        ),
        KC.TD(ck['MESSAGES'], ck['WHATSAPP'], ck['DISCORD'], ck['SLACK']),
        KC.TD(ck['ZOOM'], ck['GOOGLE_MEET']),

        # Row 3
        KC.TD(ck['FIGMA'], simple_key_sequence([KC.LCTRL, KC.LCMD, KC.J])),
        KC.TD(ck['TECHMEME'], simple_key_sequence([KC.LCTRL, KC.LCMD, KC.L])),
        KC.TD(ck['TWITTER'], ck['REDDIT']),
        KC.TD(ck['YOUTUBE'], simple_key_sequence([KC.LCTRL, KC.LCMD, KC.K])),

        # Encoder 1: Turn up/down 
        KC.AUDIO_VOL_DOWN,
        KC.AUDIO_VOL_UP,
    ],
    [
        # Layer 1 (HAZEL-MODE)
        # Encoder 1 & 2 button push
        KC.AUDIO_MUTE,
        simple_key_sequence([KC.RGB_TOG, KC.LCTRL, KC.LCMD, KC.K]),

        # Row 1
        ck['GIMKIT'],
        ck['TAYLOR'],
        ck['MONKEY'],
        KC.HT(
            DEACTIVATE_HAZEL_MODE,  # Tap action
            DEACTIVATE_HAZEL_MODE,  # Hold action to activate HAZEL-MODE layer permanently
            prefer_hold=True
        ),

        # Row 2
        ck['FART'], ck['FART'], ck['FART'], ck['FART'],

        # Row 3
        ck['FART'], ck['FART'], ck['FART'], ck['FART'],

        # Encoder 1: Turn up/down 
        KC.AUDIO_VOL_DOWN,
        KC.AUDIO_VOL_UP,
    ]
]

def debug_key_resolution(key):
    print(f"Resolving key: {key}")
    print(f"Key code: {key.code}")
    print(f"Current active layers: {keyboard.active_layers}")
    return key

keyboard.key_resolution_override = debug_key_resolution

if __name__ == '__main__': 
    while True:
        keyboard.go(hid_type=HIDModes.USB)
        print(f'Current active layers: {keyboard.active_layers}')
