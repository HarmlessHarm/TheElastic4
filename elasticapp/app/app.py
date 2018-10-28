from flask import Flask, render_template, request

from elasticapp.app.search import getQuestions, getAnswers
from collections import Counter

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():

	return render_template('index.html', results=None)


@app.route('/search', methods=['GET','POST'])
def search_question():
	operators = ['AND', 'OR', 'NOT']
	query = request.args.get('search')
	page = request.args.get('p')
	if not page:
		page = 1
	page = int(page) - 1
	(count, questions) = getQuestions(query, page)
	timeline = make_timeline(questions)
	wordcloud = make_wordcloud(questions)
	data = {
		'results': questions,
		'timeline': timeline,
		'wordcloud': wordcloud,
		'count': count,
		'range': '{} - {}'.format(str(page * 25 + 1), str(page * 25 + 25))
	}
	return render_template('index.html', data=data, search_term=query)

def make_timeline(results):
	dates = []

	# Results moeten nog verder uitgepakt worden
	for r in results:
		date = r.date[0:10]
		dates.append(date)

	# timeline = Counter(dates)

	return dates

def make_wordcloud(results):
	answers = {}
	for r in results:
		answers[r.questionId] = []
		for a in r.answers:
			answers[r.questionId].append(a.answer)
	# print(answers)


	return answers
