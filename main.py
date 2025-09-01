import time
from typing import List

import pygame
import pygame.midi


class Key:
	def __init__(self, keyboard, pos: list, col: tuple, rect: tuple):
		self.keyboard = keyboard
		self.pos: list = pos.copy()
		self.col: tuple = col
		self.col_init: tuple = self.col
		self.rect: tuple = rect

	def point_in_rect(self, mouse_pos: tuple) -> bool:
		vert = self.rect[0] < mouse_pos[0] < self.rect[0] + self.rect[2]
		hor = self.rect[1] < mouse_pos[1] < self.rect[1] + self.rect[3]
		return vert and hor

	def on_hover(self, mouse_pos: tuple):
		# if the mouse if over a key
		if self.point_in_rect(mouse_pos):
			# highlight
			self.col = (255, 255, 0)
		else:
			self.col = self.col_init

	def on_click(self, mouse_pos: tuple):
		# if clicked
		if self.point_in_rect(mouse_pos):
			self.play_key()

	def play_note(self, shift):
		do = 36
		self.keyboard.midi.note_on(do + (2 * shift), 127)
		time.sleep(0.15)
		self.keyboard.midi.note_off(do + (2 * shift), 127)

	def play_key(self):
		for coord in self.pos:
			self.play_note(coord)


class FractalKeyboard:

	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Fractal Keyboard")
		pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

		pygame.midi.init()
		self.midi = pygame.midi.Output(0)
		self.midi.set_instrument(1)  # Grand piano

		self.screen_size: int = 600
		win_size: tuple = (self.screen_size, self.screen_size)
		self.surface: pygame.Surface = pygame.display.set_mode(win_size)

		self.key_list = [0, 1, 0, 1, 0, 0, 1, 0]
		# self.key_list = [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]
		self.dimensions: int = 4

		self.running: bool = True

		self.keys: List[Key] = []

		self.recursive_setup(self.dimensions)
		self.run()

	def make_row(self, coords, colors):
		if all(v == 1 for v in colors):
			col = (0, 0, 0)
		elif all(v == 0 for v in colors):
			col = (255, 255, 255)
		else:
			col = (127, 127, 127)

		list_size = len(self.key_list)
		grid_size: float = self.screen_size / list_size

		if len(coords) == 0:
			x = 0
		elif len(coords) == 1 or len(coords) == 2:
			x = coords[-1] * grid_size
		elif len(coords) == 3 or len(coords) == 4:
			x = (coords[-3] * grid_size) + (coords[-1] * (grid_size / list_size))

		if len(coords) == 0 or len(coords) == 1:
			y = 0
		elif len(coords) == 2 or len(coords) == 3:
			y = coords[-2] * grid_size
		elif len(coords) == 4:
			y = (coords[-4] * grid_size) + (coords[-2] * (grid_size / list_size))

		if len(coords) == 0:
			width = self.screen_size
		elif len(coords) == 1 or len(coords) == 2:
			width = grid_size
		elif len(coords) == 3 or len(coords) == 4:
			width = grid_size / list_size

		if len(coords) == 0 or len(coords) == 1:
			height = self.screen_size
		elif len(coords) == 2 or len(coords) == 3:
			height = grid_size
		elif len(coords) == 4:
			height = grid_size / list_size

		rect = (x, y, width + 1, height + 1)

		key: Key = Key(self, coords, col, rect)
		self.keys.append(key)

	def recursive_setup(self, times, parent_indexes=None, parent_values=None):
		if parent_indexes is None:
			parent_indexes = []
		if parent_values is None:
			parent_values = []
		if times > 0:
			for index, value in enumerate(self.key_list):
				parent_indexes.append(index)
				parent_values.append(value)
				self.recursive_setup(times - 1, parent_indexes, parent_values)
				parent_indexes.pop()
				parent_values.pop()
		else:
			self.make_row(parent_indexes, parent_values)

	def step(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.MOUSEMOTION:
				self.hover(event.pos)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == pygame.BUTTON_LEFT:
					self.input(event.pos)

	def draw(self):
		self.surface.fill((255, 0, 0))
		for key in self.keys:
			pygame.draw.rect(self.surface, key.col, key.rect)

			pygame.draw.line(
				self.surface,
				(0, 0, 255),
				(key.rect[0], key.rect[1]),
				(key.rect[0] + key.rect[2], key.rect[1])
			)
			pygame.draw.line(
				self.surface,
				(0, 0, 255),
				(key.rect[0], key.rect[1]),
				(key.rect[0], key.rect[1] + key.rect[3]),
				2
			)

	def hover(self, pos):
		for key in self.keys:
			key.on_hover(pos)

	def input(self, pos):
		for key in self.keys:
			key.on_click(pos)

	def run(self):
		print("Start")
		try:
			while self.running:
				self.step()
				self.draw()
				pygame.display.flip()
		except KeyboardInterrupt:
			pass
		print("End")


def main():
	FractalKeyboard()


if __name__ == '__main__':
	main()
