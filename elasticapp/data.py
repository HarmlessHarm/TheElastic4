import csv, os, textwrap, re

_all_questions = None



class Question(object):
	"""

	"""
	def __init__(self, questionId, date, userId, categoryId, question, description):
		super(Question, self).__init__()
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
		
class Answer(object):
	"""

	"""
	def __init__(self, answerId, date, userId, questionId, answer, 
							thumbsDown, thumbsUp, isBestAnswer):
		super(Answer, self).__init__()
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
		

def get_questions():

	global _all_questions

	if _all_questions is None:
		_all_questions = []

		with open('../data/questions.csv') as qf:
			questionReader = csv.reader(qf, delimiter=',')
			count = 0
			for i, row in enumerate(questionReader):
				if (len(row) > 6):
					print(row[0], len(row), row[6:])
				if i > 1000: break
			# print(count)


def preprocess_questions():
	import pprint
	tm40 = 4175
	with open('../data/questions.csv') as file:
		all_lines = file.read(tm40).replace('\n', ' ')
		# print(all_lines)
		rId = '([0-9]+)'
		rDate = '([0-9]{4}\-[0-9]{2}\-[0-9]{2}\s[0-9]{2}\:[0-9]{2}\:[0-9]{2})'
		r1 = '{}\,\"{}\"\,{}\,{}\,'.format(rId, rDate, rId, rId)
		r2 = r1 + '(.*?)' + '(?=' + r1 + ')'
		result = re.findall(r1, all_lines)
		pprint.pprint((len(result), result))


# get_questions()
preprocess_questions()