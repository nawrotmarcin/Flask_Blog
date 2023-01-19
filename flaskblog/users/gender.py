import requests


class PredictGender:

	def __init__(self, name):
		self.name = name

	def is_male(self):
		respond = requests.get(url=f'https://api.genderize.io?name={self.name}')
		gender = respond.json()['gender']
		if gender == 'male':
			return True
		else:
			return False

