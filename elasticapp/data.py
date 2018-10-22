import csv, os, textwrap, re

_all_questions = None



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

def get_questions():

	parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	file_path = os.path.join(parent_dir,'data/q1000.csv')
	
	with open(file_path) as file:
		all_lines = file.read().replace('\n', ' ')
		
		rId = r'[0-9]+'
		rDate = r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}'
		rTime = r'[0-9]{2}\:[0-9]{2}\:[0-9]{2}'
		r = r'({}\,\"{}\s{}\"\,{}\,{})\,'.format(rId, rDate, rTime, rId, rId)
		results = re.split(r, all_lines)

		for info, text in zip(*[iter(results[1:])]*2):

			rT = r'\"(.*?)\"'
			rN = r'\\N'
			data = info.split(',') + list(re.findall(rT+r','+rT+r'|'+rN, text)[0])
			q_data = QuestionData(*data)

			print(q_data.question)


def parse_string(ugly_str):
	# print(ugly_str)
	import string
	# translate_table = str.maketrans(dict.fromkeys(['\\']))
	# print(translate_table)

	new_str = ugly_str.strip('\"')
	new_str = new_str.replace('\\\"','\"')
	new_str = new_str.replace('\\\\','\\')
	r = re.findall('\\{2}', ugly_str)
	if len(r) > 0:
		print(ugly_str.find(''))
		print("{}\n{}\n{}\n\n".format(ugly_str, new_str, r))

	return ugly_str


get_questions()