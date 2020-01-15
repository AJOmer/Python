from flask import Flask, render_template, request, redirect, session, flash 
from mysqlconnection import connectToMySQL  
app = Flask(__name__)
app.secret_key="omg a secret"
@app.route('/')
def index():
	mysql = connectToMySQL('dojo_survey')
	survey = mysql.query_db('SELECT * FROM dojo_survey;')
	return render_template('survey.html', whole_survey= survey)

@app.route('/results', methods = ['POST'])
def outcome():
	# print('*' *80)
	is_valid = True
	if len(request.form['name1']) < 1:
		is_valid= False
		flash('Please enter a Name')
	if len(request.form['Select1']) < 1:
		is_valid=False
		flash('Choose Location')
	if len(request.form['Select2']) < 1:
		is_valid= False
		flash('Fav Language?')
	if len(request.form['textarea1']) < 1:
		is_valid= False
		flash('Its Optional but just do it!')
	if not is_valid:
		return redirect('/')
	else:
		flash("Thanks for your feedback!")
		mysql = connectToMySQL('dojo_survey')
		query = 'INSERT INTO survey (name, location, language, comment, created_at, updated_at)  VALUES(%(nm)s, %(slct1)s, %(slct2)s, %(txt)s, NOW(), NOW());'		
		data = {
			'nm' : request.form['name1'],
			'slct1' : request.form['Select1'],
			'slct2' : request.form['Select2'],
			'txt' : request.form['textarea1']
		}
		full_name = request.form['name1']
		location = request.form['Select1']
		language = request.form['Select2']
		comment = request.form['textarea1']
		new_survey_id = mysql.query_db(query, data)
		mysql = connectToMySQL('dojo_survey')
		survey = mysql.query_db('SELECT * FROM survey')
	return render_template('results.html', whole_survey = survey, the_name = full_name, the_location = location, fav_lang= language, nit_pick= comment)


if __name__ == '__main__':
	app.run(debug = True)




	# 	full_name = request.form['name1']
	# location = request.form['Select1']
	# language = request.form['Select2']
	# comment = request.form['textarea1']

		# return render_template('results.html', the_name = full_name, the_location = location, fav_lang= language, nit_pick= comment)