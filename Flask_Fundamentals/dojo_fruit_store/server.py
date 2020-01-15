from flask import Flask, render_template, request, redirect
import datetime
app = Flask(__name__)  

@app.route('/')         
def index():
    return render_template("index.html")

@app.route('/checkout', methods=['POST'])         
def checkout():
    print(request.form)
    print('*'*80)
    first = request.form['first_name']
    last = request.form['last_name']
    student= request.form['student_id']
    strawb = request.form['strawberry']
    rasp = request.form['raspberry']
    appl = request.form['apple']
    blacc = request.form['blackberry']
    # date = datetime.datetime.now()
    currentDT = datetime.datetime.now()
    sum_fruits = int(request.form['strawberry'])+int(request.form['raspberry'])+int(request.form['apple'])+ int(request.form['blackberry'])
    # count = request.form[int('strawberry'), int('raspberry'), int('apple')]
    return render_template("checkout.html", dated=currentDT, firstname = first, lastname = last, student = student, strawbnum= strawb, raspnum = rasp, applenum=appl, blacknum=blacc, x= sum_fruits )

@app.route('/fruits')         
def fruits():
    return render_template("fruits.html")

if __name__=="__main__":   
    app.run(debug=True)    