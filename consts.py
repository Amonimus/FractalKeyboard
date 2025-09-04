# Consts
col_BLACK: tuple = (0, 0, 0)
col_GRAY: tuple = (127, 127, 127)
col_WHITE: tuple = (255, 255, 255)
col_RED: tuple = (255, 0, 0)
col_BLUE: tuple = (0, 0, 255)
col_YELLOW: tuple = (255, 255, 0)
note_DO: int = 36  # The starting MIDI sound pitch
# Quick parameters
const_NOTE_DISTANCE: int = 4  # The step between sound keys, the standard is 2
const_VOLUME: int = 127  # MIDI velocity, 127 is max
const_NOTE_DELAY: float = 0.15  # The length of a key press
const_KEY_WIDTH: int = 10  # Minimum size of a key in pixels
const_BACKGROUND_COL: tuple = col_RED  # Default color of the surface
const_GRID_COL: tuple = col_BLUE  # Color for the grid
