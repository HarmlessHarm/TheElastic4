from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from typing import List

from elasticapp.constants import *

HEADERS = {'content-type': 'application/json'}

class QuestionResult(object):
	"""docstring for QuestionResult"""
	def __init__(self, questionId, date, question, description):
		self.questionId = questionId
		self.date = date
		self.question = question
		self.description = description
		self.answers = getAnswers(questionId)

	def from_doc(doc) -> 'QuestionResult':
		return QuestionResult(
				questionId = doc.meta.id,
				date = doc.date,
				question = doc.question,
				description = doc.description,
			)

class AnswerResult(object):
	"""docstring for QuestionResult"""
	def __init__(self, answer):
		self.answer = answer

	def from_doc(doc) -> 'AnswerResult':

		return AnswerResult(
				answer = doc.answer,
			)

def getQuestions(term:str) -> List[QuestionResult]:
	client = Elasticsearch()

	client.transport.connection_pool.connection.headers.update(HEADERS)

	s = Search(using=client, index=Q_INDEX, doc_type=Q_DOC_T)
	q_query = {
		'match': {
			'question.dutch_analyzed': {
				'query': term,
				'operator': 'and',
				'fuzziness': '1',
			}
		}
	}
	d_query = {
		'match': {
			'description.dutch_analyzed': {
				'query': term,
				'operator': 'and',
				'fuzziness': '1',
			}
		}
	}
	dis_max = {
		'dis_max': {
			'tie_breaker': 0.7,
			'queries': [q_query, d_query],
		}
	}

	docs = s.query(dis_max)[:100].execute()

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