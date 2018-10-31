try:
	with open('test.txt') as file:
		for chore in file:
			print(chore)
except FileNotFoundError:
	print('the data is missing')
except PermissionError:
	print('this is not allowed')