from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "bigasssecret"
@app.route("/")
def index():
    mysql = connectToMySQL('first_flask')
    friends = mysql.query_db('SELECT * FROM friends;')
    print(friends)
    return render_template("index.html", all_friends=friends)


@app.route('/create_friend', methods=["POST"])
def add_a_friend():
	# print (request.form)
	is_valid = True
	if len(request.form['fname']) < 1:
		is_valid = False
		flash("Please enter First Name")
	if len(request.form['lname']) < 1:
		is_valid = False
		flash('Please enter Last Name')
	if len(request.form['occ']) < 2:
		is_valid= False
		flash('What is your Occupation?')
	if is_valid:
		mysql = connectToMySQL('first_flask')
		query = 'INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES(%(fn)s, %(ln)s, %(occup)s, NOW(), NOW());'
		data = {
			'fn': request.form['fname'],
			'ln':request.form['lname'],
			'occup': request.form['occ']
		}
		flash('friend successfully added!')
		new_friend_id=mysql.query_db(query, data)
	return redirect('/')


            
if __name__ == "__main__":
	app.run(debug=True)


