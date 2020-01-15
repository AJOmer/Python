from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
import re
app = Flask(__name__)
app.secret_key="super secret"

email_regex= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

@app.route('/')
def index():
	mysql = connectToMySQL('email_validation')
	mail = ('SELECT * FROM email;')
	return render_template('login.html', whole_mail = mail)

@app.route('/success', methods = ['POST'])
def result():
	mysql = connectToMySQL('email_validation')
	mail = mysql.query_db('SELECT * FROM email;')
	is_valid= True
	if len(request.form['email_addy']) < 5:
		is_valid = False
		flash('Email Length not met')
		return redirect('/')
	if not email_regex.match(request.form['email_addy']):
		flash("Invalid Email Pattern!")
		return redirect('/')
	for one_email in mail:
		if request.form['email_addy'] == one_email['email_address']:
			is_valid = False
			flash('email already taken')
	if not is_valid:
		return redirect('/')
	else:
		flash("The Email address you entered is a VALID email address! Thank You!")
		mysql = connectToMySQL('email_validation')
		query = 'INSERT INTO email (email_address, created_at, updated_at) VALUES(%(em)s, NOW(), NOW());'
		data = {
			'em' : request.form['email_addy']
		}
		email_address = request.form['email_addy']
		new_email_id = mysql.query_db(query, data)
		mysql = connectToMySQL('email_validation')
		mail = mysql.query_db('SELECT * FROM email;')
	return render_template('success.html', whole_mail = mail, the_email = email_address)





if __name__ == '__main__':
	app.run(debug = True)