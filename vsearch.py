def search4vowels (phrase: str) -> set:
	"""выводит гласные, найденные в коде"""
	vowels = set('aeiou')
	return vowels.intersection(set(phrase))

def search4letters(phrase: str, letters: str='aieou') -> set:
	return set(letters).intersection(set(phrase))