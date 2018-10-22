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
	results = [(t, search(t, num_results)) for t in search_terms]
	return render_template('index.html', results=results)


@app.route('/search', methods=['GET','POST'])
def search_question():

	query = request.args.get('search')
	num_results = 50
	results = [(query, search(query, num_results))]
	return render_template('index.html', results=results,search_term=query)