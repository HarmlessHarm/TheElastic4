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

	es.indices.delete(index=A_INDEX, ignore=404)
	es.indices.create(
		index=A_INDEX,
		body={
			'mappings':{},
			'settings':{},
		})

	# helpers.bulk(es, questions_to_index(all_questions()))
	helpers.bulk(es, answers_to_index(all_answers()))

def questions_to_index(questions):
	# Generator function that yields data objects
	print("Indexing questions")
	for i, q in enumerate(questions):

		if i % int(len(questions)/50) == 0:
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

if __name__ == '__main__':
	main()