from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt 
import re
app=Flask(__name__)


bcrypt=Bcrypt(app)
app.secret_key="Hiddenaway"

email_regex= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/')
def index():
	return render_template('login.html')

@app.route('/register', methods=['POST'])
def reg():
	mysql = connectToMySQL('testschema')
	mysql.query_db = ('SELECT * from users')
	is_valid = True
	if len(request.form['first']) < 2:
		is_valid = False
		flash("First Name Length Not Met")
		return redirect('/')
	if len(request.form['last']) < 2:
		is_valid = False
		flash("Last Name Length Not Met")
		return redirect('/')
	if not email_regex.match(request.form['email']):
		flash('Invalid Email Pattern')
		return redirect('/')
	if len(request.form['pass1']) < 8:
		is_valid = False
		flash("Password Length Requirement not met")
		return redirect('/')
	if len(request.form['pass2']) < 8:
		is_valid = False
		flash("Invalid password confirmation")
		return redirect('/')
	if request.form['pass1'] != request.form['pass2']:
		is_valid = False
		flash("Passwords don't Match!")
		return redirect('/')
	else:
		pw_hash = bcrypt.generate_password_hash(request.form['pass1'])
		print (pw_hash)
		mysql = connectToMySQL('testschema')
		query = 'INSERT into users (first_name, last_name, email_address, password, created_at, updated_at) VALUES(%(fn)s, %(ln)s, %(em)s, %(password_hash)s, NOW(), NOW()); '
		data = {
			'fn' : request.form['first'],
			'ln' : request.form['last'],
			'em' : request.form['email'],
			'password_hash' : pw_hash
		}
		flash('Successfully registered! Please Log-in')
		mysql.query_db(query, data)
		return redirect('/')

@app.route('/login', methods=['POST'])
def signin():
	mysql = connectToMySQL('testschema')
	query = 'SELECT * FROM users Where email_address = %(em)s;'
	data = { 'em' : request.form['elog']}
	logon = mysql.query_db(query, data)
	if len(logon) > 0:
		if bcrypt.check_password_hash(logon[0]['password'], request.form['plog']):
			session['userid'] = logon[0]['users_id']
			session['first'] = logon[0]['first_name']
			session['last'] = logon[0]['last_name']
			session['email'] = logon[0]['email_address']
			return redirect('/dashboard')
	flash("You could not be logged in ")
	return redirect('/')



@app.route('/logout')
def logout():
	session.clear()
	flash("You have successfully logged out")
	return redirect('/')



@app.route('/dashboard')
def dash():
	mysql = connectToMySQL('testschema')
	query0 = "SELECT * from users"
	if 'userid' not in session:
		flash("Please Log In")
		return redirect('/')	
	mysql = connectToMySQL('testschema')
	query1 = 'SELECT books.book_id, books.book_title, users.first_name, users.last_name, users.users_id, books.uploaded_by_id from users join books on users.users_id=books.uploaded_by_id;'
	allbooks= mysql.query_db(query1)


	return render_template('index.html', allbooks=allbooks)





@app.route('/add_book', methods=['POST'])
def main():
	mysql = connectToMySQL('testschema')
	query1 = "INSERT into books(books.book_title, books.about_book, books.uploaded_by_id, books.created_at) VALUES (%(bt)s, %(ab)s, %(ub)s, NOW());"
	data1 = {
		"bt" : request.form['title'],
		"ab" : request.form['about'],
		"ub" : session['userid']
	}
	adding = mysql.query_db(query1, data1)
	return redirect('/dashboard')


@app.route('/dashboard/<id>/show')
def show(id):
	mysql = connectToMySQL('testschema')
	query = 'SELECT * FROM users join books on users.users_id=books.uploaded_by_id where book_id=%(id)s;'
	data = {
		"id": id
	}
	library = mysql.query_db(query, data)
	return render_template('edit.html', library=library)





@app.route('/dashboard/<id>/edit')
def viewupdate(id):
	mysql = connectToMySQL('testschema')
	return render_template('useredit.html', book_id=id)



@app.route('/updating/<int:id>', methods=['POST'])
def update(id):
	# id = str(id)
	# *****NEW QUERY TO SELECT BOOK_ID****
	# mysql = connectToMySQL('testschema')
	# query1 = "SELECT book_id FROM books where id = %(id)s;"
	# data = {
	# 	"id" : id
	# }
	# choosing = mysql.query_db(query1, data)
	print('hiIiiiiiiiiiiiiiiiiiiiiiiiiii')
	mysql = connectToMySQL('testschema')
	query = "UPDATE books SET book_title = %(bti)s, about_book = %(about)s WHERE book_id=%(id)s;"
	data = {
		"bti" : request.form['new_name'],
		"about" : request.form['description'],
		"id" : id
	}
	update = mysql.query_db(query, data)
	return redirect('/dashboard' )	




if __name__ == '__main__':
	app.run(debug = True)