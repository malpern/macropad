import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.scanners.keypad import MatrixScanner
from kmk.modules.encoder import GPIOEncoder
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
            GPIOEncoder(
                pin_a=self.volume_encoder_a,
                pin_b=self.volume_encoder_b,
            ),
            GPIOEncoder(
                pin_a=self.rgb_encoder_a,
                pin_b=self.rgb_encoder_b,
            )
        ]

    row_pins = (board.D7, board.D8, board.D9)
    col_pins = (board.D3, board.D4, board.D5, board.D6)
    diode_orientation = DiodeOrientation.COL2ROW
    rgb_pixel_pin = board.D10
    rgb_num_pixel = 4
    volume_encoder_a = board.A1
    volume_encoder_b = board.A2
    rgb_encoder_a = board.SCK
    rgb_encoder_b = board.MISO
