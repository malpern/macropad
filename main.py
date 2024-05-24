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
        # Row 1 First two are the push button of the encoder. Then top two buttons in the first row from the top.
        KC.AUDIO_MUTE, KC.RGB_TOG, ck['ARCH'], ck['EVERNOTE'],
        # Row 2
        ck['CALANDER'], ck['CHATGPT'], ck['CURSOR'], ck['DOWNLOADS'],
        # Row 3
        ck['MESSAGES'], ck['WHATSAPP'], ck['FIGMA'], ck['TECHMEME'],
        # Row 4
        ck['TWITTER'], ck['YOUTUBE'], KC.AUDIO_VOL_DOWN, KC.AUDIO_VOL_UP
    ],
    # Layer 1
    [
        # Row 1 First two are the push button of the encoder. Then top two buttons in the first row from the top.
        KC.AUDIO_MUTE, KC.RGB_TOG, KC.KP_7, KC.KP_8,
        # Row 2
        KC.KP_9, KC.KP_ASTERISK, KC.KP_4, KC.KP_5,
        # Row 3
        KC.KP_6, KC.KP_MINUS, KC.KP_1, KC.KP_2,
        # Row 4
        KC.KP_3, KC.KP_PLUS, KC.AUDIO_VOL_DOWN, KC.AUDIO_VOL_UP
    ],
    # Layer 2
    [
       # Row 1 First two are the push button of the encoder. Then top two buttons in the first row from the top.
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 2
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 3
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 4
        KC.NO, KC.NO, KC.NO, KC.NO
    ],
    # Layer 3
    [
        # Row 1 First two are the push button of the encoder. Then top two buttons in the first row from the top.
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 2
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 3
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 4
        KC.NO, KC.NO, KC.NO, KC.NO
    ],
    # Layer 4
    [
        # Row 1 First two are the push button of the encoder. Then top two buttons in the first row from the top.
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 2
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 3
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 4
        KC.NO, KC.NO, KC.NO, KC.NO
    ],
    # Layer 5
    [
        # Row 1 First two are the push button of the encoder. Then top two buttons in the first row from the top.
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 2
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 3
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 4
        KC.NO, KC.NO, KC.NO, KC.NO
    ],
    # Layer 6
    [
        # Row 1 First two are the push button of the encoder. Then top two buttons in the first row from the top.
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 2
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 3
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 4
        KC.NO, KC.NO, KC.NO, KC.NO
    ],
    # Layer 7
    [
        # Row 1 First two are the push button of the encoder. Then top two buttons in the first row from the top.
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 2
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 3
        KC.NO, KC.NO, KC.NO, KC.NO,
        # Row 4
        KC.NO, KC.NO, KC.NO, KC.NO
    ]
]
if __name__ == '__main__': 
    keyboard.go(hid_type=HIDModes.USB)
    keyboard.extensions.append(StringyKeymaps())
