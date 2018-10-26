from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from typing import List

from elasticapp.constants import *

HEADERS = {'content-type': 'application/json'}

class QuestionResult(object):
	"""docstring for QuestionResult"""
	def __init__(self, questionId, date, userId, categoryId, question, description):
		self.questionId = questionId
		self.date = date
		self.userId = userId
		self.categoryId = categoryId
		self.question = question
		self.description = description
		self.answers = getAnswers(questionId)

	def from_doc(doc) -> 'QuestionResult':
		return QuestionResult(
				questionId = doc.meta.id,
				date = doc.date,
				userId = doc.userId,
				categoryId = doc.categoryId,
				question = doc.question,
				description = doc.description,
			)

class AnswerResult(object):
	"""docstring for QuestionResult"""
	def __init__(self, answer, userId, questionId, thumbsUp, thumbsDown, isBestAnswer):
		self.answer = answer
		self.answer = doc.answer,
		self.userId = doc.userId,
		self.questionId = doc.questionId,
		self.thumbsUp = doc.thumbsUp,
		self.thumbsDown = doc.thumbsDown,
		self.isBestAnswer = doc.isBestAnswer,

	def from_doc(doc) -> 'AnswerResult':

		return AnswerResult(
				answerId = doc.meta.id,
				answer = doc.answer,
				userId = doc.userId,
				questionId = doc.questionId,
				thumbsUp = doc.thumbsUp,
				thumbsDown = doc.thumbsDown,
				isBestAnswer = doc.isBestAnswer,
			)

def getQuestions(term:str) -> List[QuestionResult]:
	client = Elasticsearch()

	client.transport.connection_pool.connection.headers.update(HEADERS)
	
	fuzziness = 0
	if len(term.split(' ')) > 1:
		fuzziness = 'AUTO'

	s = Search(using=client, index=Q_INDEX, doc_type=Q_DOC_T)
	search = {
		'multi_match': {
			'query': term,
			'type': 'best_fields',
			"fields": [ "question.dutch_analyzed^3", "description.dutch_analyzed" ],
			'tie_breaker': 0.7,
			'fuzziness': fuzziness,
		}
	}

	docs = s.query(search)[:100].execute()

	return [QuestionResult.from_doc(d) for d in docs]

def getAdvanced(query) -> List[QuestionResult]:

	client = Elasticsearch()
	client.transport.connection_pool.connection.headers.update(HEADERS)
	s = Search(using=client, index=Q_INDEX, doc_type=Q_DOC_T)

	search = {
		'query_string': {
			'query': query,
			'fields': ["question.dutch_analyzed^3", "description.dutch_analyzed" ],
			'tie_breaker': 0
		}
	}

	docs = s.query(search)[:100].execute()

	return [QuestionResult.from_doc(d) for d in docs]

def getAnswers(questionId) -> List[AnswerResult]:
	client = Elasticsearch()

	client.transport.connection_pool.connection.headers.update(HEADERS)

	s = Search(using=client, index=A_INDEX, doc_type=A_DOC_T)

	a_query = {
		'term': {
			'questionId': questionId
		}
	}

	docs = s.query(a_query).execute()
	
	return [AnswerResult.from_doc(d) for d in docs]