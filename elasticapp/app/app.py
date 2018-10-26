from flask import Flask, render_template, request

from elasticapp.app.search import getQuestions, getAnswers, getAdvanced
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
	if any(o in query for o in operators):
		questions = getAdvanced(query)
	questions = getQuestions(query)
	timeline = make_timeline(questions)
	wordcloud = make_wordcloud(questions)
	return render_template('index.html', results=questions,search_term=query,timeline=timeline,wordcloud=wordcloud)

def make_timeline(results):
	dates = []

	# Results moeten nog verder uitgepakt worden
	for r in results:
		date = int(r.date[1:5])
		dates.append(date)

	# timeline = Counter(dates)

	return dates

def make_wordcloud(results):
	answers = {}
	for r in results:
		answers[r.questionId] = []
		for a in r.answers:
			answers[r.questionId].append(a.answer)
	print(answers)


	return answers
