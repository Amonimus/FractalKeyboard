import time
from typing import TYPE_CHECKING

from Vector2 import Vector2
from consts import col_YELLOW, note_DO, const_NOTE_DISTANCE, const_VOLUME, const_NOTE_DELAY

if TYPE_CHECKING:
	from FractalKeyboard import FractalKeyboard


class Key:
	def __init__(self, keyboard: 'FractalKeyboard', coord: list, col: tuple, rect: tuple):
		self.keyboard = keyboard
		self.coord: list = coord.copy()  # Multidimensional coordinates list. The list is mutable, so it needs to be copied
		self.col: tuple = col  # Key color
		self.col_init: tuple = self.col  # Initial key color
		self.rect: tuple = rect  # Screen position (x, y, height, width)

	def is_mouse_in_rect(self, mouse_pos: Vector2) -> bool:
		"""Checks if mouse is colliding with own mask"""
		vert: bool = self.rect[0] < self.keyboard.zoom_pos.x + mouse_pos.x < self.rect[0] + self.rect[2]
		hor: bool = self.rect[1] < self.keyboard.zoom_pos.y + mouse_pos.y < self.rect[1] + self.rect[3]
		return vert and hor

	def on_hover(self, mouse_pos: Vector2) -> None:
		"""Action if the key is hovered by the mouse"""
		if self.is_mouse_in_rect(mouse_pos):
			# highlight
			self.col = col_YELLOW
		else:
			# remove highlight
			self.col = self.col_init

	def on_click(self, mouse_pos: Vector2) -> None:
		"""Action if the key is clicked on"""
		if self.is_mouse_in_rect(mouse_pos):
			self.play_key()

	def play_note(self, shift: int) -> None:
		"""Play MIDI sound"""
		note: int = note_DO + (const_NOTE_DISTANCE * shift)  # MIDI pitch to play
		self.keyboard.midi.note_on(note, const_VOLUME)
		time.sleep(const_NOTE_DELAY)
		self.keyboard.midi.note_off(note, const_VOLUME)

	def play_key(self):
		print("Play:", self.coord)
		for coord in self.coord:
			self.play_note(coord)
