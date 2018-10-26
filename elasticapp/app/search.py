from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from typing import List

from elasticapp.constants import *

HEADERS = {'content-type': 'application/json'}

class SearchResult(object):
	"""docstring for SearchResult"""
	def __init__(self, qid, question, description, date):
		super(SearchResult, self).__init__()
		self.id = qid
		self.question = question
		self.description = description
		self.date = date

	def from_doc(doc) -> 'SearchResult':
		return SearchResult(
				qid = doc.meta.id,
				question = doc.question,
				description = doc.description,
				date = doc.date,
			)
		pass


def search(term:str, count:int) -> List[SearchResult]:
	client = Elasticsearch()

	client.transport.connection_pool.connection.headers.update(HEADERS)

	s = Search(using=client, index=Q_INDEX, doc_type=Q_DOC_T)
	q_query = {
		'match': {
			'question': {
				'query': term,
				'operator': 'and',
				'fuzziness': 'AUTO',
			}
		}
	}

	docs = s.query(q_query)[:count].execute()

	return [SearchResult.from_doc(d) for d in docs]
