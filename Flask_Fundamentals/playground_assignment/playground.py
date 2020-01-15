from flask import Flask, render_template
app = Flask(__name__)
@app.route('/play')
def level_1():
    return render_template('playground.html',times=3)



@app.route('/play/<x>')
def level_2(x):
	return render_template('playground.html',times= int(x))



@app.route('/play/<x>/<color>')
def level_3(x, color):
    return render_template('playground.html',times=int(x),background=color)


if __name__=="__main__":
    app.run(debug=True)
