from FractalKeyboard import FractalKeyboard


def main():
	key_list: list = [0, 1, 0, 1, 0, 0, 1, 0, -1]   # Colors of a row
	FractalKeyboard(key_list, 2, 800)


if __name__ == '__main__':
	main()
