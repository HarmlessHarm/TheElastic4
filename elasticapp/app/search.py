from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from typing import List

from elasticapp.constants import *

HEADERS = {'content-type': 'application/json'}

connections.create_connection(hosts=['localhost'])

class QuestionResult(object):
	"""docstring for QuestionResult"""
	def __init__(self, questionId, date, userId, categoryId, question, description):
		self.questionId = questionId
		self.date = date.strip('\"')
		self.user = getUser(userId)
		self.categoryId = categoryId
		self.question = question
		self.description = description
		self.answers = getAnswers(questionId)

	def from_doc(doc) -> 'QuestionResult':
		return QuestionResult(
				questionId = doc.meta.id,
				date = doc.date,
				userId = doc.user,
				categoryId = doc.category,
				question = doc.question,
				description = doc.description,
			)

class AnswerResult(object):
	"""docstring for QuestionResult"""
	def __init__(self, answerId, date, answer, userId, questionId, thumbsUp, thumbsDown, isBestAnswer):
		self.answer = answer
		self.answerId = answerId
		self.date = date.strip('\"')
		self.user = getUser(userId)
		self.questionId = questionId
		self.thumbsUp = thumbsUp
		self.thumbsDown = thumbsDown
		self.isBestAnswer = isBestAnswer

	def from_doc(doc) -> 'AnswerResult':

		return AnswerResult(
				answerId = doc.meta.id,
				date = doc.date,
				answer = doc.answer,
				userId = doc.user,
				questionId = doc.questionId,
				thumbsUp = doc.thumbsUp,
				thumbsDown = doc.thumbsDown,
				isBestAnswer = doc.isBestAnswer,
			)

class UserResult(object):
	"""docstring for UserResult"""
	def __init__(self, userId, regDate, expertise, bestAnswers):
		self.userId = userId
		self.regDate = regDate.strip('\"')
		self.expertise = expertise
		self.bestAnswers = bestAnswers
	
	def from_doc(doc) -> 'UserResult':

		return UserResult(
				userId = doc.meta.id,
				regDate = doc.date,
				expertise = doc.expertise,
				bestAnswers = doc.bestAnswers,
			)

def getQuestions(query:str,page:int) -> List[QuestionResult]:
	client = Elasticsearch()

	client.transport.connection_pool.connection.headers.update(HEADERS)

	s = Search(using=client, index=Q_INDEX, doc_type=Q_DOC_T)
	query_dict = {
		'from': page * 50,
		'query': {
			'bool': {
				'must': {
					'query_string': {
						"fields": [ "question.dutch_analyzed^10", "description.dutch_analyzed" ],
						'query': query
					}
				}
			}
		}
	}

	search = s.from_dict(query_dict)
	count = search.count()
	strt = int(page)
	end = int(page) + 50
	docs = search[strt:end].execute()

	return (count, [QuestionResult.from_doc(d) for d in docs])

def getAdvanced(query) -> List[QuestionResult]:

	client = Elasticsearch()
	client.transport.connection_pool.connection.headers.update(HEADERS)
	s = Search(using=client, index=Q_INDEX, doc_type=Q_DOC_T)

	query_dict = {
		'query': {
			'bool': {
				'must': {
					'query_string': {
						"fields": [ "question.dutch_analyzed^10", "description.dutch_analyzed" ],
						'query': query
					}
				}
			}
		}
	}
	search = s.from_dict(query_dict)
	print("length!!", search.count())
	docs = search[:50].execute()

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


def getUser(userId) -> UserResult:
	client = Elasticsearch()

	client.transport.connection_pool.connection.headers.update(HEADERS)

	s = Search(using=client, index=U_INDEX, doc_type=U_DOC_T)
	u_query = {
		'term': {
			'_id': {
				'value': userId
			}
		}
	}

	docs = s.query(u_query).execute()
	if len(docs) > 0:
		return UserResult.from_doc(docs[0])
	return False
		