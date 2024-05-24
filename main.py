from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.hid import HIDModes
from kmk.handlers.sequences import send_string
import supervisor
import json

# Load custom keycodes into a dictionary
ck = {}
with open('custom-keycodes.json', 'r') as f:
    custom_keycodes_list = json.load(f)
    for kc in custom_keycodes_list:
        ck[kc['display']] = eval(kc['code'])  # Use eval to convert string to executable code

keyboard = KMKKeyboard()
modtap = ModTap()
layers_ext = Layers()
keyboard.modules.append(layers_ext)
keyboard.modules.append(modtap)
keyboard.debug_enabled = True
from kmk.extensions.media_keys import MediaKeys
from kmk.handlers.sequences import simple_key_sequence
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.RGB import RGB
import microcontroller

rgb = RGB(
    pixel_pin=keyboard.rgb_pixel_pin, 
    num_pixels=keyboard.rgb_num_pixel, 
    hue_default=microcontroller.nvm[0]
)

def on_move_do(state):
    if state is not None and state['direction'] == -1:
        rgb.decrease_hue()
    else:
        rgb.increase_hue()
    microcontroller.nvm[0] = rgb.hue

encoder_handler = EncoderHandler()
encoder_handler.pins = ((keyboard.rgb_encoder_a, keyboard.rgb_encoder_b, None, False),)
encoder_handler.on_move_do = lambda x, y, state: on_move_do(state)

encoder_handler.map =   [ ((KC.RGB_HUD, KC.RGB_HUI, KC.RGB_TOG),), ]
keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(rgb)
keyboard.extensions.append(encoder_handler)
keyboard.modules = [layers_ext, modtap]

keyboard.keymap = [
    # Layer 0
    [
        # Encoder press buttons
        KC.AUDIO_MUTE, KC.RGB_TOG,
        # Row 1
        ck['ARCH'], ck['EVERNOTE'], ck['CALANDER'], ck['CHATGPT'],
        # Row 2
        ck['CURSOR'], ck['DOWNLOADS'], ck['MESSAGES'], ck['WHATSAPP'],
        # Row 3
        ck['FIGMA'], ck['TECHMEME'], ck['TWITTER'], ck['YOUTUBE'],
        # Encoder turn options
        KC.AUDIO_VOL_DOWN, KC.AUDIO_VOL_UP
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
    # Layer 2
    [
        # Encoder press buttons
        KC.NO, KC.NO,
        # Row 1
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 2
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 3
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Encoder turn options
        KC.NO, KC.NO
    ],
    # Layer 3
    [
        # Encoder press buttons
        KC.NO, KC.NO,
        # Row 1
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 2
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 3
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Encoder turn options
        KC.NO, KC.NO
    ],
    # Layer 4
    [
        # Encoder press buttons
        KC.NO, KC.NO,
        # Row 1
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 2
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 3
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Encoder turn options
        KC.NO, KC.NO
    ],
    # Layer 5
    [
        # Encoder press buttons
        KC.NO, KC.NO,
        # Row 1
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 2
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 3
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Encoder turn options
        KC.NO, KC.NO
    ],
    # Layer 6
    [
        # Encoder press buttons
        KC.NO, KC.NO,
        # Row 1
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 2
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 3
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Encoder turn options
        KC.NO, KC.NO
    ],
    # Layer 7
    [
        # Encoder press buttons
        KC.NO, KC.NO,
        # Row 1
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 2
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 3
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Encoder turn options
        KC.NO, KC.NO
    ]
]

if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.USB)
    keyboard.extensions.append(StringyKeymaps())
