from elasticsearch import Elasticsearch, helpers

from elasticapp.constants import *
from elasticapp.data import *

def main():
	es = Elasticsearch()

	es.indices.delete(index=Q_INDEX, ignore=404)
	es.indices.create(
		index=Q_INDEX,
		body={
			'mappings':{},
			'settings':{},
		})

	helpers.bulk(es, questions_to_index(all_questions(False)))

def questions_to_index(questions):
	# Generator function that yields data objects
	for q in questions:
		yield {
			'_op_type': 'create',
			'_index': Q_INDEX,
			'_type': Q_DOC_T,
			'_id': q.questionId,
			'_source': {
				'date': q.date,
				'user': q.userId,
				'category': q.categoryId,
				'question': q.question,
				'description': q.description
			}
		}

if __name__ == '__main__':
	main()