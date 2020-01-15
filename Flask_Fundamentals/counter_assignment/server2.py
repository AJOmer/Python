from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key='bigsecret'
app.count = 0

@app.route('/')
def viewers():
	# session['count'] + 1
	if 'count' in session:
		session['count'] = session.get('count') + 1
		print('it exists')
	else:
		session['count'] = 1
		print('nope not here')
	print("YO!"*25)
	return render_template('counting.html')

@app.route('/destroy_session')
def clear():
	if 'count' in session:
		session.clear()
	return redirect('/')

if __name__ == '__main__':
	app.run(debug = True)