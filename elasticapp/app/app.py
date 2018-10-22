from flask import Flask, render_template, request

from elasticapp.app.search import search

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	search_terms = [
		'konijn',
		'nederlandse',
		'nederndse',
	]

	num_results = 9
	searched_questions = [(t, search(t, num_results)) for t in search_terms]
	return render_template('index.html', searched_questions=searched_questions)
