from flask import Flask, render_template, request

from elasticapp.app.search import getQuestions, getAnswers
from collections import Counter

import os

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():

	return render_template('index.html', results=None)


@app.route('/search', methods=['GET','POST'])
def search_question():

	query = request.args.get('search')
	
	q = request.args.get('question')
	d = request.args.get('description')
	y = request.args.get('year')
	c = request.args.get('category')

	# print(category)
	page = request.args.get('p')

	if not page:
		page = 1
	page = int(page) - 1
	(count, questions, categories) = getQuestions(query, page, q,d,y,c)
	timeline = make_timeline(questions)
	wordcloud = make_wordcloud(questions)
	data = {
		'results': questions,
		'timeline': timeline,
		'wordcloud': wordcloud,
		'count': count,
		'range': '{} - {}'.format(str(page * 10 + 1), str(min(count,page * 10 + 10))),
		'categories': categories,
	}
	search_terms = {
		'query': query,
		'question': q,
		'description': d,
		'year': y,
		'category': c,
	}
	return render_template('index.html', data=data, search_terms=search_terms)

def make_timeline(results):
	dates = []

	# Results moeten nog verder uitgepakt worden
	for r in results:
		date = r.date[0:10]
		dates.append(date)
		
	# timeline = Counter(dates)

	return dates

def make_wordcloud(results):
	parent_dir = os.path.dirname(os.path.abspath(__file__))
	file_path = os.path.join(parent_dir, 'static/stopwords-nl.txt')
	stop_words = open(file_path).read().split()
	answers = {}
	for r in results:
		answers[r.questionId] = []
		for a in r.answers:
			filtered = [word for word in a.answer.split(' ') if word not in stop_words]
			answers[r.questionId].append(filtered)

	return answers
