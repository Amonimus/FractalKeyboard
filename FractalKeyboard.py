from typing import List

import pygame
from pygame import midi

from Key import Key
from Vector2 import Vector2
from consts import const_BACKGROUND_COL, const_GRID_COL, const_KEY_WIDTH, col_WHITE


class FractalKeyboard:

	def __init__(self, key_list: list, dimensions: int, screen_size: int):
		# Pygame setup
		print("Init")
		pygame.init()
		pygame.display.set_caption("Fractal Keyboard")
		self.screen_size: int = screen_size
		self.screen_dims: Vector2 = Vector2(self.screen_size, self.screen_size)
		print("Scren size:", self.screen_dims)
		self.screen: pygame.Surface = pygame.display.set_mode(self.screen_dims.get())

		self.mouse_mos: Vector2 = Vector2(0, 0)
		pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

		# MIDI interface setup
		pygame.midi.init()
		self.midi: pygame.midi.Output = pygame.midi.Output(0)
		self.midi.set_instrument(1)  # Grand piano

		# Set up a list of keys and colors in each direction
		self.key_list: list = key_list
		print("Keys:", self.key_list)
		self.keylist_size: int = len(self.key_list)
		self.dimensions: int = dimensions
		print("Dimensions:", self.dimensions)
		self.keys: List[Key] = []

		self.background_col: tuple = const_BACKGROUND_COL
		self.grid_col: tuple = const_GRID_COL

		self.max_image_size: int = const_KEY_WIDTH * (self.keylist_size ** ((self.dimensions + 1) // 2))
		self.image_dims: Vector2 = Vector2(self.max_image_size, self.max_image_size)
		print("Image size:", self.image_dims)
		self.surf: pygame.Surface = pygame.Surface(self.image_dims.get())

		self.zoom_pos: Vector2 = Vector2(0, 0)
		self.zoom_step: float = self.max_image_size / ((self.dimensions + 1) * 2)
		self.zoom_dims: Vector2 = Vector2(self.image_dims.x, self.image_dims.y)
		self.zoom_scale: int = 1

		self.recursive_setup(self.dimensions)

		self.running: bool = True  # A flag to quit the game loop
		self.run()

	def run(self) -> None:
		"""MAIN gameloop"""
		print("Start")
		try:
			while self.running:
				self.step()
				self.draw()
		except KeyboardInterrupt:
			pass
		print("End")

	def step(self) -> None:
		"""On each logic frame, handle events"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.MOUSEMOTION:
				self.hover(event.pos)
			elif event.type == pygame.MOUSEWHEEL:
				self.zoom(event.y)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == pygame.BUTTON_LEFT:
					self.click(event.pos)

	def draw(self) -> None:
		"""On each display frame, handle graphics"""
		self.screen.fill(self.background_col)
		self.draw_keys()
		self.draw_grid()
		self.fit_screen()
		pygame.display.flip()

	def click(self, pos: tuple) -> None:
		"""Makes all keys react to the click event"""
		self.mouse_mos.set(pos)
		rel_pos: Vector2 = self.get_mouse_relative()
		for key in self.keys:
			key.on_click(rel_pos)

	def hover(self, pos: tuple) -> None:
		"""Makes all keys react to the hover event"""
		self.mouse_mos.set(pos)
		rel_pos: Vector2 = self.get_mouse_relative()
		for key in self.keys:
			key.on_hover(rel_pos)

	def get_mouse_relative(self) -> Vector2:
		"""Returns mouse position in accordance to inner image"""
		surface_scale_x: float = self.zoom_dims.x / self.screen_dims.x
		surface_scale_y: float = self.zoom_dims.y / self.screen_dims.y
		rel_pos: Vector2 = Vector2(self.mouse_mos.x * surface_scale_x, self.mouse_mos.y * surface_scale_y)
		return rel_pos

	def zoom(self, direction: int) -> None:
		"""Handles zoom event"""
		# Checks from (0,0) to (1, 1) where the mouse is
		rel_pos_percent: Vector2 = Vector2(self.mouse_mos.x / self.screen_dims.x, self.mouse_mos.y / self.screen_dims.y)
		# print(rel_pos_percent)
		if direction >= 1:
			# Zoom in
			# Checks so the intended screen is not out of bounds
			check_zoom_size: Vector2 = self.zoom_dims - self.zoom_step
			if check_zoom_size.x > 0 and check_zoom_size.y > 0:
				self.zoom_dims = check_zoom_size
				self.zoom_pos.x += self.zoom_step * rel_pos_percent.x
				self.zoom_pos.y += self.zoom_step * rel_pos_percent.y
		elif direction <= -1:
			# Zoom out
			# Checks so the intended screen is not out of bounds
			check_zoom_size: Vector2 = self.zoom_dims + self.zoom_step
			if check_zoom_size.x <= self.image_dims.x and check_zoom_size.y <= self.image_dims.y:
				self.zoom_dims = check_zoom_size
				self.zoom_pos.x -= self.zoom_step * rel_pos_percent.x
				self.zoom_pos.y -= self.zoom_step * rel_pos_percent.y

		# Size correction if got out of bounds anyway
		if self.zoom_pos.x + self.zoom_dims.x > self.image_dims.x:
			self.zoom_pos.x = self.image_dims.x - self.zoom_dims.x
		if self.zoom_pos.y + self.zoom_dims.y > self.image_dims.y:
			self.zoom_pos.y = self.image_dims.y - self.zoom_dims.y

		# Position correction if got out of bounds anyway
		if self.zoom_pos.x < 0:
			self.zoom_pos.x = 0
		if self.zoom_pos.y < 0:
			self.zoom_pos.y = 0
		if self.zoom_pos.x > self.max_image_size:
			self.zoom_pos.x = self.max_image_size
		if self.zoom_pos.y > self.max_image_size:
			self.zoom_pos.y = self.max_image_size

	# print("Zoom position", self.zoom_pos)

	def fit_screen(self) -> None:
		"""Stretches the drawing surface to fit the window"""
		crop_rect: tuple = (
			self.zoom_pos.x,
			self.zoom_pos.y,
			self.zoom_dims.x,
			self.zoom_dims.y
		)
		crop_size: tuple = (
			self.zoom_pos.x,
			self.zoom_pos.y,
			self.zoom_pos.x + self.zoom_dims.x,
			self.zoom_pos.y + self.zoom_dims.y
		)
		# print("Crop:", crop_size)
		surf_zoomed: pygame.Surface = self.surf.subsurface(crop_rect)
		surf_scaled: pygame.Surface = pygame.transform.scale(surf_zoomed, self.screen_dims.get())
		self.screen.blit(surf_scaled, (0, 0))

	def make_row(self, coords: list, colors: list) -> None:
		"""Build a key for each dimension"""
		if len(colors) == 0:
			# This can only happen if the dimensions = 0
			colors = [self.key_list[0]]
		black_count: int = colors.count(1)
		shade: float = black_count / len(colors)
		col: tuple = tuple(c * shade for c in col_WHITE)

		x_depth: int = (len(coords) + 1) // 2
		y_depth: int = len(coords) // 2

		x: int = 0
		for i in range(1, x_depth + 1):
			x += coords[(i - 1) * 2] * (self.max_image_size / (self.keylist_size ** (x_depth - (i - 1))))
		y: int = 0
		for i in range(1, y_depth + 1):
			y += coords[(i * 2) - 1] * (self.max_image_size / (self.keylist_size ** (y_depth - (i - 1))))

		width: float = self.max_image_size / (self.keylist_size ** x_depth)
		height: float = self.max_image_size / (self.keylist_size ** y_depth)

		rect: tuple = (x, y, width, height)

		if len(coords) == 0:
			coords = [0]
		key: Key = Key(self, coords, col, rect)
		self.keys.append(key)

	def recursive_setup(self, depth: int, coords=None, colors=None):
		"""Iterates through they key list dimension times, building a dimension-D array"""
		if coords is None:
			coords = []
		if colors is None:
			colors = []
		if depth > 0:
			for index, value in enumerate(self.key_list):
				coords.insert(0, index)
				colors.append(value)
				self.recursive_setup(depth - 1, coords, colors)
				coords.pop(0)
				colors.pop()
		else:
			self.make_row(coords, colors)

	def draw_keys(self) -> None:
		"""Display the key rectangles"""
		for key in self.keys:
			pygame.draw.rect(self.surf, key.col, key.rect)

	def draw_grid(self) -> None:
		"""Draws lines across the screen"""
		depth: int = 0
		x_min: int = 1
		y_min: int = 2
		while depth < self.dimensions + 1:
			# print("Dim:", depth)
			if depth % 2 != 0:
				# Vertical lines
				x_depth: int = (depth + x_min) // 2
				# print("X depth:", x_depth)
				if x_depth > x_min:
					grid_size: float = self.image_dims.x / (self.keylist_size ** (x_depth - x_min))
					# print("X Grid size:", grid_size)
					width: int = ((self.dimensions + 1) // 2) - x_depth + x_min + 1
					# print("X width:", width)
					x: int = 0
					while x <= self.image_dims.x:
						pygame.draw.line(self.surf, self.grid_col, (x, 0), (x, self.image_dims.x), width)
						x += grid_size
			if depth % 2 == 0:
				# Horizontal lines
				y_depth: int = (depth + y_min) // 2
				# print("Y depth:", y_depth)
				if y_depth > y_min:
					grid_size: float = self.image_dims.y / (self.keylist_size ** (y_depth - y_min))
					# print("Y Grid size:", grid_size)
					width: int = (self.dimensions // 2) - y_depth + y_min + 1
					# print("Y width:", width)
					y: int = 0
					while y <= self.image_dims.y:
						pygame.draw.line(self.surf, self.grid_col, (0, y), (self.image_dims.y, y), width)
						y += grid_size
			depth += 1
