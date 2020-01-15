from flask import Flask, render_template, redirect, request
from mysqlconnection import connectToMySQL
app = Flask(__name__)
@app.route("/")
def index():
    mysql = connectToMySQL('pets')
    pets = mysql.query_db('SELECT * FROM pets;')
    print(pets)
    return render_template("starter.html", all_pets=pets)


@app.route('/new_pet', methods=['POST'])
def add_a_pet():
	print (request.form)
	mysql = connectToMySQL('pets')

	query = 'INSERT INTO pets(name, type, created_at, updated_at) VALUES(%(nm)s, %(typ)s, NOW(), NOW());'
	data = {
	'nm': request.form['fullname'],
	'typ': request.form['breed']
	}
	new_pet_id = mysql.query_db(query, data)
	return redirect('/')


if __name__ == "__main__":
	app.run(debug=True)

