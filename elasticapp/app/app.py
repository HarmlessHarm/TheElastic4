from flask import Flask, render_template, request

from elasticapp.app.search import getQuestions, getAnswers

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	
	return render_template('index.html', results=None)


@app.route('/search', methods=['GET','POST'])
def search_question():

	query = request.args.get('search')
	questions = getQuestions(query)
	results = {}
	for q in questions:
		answers = getAnswers(q.questionId)
		results[q.questionId] = {'question': q, 'answers': answers}

	return render_template('index.html', results=results,search_term=query)



@app.route('/question', methods=['GET', 'POST'])
def search_answers():

	query = request.args.get('search')
	results = [(findAnswers(query))]
	return render_template('answer.html', results=results)