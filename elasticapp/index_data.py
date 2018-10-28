from elasticsearch import Elasticsearch, helpers

from elasticapp.constants import *
from elasticapp.data import *

import sys

def main(test):
	es = Elasticsearch()

	es.indices.delete(index=Q_INDEX, ignore=404)
	es.indices.create(
		index=Q_INDEX,
		body={
			'mappings':{
				Q_DOC_T: {
					'properties': {
						'question': {
							'type': 'text',
							'fields': {
								'dutch_analyzed': {
									'type': 'text',
									'analyzer': 'dutch'
								}
							}
						},
						'description': {
							'type': 'text',
							'fields': {
								'dutch_analyzed': {
									'type': 'text',
									'analyzer': 'dutch'
								}
							}
						},
						'category': {
							'type': 'keyword'
						},
						# 'date': {
						# 	'type': 'date',
						# 	"format": "yyyy-MM-dd HH:mm:ss"
						# }
					},
				},
			},
			'settings':{},
		})
	helpers.bulk(es, questions_to_index(all_questions(test)))

	es.indices.delete(index=A_INDEX, ignore=404)
	es.indices.create(
		index=A_INDEX,
		body={
			'mappings':{
				A_DOC_T: {
					'properties': {
						'answer': {
							'type': 'text',
							'fields': {
								'dutch_analyzed': {
									'type': 'text',
									'analyzer': 'dutch'
								}
							}
						},
					},
				}
			},
			'settings':{},
		})

	helpers.bulk(es, answers_to_index(all_answers(test)))

	es.indices.delete(index=C_INDEX, ignore=404)
	es.indices.create(
		index=C_INDEX,
		body={
			'mappings':{},
			'settings':{},
		})

	helpers.bulk(es, categories_to_index(all_categories()))

	es.indices.delete(index=U_INDEX, ignore=404)
	es.indices.create(
		index=U_INDEX,
		body={
			'mappings':{},
			'settings':{},
		})

	helpers.bulk(es, users_to_index(all_users()))

def questions_to_index(questions):
	# Generator function that yields data objects
	print("Indexing questions")
	for i, q in enumerate(questions):

		if i % int(len(questions) / 50) == 0:
			print('.', end="", flush=True)
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
	print("\nFinished indexing {} questions".format(len(questions)))

def answers_to_index(answers):
	print("Indexing answers")
	for i, a in enumerate(answers):
		if i % int(len(answers) / 50) == 0:
			print('.', end="", flush=True)
		yield {
			'_op_type': 'create',
			'_index': A_INDEX,
			'_type': A_DOC_T,
			'_id': a.answerId,
			'_source': {
				'date': a.date,
				'user': a.userId,
				'questionId': a.questionId,
				'answer': a.answer,
				'thumbsUp': a.thumbsUp,
				'thumbsDown': a.thumbsDown,
				'isBestAnswer': a.isBestAnswer,
			}
		}
	print("\nFinished indexing {} answers".format(len(answers)))


def categories_to_index(categories):
	print("Indexing categories")
	for i, c in enumerate(categories):
		if i % int(len(categories) / 50) == 0:
			print('.', end="", flush=True)
		yield {
			'_op_type': 'create',
			'_index': C_INDEX,
			'_type': C_DOC_T,
			'_id': c.categoryId,
			'_source': {
				'parentId': c.parentId,
				'name': c.name,
			}
		}
	print("\nFinished indexing {} categories".format(len(categories)))

def users_to_index(users):
	print("Indexing users")
	for i, u in enumerate(users):
		if i % int(len(users) / 50) == 0:
			print('.', end="", flush=True)
		yield {
			'_op_type': 'create',
			'_index': U_INDEX,
			'_type': U_DOC_T,
			'_id': u.userId,
			'_source': {
				'date': u.date,
				'expertise': u.expertise,
				'bestAnswers': u.bestAnswers,
			}
		}
	print("\nFinished indexing {} users".format(len(users)))


if __name__ == '__main__':
	test = False
	if len(sys.argv) > 1 and sys.argv[1] == 'test':
		test = True
	main(test)