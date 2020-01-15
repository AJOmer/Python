from flask import Flask, render_template, redirect, request
from sqlconnection import connectToMySQL
app = Flask(__name__)
@app.route("/")
def index():
	mysql = connectToMySQL('users')
	print('friends')
	friends = mysql.query_db('SELECT * FROM friends;')
	return render_template('all_users.html', all_friends=friends)

@app.route('/new_user', methods=['POST'])
def add_a_user():
	print(request.form)
	mysql = connectToMySQL('users')

	query = 'INSERT INTO friends(first_name, last_name, email, created_at) VALUES (%(fn)s, %(ln)s, %(email)s, NOW());'
	data= {
	'fn': request.form['fname'],
	'ln': request.form['lname'],
	'email': request.form['mail']
	}
	new_friend_id = mysql.query_db(query, data)
	return redirect('/')

@app.route('/new_page')
def go_to():
	print('hi')
	return render_template('add_user.html')


@app.route('/all_users/<id>')
def info_display(id):
	id=id
	query2 = "SELECT * FROM friends where user_id=%(id)s;"
	data2 = {
		"id": id
	}
	mysql = connectToMySQL('users')
	friends = mysql.query_db(query2, data2)
	return render_template('show.html',id=id, friends=friends)


@app.route('/all_users/<id>/edit')
def edit(id):
	id=id
	query3= "SELECT * FROM friends where user_id=%(id)s;"
	data3= {
		"id":id
	}
	mysql= connectToMySQL('users')
	friends= mysql.query_db(query3, data3)
	return render_template('edit.html', id=id, friends=friends)

@app.route('/all_users/<id>/destroy')
def destroy(id):
	id=id
	query4= "DELETE FROM friends where user_id=%(id)s;"
	data4={
		"id":id
	}
	mysql= connectToMySQL('users')
	friends=mysql.query_db(query4, data4)
	return redirect('/')

@app.route('/all_users/<id>/update', methods=['POST'])
def update(id):
	id=id
	mysql = connectToMySQL('users')
	query5= "UPDATE friends SET first_name = %(fn)s, last_name=%(ln)s, email=%(email)s WHERE user_id=%(id)s;"
	data5 = {
		"id": id,
		"fn":request.form['fname'],
		"ln": request.form['lname'],
		"email": request.form['mail']
	}
	new_friend_id = mysql.query_db(query5, data5)
	return redirect('/')

if __name__ == "__main__":
	app.run(debug=True)