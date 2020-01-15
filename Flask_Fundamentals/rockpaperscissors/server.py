from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'secret key goes here'



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/rps', methods=['POST'])
def rps():
    session.clear()
    mylist = [0, 'rock', 'paper', 'scissors']
    myDict = {'rock': {'paper': 'you win!', 'scissors': 'you lose!'},
    'scissors': {'rock': 'you win!', 'paper': 'you lose!'},
    'paper': {'rock': 'you lose!', 'scissors': 'you win!'}
    }
    session['randnum'] = random.randint(1,3)
    session['mychoice'] = mylist[int(request.form['checker'])]
    session['compchoice'] = mylist[int(session['randnum'])]
    # print(request.form['checker'])
    if session['mychoice'] == session['compchoice']:
        session['results'] = 'you tied!'
        return redirect('/')
    session['results'] = myDict[mylist[int(session['randnum'])]][mylist[int(request.form['checker'])]]
    # print(session['results'])
    return redirect('/')


@app.route('/destroy_session')
def destroy():
    session.clear()
    return redirect("/")
    


if __name__=="__main__":
    app.run(debug=True)