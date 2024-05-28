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
    # rgb_encoder = RGBEncoder(
    #     pin_a=rgb_encoder_a,
    #     pin_b=rgb_encoder_b,
    # )
