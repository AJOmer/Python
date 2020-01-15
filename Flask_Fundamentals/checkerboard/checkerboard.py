from flask import Flask, render_template
app = Flask(__name__)
@app.route ('/')
def twoeight():
	return render_template('checkerboard.html', times= 4 ,bars = 4)


@app.route('/<x>')
def foureight(x):
	return render_template('checkerboard.html', times = int(x) ,bars = 4)

@app.route('/<x>/<y>')
def brokeserver(x,y):
	return render_template('checkerboard.html', times = int(x), bars=int(y))

@app.route('/<x>/<y>/<col1>/<col2>')
def colors(x,y,col1,col2):
	return render_template('checkerboard.html', times = int(x), bars=int(y), color1=col1, color2=col2)

if __name__=="__main__":  
  app.run(debug=True)