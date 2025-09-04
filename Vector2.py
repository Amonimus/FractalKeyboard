class Vector2:
	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y

	def __str__(self):
		return f"{self.get()}"

	def set(self, coor: tuple) -> None:
		self.x = coor[0]
		self.y = coor[1]

	def get(self) -> tuple:
		return self.x, self.y

	def __add__(self, val: float) -> 'Vector2':
		return Vector2(self.x + val, self.y + val)

	def __sub__(self, val: float) -> 'Vector2':
		return Vector2(self.x - val, self.y - val)
