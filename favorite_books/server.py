from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt 
import re
app=Flask(__name__)

bcrypt=Bcrypt(app)
app.secret_key="SecretStash"

email_regex= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register', methods=['POST'])
def reg():
	mysql = connectToMySQL('favbooks')
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
		mysql = connectToMySQL('favbooks')
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
	mysql = connectToMySQL('favbooks')
	query = 'SELECT * FROM users Where email_address = %(em)s;'
	data = { 'em' : request.form['elog']}
	logon = mysql.query_db(query, data)
	if len(logon) > 0:
		if bcrypt.check_password_hash(logon[0]['password'], request.form['plog']):
			session['userid'] = logon[0]['user_id']
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
	mysql=connectToMySQL('favbooks')
	query1 = 'SELECT * from users'
	if 'userid' not in session:
		flash("Please Log-in")
		return redirect('/')
	theusers = mysql.query_db(query1)
	query = 'SELECT users.user_id, users.first_name,books.book_name, books.book_id, books.users_user_id FROM users JOIN books ON users.user_id=books.users_user_id where books.borrowed_by is NULL;'
	mysql = connectToMySQL('favbooks')
	thebooks= mysql.query_db(query)
	# print(thebooks)
	query = "SELECT books.book_name, users.user_id, books.book_id, books.borrowed_by from users JOIN books on users.user_id=books.users_user_id where books.borrowed_by = %(id)s;"
	data = {
		"id" : session['userid']
	}
	mysql=connectToMySQL('favbooks')
	thename= mysql.query_db(query, data)
	query2 = 'SELECT books.book_name, users.user_id, users.first_name, books.book_id, books.borrowed_by from users JOIN books on users.user_id=books.borrowed_by where books.users_user_id = %(id)s;'
	data2 = {
		"id" : session['userid']
	}
	mysql = connectToMySQL('favbooks')
	letborrow = mysql.query_db(query2, data2)
	return render_template('books.html', theusers=theusers, thebooks=thebooks, thename=thename, letborrow=letborrow)

@app.route('/add_book_page')
def new_add():
	return render_template('add.html')

@app.route('/new_book', methods=['POST'])
def addit():
	mysql = connectToMySQL('favbooks')
	query = 'INSERT INTO books(book_name, author, about_book, users_user_id, created_at) VALUES (%(bn)s, %(au)s, %(ab)s, %(li)s, NOW());'
	data = {
		"bn" : request.form['title'],
		"au" : request.form['auth'],
		"ab" : request.form['desc'],
		"li" : session['userid']
	}
	newq = mysql.query_db(query, data)
	return redirect('/dashboard')


@app.route('/dashboard/<id>/show')
def info(id):
	mysql = connectToMySQL('favbooks')
	query = "SELECT * FROM users JOIN books on users.user_id=books.users_user_id where book_id = %(id)s;"
	data = {
		"id" : id
	}
	library = mysql.query_db(query, data)
	return render_template('shows.html', id = id, library=library)

@app.route('/dashboard/<id>/destroy')
def boom(id):
	mysql = connectToMySQL('favbooks')
	query = 'DELETE FROM books where book_id = %(id)s;'
	data = {
		"id" : id
	}
	dest = mysql.query_db(query, data)
	return redirect('/dashboard')

@app.route('/dashboard/<id>/borrow')
def borrowing(id):
	mysql = connectToMySQL('favbooks')
	query = 'UPDATE books SET borrowed_by = %(id)s WHERE book_id = %(yo)s;'
	data = {
		"id" : session['userid'],
		"yo" : id
	}
	mysql.query_db(query, data)
	return redirect('/dashboard')

@app.route('/dashboard/<id>/return')
def release(id):
	mysql = connectToMySQL('favbooks')
	query = 'UPDATE books SET borrowed_by = NULL where book_id = %(id)s ;'
	data = {
		"id" : id
	}
	returning = mysql.query_db(query, data)
	return redirect('/dashboard')

@app.route('/availbooks/<id>')
def book2borrow(id):
	mysql= connectToMySQL('favbooks')
	query = 'SELECT users.first_name, books.book_name, books.book_id from users join books on users.user_id=books.users_user_id where books.users_user_id = %(id)s AND books.borrowed_by is NULL;'
	data = {
		"id" : id
	}
	inventory = mysql.query_db(query, data)
	return render_template('borrowbooks.html', inventory=inventory)

@app.route('/dashboard/<id>/edit')
def edit(id):
	mysql = connectToMySQL('favbooks')
	query = 'SELECT users.user_id, users.first_name, books.book_id, books.borrowed_by from users join books on users.user_id= books.users_user_id where users.user_id=%(id)s;'
	data = {
		"id" : id
	}
	useredit = mysql.query_db(query, data)
	# print("THIS IS THE ENDDDDDDDDDDDDDDDD", useredit)
	# is_valid = True
	# if useredit['user_id'] != str(session['userid']):
	# 	is_valid = False
	# 	flash("nacho cheese")
	# 	return redirect('/dashboard')
	return render_template ('edit.html', useredit=useredit)

if __name__ == '__main__':
	app.run(debug = True)