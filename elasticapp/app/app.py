from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	msg = "HOOI DIT IS DATAA"
	return render_template('index.html', data=msg)
