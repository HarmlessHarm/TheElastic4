from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from typing import List

from elasticapp.constants import *

HEADERS = {'content-type': 'application/json'}

class SearchResult(object):
	"""docstring for SearchResult"""
	def __init__(self, qid, question, description):
		self.id = qid
		self.question = question
		self.description = description

	def from_doc(doc) -> 'SearchResult':
		return SearchResult(
				qid = doc.meta.id,
				question = doc.question,
				description = doc.description,
			)

class AnswerResult(object):
	"""docstring for SearchResult"""
	def __init__(self, answer):
		self.answer = answer

	def from_doc(doc) -> 'AnswerResult':

		return AnswerResult(
				answer = doc.answer,
			)

def search(term:str, count:int) -> List[SearchResult]:
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

	docs = s.query(dis_max)[:count].execute()

	return [SearchResult.from_doc(d) for d in docs]


def findAnswers(query):
	client = Elasticsearch()

	client.transport.connection_pool.connection.headers.update(HEADERS)

	s = Search(using=client, index=A_INDEX, doc_type=A_DOC_T)

	a_query = {
		'term': {
			'questionId': query
		}
	}

	docs = s.query(a_query).execute()
	
	return [AnswerResult.from_doc(d) for d in docs]