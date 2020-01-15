from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
app = Flask(__name__)
import re

bcrypt = Bcrypt(app)

app.secret_key="very huge secret"

email_regex= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def new_user():
    mysql = connectToMySQL('social_media_project')
    register = mysql.query_db('SELECT * FROM login')
    # pw_hash = bcrypt.generate_password_hash(request.form['pass'])
    is_valid = True
    if len(request.form['first']) < 2:
        is_valid = False
        flash('First Name Length Requirement not met')
        return redirect('/')
    if len(request.form['last']) < 2:
        is_valid = False
        flash('Last Name Length Requirement not met')
        return redirect('/')
    if not email_regex.match(request.form['email']):
        flash('Invalid Email Pattern!')
        return redirect('/')
    if len(request.form['pass']) < 8:
        is_valid= False
        flash('Password is Weak')
        return redirect('/')
    if len(request.form['pass2']) < 1:
        is_valid= False
        flash('Password too short')
        return redirect('/')
    if request.form['pass'] != request.form['pass2']:
        is_valid = False
        flash('Passwords dont match!')
        return redirect('/')
    if not is_valid:
        return redirect ('/')
    else:
        # session['first'] = request.form['first']
        # session['last'] = request.form['last']
        pw_hash = bcrypt.generate_password_hash(request.form['pass'])
        print (pw_hash)
        mysql = connectToMySQL('social_media_project')
        query = 'INSERT INTO users (first_name, last_name, email_address, password, created_at, updated_at) VALUES(%(fn)s, %(ln)s, %(em)s, %(password_hash)s, NOW(), NOW());'
        data = {    'fn' : request.form['first'],
                    'ln' : request.form['last'],
                    'em' : request.form['email'],
                    'password_hash' : pw_hash }

        flash('Successfully registered! Please Log-in')
        mysql.query_db(query, data)
        return redirect('/')



@app.route('/login', methods=['POST'])
def login():
    mysql = connectToMySQL('social_media_project')
    query = 'SELECT * FROM users WHERE email_address = %(em)s;'
    data = { "em" : request.form['elog']}
    result = mysql.query_db(query, data)
    if len(result) > 0:
        if bcrypt.check_password_hash(result[0]['password'], request.form['plog']):
            session['userid'] = result[0]['user_id']
            session['first'] = result[0]['first_name']
            session['last'] = result[0]['last_name']
            session['mail'] = result[0]['email_address']
            return redirect ('/dashboard')
    flash("you could not be logged in")
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    flash("You've successfully logged out")
    return redirect('/')

@app.route('/dashboard')
def dash():
	mysql = connectToMySQL('social_media_project')
	query0 = 'SELECT * from users'
	if 'userid' not in session:
		flash("Please Log In")
		return redirect('/')
	people=mysql.query_db(query0)
	mysql=connectToMySQL('social_media_project')
	query1='SELECT messages.message_id, messages.text, messages.recieved_from, users.first_name, users.last_name, messages.created_at from users join messages on users.user_id=messages.uploaded_by_id'
	allmessages = mysql.query_db(query1)
	print("YOOOOOOOOOO")
	return render_template('dashboard.html', people=people, allmessages=allmessages)

@app.route('/create_post', methods=['POST'])
def newpost():
	mysql = connectToMySQL('social_media_project')
	print("YOOOOOOOOOO")
	query= 'INSERT INTO messages (text, uploaded_by_id) VALUES (%(txt)s, %(ub)s);'
	data = {
		'txt' : request.form['message1'],
		'ub' : session['userid']
	}
	mysql.query_db(query, data)
	return redirect('/dashboard')




if __name__ == '__main__':
    app.run(debug = True)