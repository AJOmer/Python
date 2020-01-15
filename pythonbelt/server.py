from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt 
import re
app=Flask(__name__)


bcrypt=Bcrypt(app)
app.secret_key="VeryHiddenAway"

email_regex= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/')
def index():
	return render_template('login.html')

@app.route('/register', methods=['POST'])
def reg():
	mysql = connectToMySQL('jobs')
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
		mysql = connectToMySQL('jobs')
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
	mysql = connectToMySQL('jobs')
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
	mysql = connectToMySQL('jobs')
	query0 = 'SELECT * from users'
	if 'userid' not in session:
		flash("Please Log In")
		return redirect('/')
	mysql = connectToMySQL('jobs')
	query1 = "SELECT users.user_id, users.first_name, users.last_name, jobs.job_id, jobs.job_name, jobs.location, jobs.created_at, jobs.updated_at, jobs.uploaded_by_id from users join jobs on users.user_id=jobs.uploaded_by_id"
	alljobs = mysql.query_db(query1)
	return render_template('index.html', alljobs=alljobs)


@app.route('/add_new_job')
def addnew():
	return render_template('add.html')

@app.route('/new_job', methods=['POST'])
def addit():
	mysql = connectToMySQL('jobs')
	is_valid = True
	if len(request.form['title']) < 3:
		is_valid = False
		flash('Job title must be at least 3 characters!')
		return redirect('/add_new_job')
	if len(request.form['desc']) < 3:
		is_valid = False
		flash('Description must be at least 3 characters!')
		return redirect('/add_new_job')
	if len(request.form['locate']) < 3:
		is_valid = False
		flash('Location must be provided!')
		return redirect('/add_new_job')
	else:
		query = 'INSERT INTO jobs(job_name, about_job, location, uploaded_by_id, created_at) VALUES (%(jn)s, %(ab)s, %(loc)s, %(ub)s, NOW());'
		data = {
			"jn" : request.form['title'],
			"ab" : request.form['desc'],
			"loc" : request.form['locate'],
			"ub" : session['userid']
		}
		newj = mysql.query_db(query, data)
		return redirect('/dashboard')


@app.route('/dashboard/<id>/destroy')
def delete(id):
	mysql = connectToMySQL('jobs')
	query = "DELETE FROM jobs where job_id = %(id)s;"
	data = {
		"id": id
	}
	boom = mysql.query_db(query, data)
	return redirect('/dashboard')

@app.route('/dashboard/<id>/view')
def show(id):
	mysql = connectToMySQL('jobs')
	query = "SELECT * from users join jobs on users.user_id=jobs.uploaded_by_id WHERE job_id = %(id)s;"
	data = {
		"id" : id
	}
	jobinfo = mysql.query_db(query, data)
	return render_template('view.html', jobinfo=jobinfo)

@app.route('/dashboard/<id>/edit')
def renderedit(id):
	mysql= connectToMySQL('jobs')
	return render_template('edit.html', job_id=id)

@app.route('/updating/<int:id>', methods=['POST'])
def update(id):
	mysql=connectToMySQL('jobs')
	is_valid= True
	if len(request.form['new_title']) < 3:
		is_valid= False
		flash("Title length did not meet requirements")
		return redirect('/dashboard/'+str(id)+'/edit')
	if len(request.form['new_desc']) < 3:
		is_valid= False
		flash("Description needs to be greater than 3 characters")
		return redirect('/dashboard/'+str(id)+'/edit')
	if len(request.form['new_loc']) < 3:
		is_valid= False
		flash("Location length not met")
		return redirect('/dashboard/'+str(id)+'/edit')
	else:
		query = "UPDATE jobs SET job_name = %(njn)s, about_job = %(nja)s, location = %(nl)s WHERE job_id = %(id)s;"
		data = {
			"njn": request.form['new_title'],
			"nja": request.form['new_desc'],
			"nl" : request.form['new_loc'],
			"id" : id
		}
		updateit = mysql.query_db(query, data)
		return redirect('/dashboard')

if __name__ == '__main__':
	app.run(debug = True)