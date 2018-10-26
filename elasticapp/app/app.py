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

	query = request.args.get('search')
	questions = getQuestions(query)
	return render_template('index.html', results=questions,search_term=query)

def make_timeline(results):
	dates = []

	# Results moeten nog verder uitgepakt worden
	for r in results:
		date = r.date[1:5]
		dates.append(date)

	timeline = Counter(dates)

	return timeline
