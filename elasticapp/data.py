import csv, os, textwrap, re

_all_questions = None
_all_answers = None



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

def all_questions(test=True):
	"""
	Returns a list with all questions parsed from ../data/questions.csv
	"""
	global _all_questions

	if _all_questions is None:
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

			count = 0
			for info, text in zip(*[iter(results[1:])]*2):

				rT = r'\"(.*?)\"'
				rN = r'\\N'
				data = info.split(',') + list(re.findall(rT+r','+rT+r'|'+rN, text)[0])
				q_data = QuestionData(*data)
				_all_questions.append(q_data)
				count += 1
			print("Loaded {} questions".format(count))

def all_answers(test=True):
	"""
	Returns a list with all questions parsed from ../data/questions.csv
	"""
	global _all_answers

	if _all_answers is None:
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
			r = r'{}\,\"{}\"\,{}\,{}\,{}\,{}\,{}\,{}'.format(rN, rDate, rN, rN, rT, rN, rN, rN)
			results = re.findall(r, all_lines)

			count = 0
			for result in results:
				a_data = AnswerData(*result)
				_all_answers.append(a_data)
				count += 1

			print("Loaded {} answers".format(count))

all_questions(True)
all_answers(True)