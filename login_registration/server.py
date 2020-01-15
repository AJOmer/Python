from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
app = Flask(__name__)
import re

bcrypt = Bcrypt(app)

app.secret_key="huge secret"

email_regex= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET','POST'])
def new_user():
    mysql = connectToMySQL('login_registration')
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
    if len(request.form['pass']) < 7:
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
        session['first'] = request.form['first']
        pw_hash = bcrypt.generate_password_hash(request.form['pass'])
        print (pw_hash)
        mysql = connectToMySQL('login_registration')
        query = 'INSERT INTO login (first_name, last_name, email_address, password, created_at, updated_at) VALUES(%(fn)s, %(ln)s, %(em)s, %(password_hash)s, NOW(), NOW());'
        data = {    'fn' : request.form['first'],
                    'ln' : request.form['last'],
                    'em' : request.form['email'],
                    'password_hash' : pw_hash }

        flash('Successfully registered!')
        mysql.query_db(query, data)
        # register = mysql.query_db('SELECT * FROM login;')

        return redirect('/success')



@app.route('/login', methods=['POST'])
def login():
    mysql = connectToMySQL('login_registration')
    query = 'SELECT * FROM login WHERE email_address = %(em)s;'
    data = { "em" : request.form['elog']}
    result = mysql.query_db(query, data)
    if len(result) > 0:
        if bcrypt.check_password_hash(result[0]['password'], request.form['plog']):
            session['userid'] = result[0]['id']
            session['first'] = result[0]['first_name']
            return redirect ('/success')
    flash("you could not be logged in")
    return redirect('/')


@app.route('/success')
def success():
    return render_template('success.html', name_on_template = session['first'])


@app.route('/logout')
def logout():
    session.clear()
    flash("You've successfully logged out")
    return redirect('/')




if __name__ == '__main__':
    app.run(debug = True)