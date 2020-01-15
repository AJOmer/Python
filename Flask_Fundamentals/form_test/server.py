from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'lawahiz'

@app.route('/form')
def index():
	return render_template('form.html')

@app.route('/users', methods=['POST'])
def create_user():
    print("Got Post Info")
    print(request.form)
    session['name_from_form'] = request.form['name']
    session['email_from_form'] = request.form['email']
    return redirect('show')

@app.route("/show")
def show_user():
    print("Showing the User Info From the Form")
    print(request.form)
    print("yo"*50)
    return render_template("show.html")


if __name__ == '__main__':
	app.run(debug = True)