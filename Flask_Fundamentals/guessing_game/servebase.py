from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key='sosecretive'

def numset():
	session['answer']=random.int(1,100)

@app.route('/')
def index():
	print('yo'*25)
	if session['answer'] == None:
		numset()
	else:
		print session['num']
	return render_template('guess.html')

@app.route('/conclusion', methods=['POST'])
def conclusion():
	WRONG = None
	BINGO = None
	



if __name__ == '__main__':
	app.run(debug = True)