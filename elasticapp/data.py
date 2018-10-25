import os, textwrap, re, csv

_all_questions = None
_all_answers = None
_all_users = None
_all_categories = None

class QuestionData(object):
	"""

	"""
	def __init__(self, questionId, date, userId, categoryId, question, description):
		self.questionId = questionId
		self.date = date
		self.userId = userId
		self.categoryId = categoryId
		self.question = question
		self.description = description

	def __str__(self):
		return textwrap.dedent("""\
			questionId : {}
			date : {}
			userId : {}
			categoryId : {}
			question : {}
			description : {}
			""").format(self.questionId, self.date, self.userId, self.categoryId, 
									self.question, self.description)
		
class AnswerData(object):
	"""

	"""
	def __init__(self, answerId, date, userId, questionId, answer, 
							thumbsDown, thumbsUp, isBestAnswer):
		self.answerId = answerId
		self.date = date
		self.userId = userId
		self.questionId = questionId
		self.answer = answer
		self.thumbsDown = thumbsDown
		self.thumbsUp = thumbsUp
		self.isBestAnswer = isBestAnswer


	def __str__(self):
		return textwrap.dedent("""\
			answerId : {}
			date : {}
			userId : {}
			questionId : {}
			answer : {}
			thumbsDown : {}
			thumbsUp : {}
			isBestAnswer : {}
			""").format(self.answerId, self.date, self.userId, self.questionId, 
									self.answer, self.thumbsDown, self.thumbsUp, self.isBestAnswer)


class CategoryData(object):
	"""docstring for CategoryData"""
	def __init__(self, categoryId, parentId, name):
		self.categoryId = categoryId
		self.parentId = parentId
		self.name = name
		
	def __str__(self):
		return textwrap.dedent("""\
			categoryId : {}
			parentId : {}
			name : {}
			""").format(self.categoryId, self.parentId, self.name)


class UserData(object):
	"""docstring for UserData"""
	def __init__(self, userId, date, expertise, bestAnswers):
		self.userId = userId
		self.date = date
		self.expertise = expertise
		self.bestAnswers = bestAnswers

	def __str__(self):
		return textwrap.dedent("""\
			userId : {}
			date : {}
			expertise : {}
			bestAnswers : {}
			""").format(self.userId, self.date, self.expertise, self.bestAnswers)
		
def all_questions(test=False):
	"""
	Returns a list with all questions parsed from ../data/questions.csv
	"""
	global _all_questions

	if _all_questions is None:
		print("Loading in questions data file")
		
		_all_questions = []
		file_name = 'data/questions.csv'
		if test: file_name = 'data/q1000.csv'

		parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		file_path = os.path.join(parent_dir, file_name)
		with open(file_path) as file:
			all_lines = file.read().replace('\n', ' ')
			
		rId = r'[0-9]+'
		rDate = r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}'
		rTime = r'[0-9]{2}\:[0-9]{2}\:[0-9]{2}'
		r = r'({}\,\"{}\s{}\"\,{}\,{})\,'.format(rId, rDate, rTime, rId, rId)
		results = re.split(r, all_lines)

		for i, (info, text) in enumerate(zip(*[iter(results[1:])]*2)):
			if i % int(len(results)/2 / 50)== 0:
				print('.', end="", flush=True)
			rT = r'\"(.*?)\"'
			rN = r'\\N'
			data = info.split(',') + list(re.findall(rT+r','+rT+r'|'+rN, text)[0])
			q_data = QuestionData(*data)
			_all_questions.append(q_data)

		print("\nLoaded {} questions".format(len(_all_questions)))
		return _all_questions

def all_answers(test=False):
	"""
	Returns a list with all answers parsed from ../data/answers.csv
	"""
	global _all_answers

	if _all_answers is None:
		print("Loading in answers data file")

		_all_answers = []
		file_name = 'data/answers.csv'
		if test: file_name = 'data/a1000.csv'

		parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		file_path = os.path.join(parent_dir, file_name)
		
		with open(file_path) as file:
			all_lines = file.read().replace('\n', ' ')
			
		rN = r'([0-9]+)'
		rDate = r'([0-9]{4}\-[0-9]{2}\-[0-9]{2}\s[0-9]{2}\:[0-9]{2}\:[0-9]{2})'
		rT = r'(.*?)'
		r = r'{}\,\"{}\"\,{}\,{}\,\"{}\"\,{}\,{}\,{}'.format(rN, rDate, rN, rN, rT, rN, rN, rN)
		results = re.findall(r, all_lines)
		ids = []
		for i, result in enumerate(results):
			if i % int(len(results)/ 50)== 0:
				print('.', end="", flush=True)
			a_data = AnswerData(*result)
			int(a_data.answerId)
			_all_answers.append(a_data)

		print("\nLoaded {} answers".format(len(_all_answers)))
		return _all_answers


def all_users():
	"""
	Returns a list with all answers parsed from ../data/answers.csv
	"""
	global _all_users

	if _all_users is None:
		_all_users = []
		file_name = 'data/users.csv'

		parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		file_path = os.path.join(parent_dir, file_name)
		
		with open(file_path) as file:
			all_lines = file.read().replace('\n', ' ')
			
		rN = r'([0-9]+)'
		rDate = r'([0-9]{4}\-[0-9]{2}\-[0-9]{2}\s[0-9]{2}\:[0-9]{2}\:[0-9]{2})'
		rT = r'(.*?)'
		r = r'{}\,\"{}\"\,{}\,{}'.format(rN, rDate, rT, rN)
		results = re.findall(r, all_lines)

		for result in results:
			u_data = UserData(*result)
			_all_users.append(u_data)

		print("Loaded {} users".format(len(_all_users)))
		return _all_users


def all_categories():
	global _all_categories

	if _all_categories is None:
		_all_categories = []

		file_name = 'data/categories.csv'

		parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		file_path = os.path.join(parent_dir, file_name)
		
		with open(file_path) as file:
			for line in csv.reader(file):
				c_data = CategoryData(*line)
				_all_categories.append(c_data)

		print("Loaded {} categories".format(len(_all_categories)))
		return _all_categories