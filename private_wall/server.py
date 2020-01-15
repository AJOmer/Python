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
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def new_user():
    mysql = connectToMySQL('wall')
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
        mysql = connectToMySQL('wall')
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
    mysql = connectToMySQL('wall')
    query = 'SELECT * FROM users WHERE email_address = %(em)s;'
    data = { "em" : request.form['elog']}
    result = mysql.query_db(query, data)
    if len(result) > 0:
        if bcrypt.check_password_hash(result[0]['password'], request.form['plog']):
            session['userid'] = result[0]['user_id']
            session['first'] = result[0]['first_name']
            session['last'] = result[0]['last_name']
            session['mail'] = result[0]['email_address']
            return redirect ('/wall')
    flash("you could not be logged in")
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    flash("You've successfully logged out")
    return redirect('/')


@app.route('/wall')
def mywall():
    mysql= connectToMySQL('wall')
    query1 = 'SELECT * from users'
    if 'userid' not in session:
        flash('Please Log in')
        return redirect('/')
    sendit = mysql.query_db(query1)
    query = 'SELECT text, receive_from, message_id from messages WHERE send_to = %(ui)s;'
    data = {
        'ui': session['userid']
    }
    mysql = connectToMySQL('wall')
    buildwall = mysql.query_db(query, data)
    return render_template('wall.html', name_on_template = session['first'], buildwall=buildwall, sending=sendit)

@app.route('/create_message', methods=['POST'])
def newmess():
    mysql = connectToMySQL('wall')
    query = 'INSERT INTO messages (text, send_to, receive_from, created_at, updated_at, user_message_id) VALUES(%(txt)s, %(st)s, %(rf)s, NOW(), NOW(), %(ea)s);'
    data = { 
    'txt': request.form['message1'],
    'st' : request.form['messsend'],
    'rf' : session['first'],
    'ea' : session['userid']
    }
    flash('MESSAGE ACCEPTED')
    mysql.query_db(query, data)
    return redirect('/wall')

@app.route('/destroy/<int:id>')
def deleteit(id):
    id = str(id)
    mysql = connectToMySQL('wall')
    query = 'DELETE FROM messages WHERE message_id= %(ui)s;'
    data = {
        'ui': id
    }
    mysql.query_db(query, data)
    return redirect('/wall')

if __name__ == '__main__':
    app.run(debug = True)