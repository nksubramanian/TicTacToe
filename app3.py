from flask import Flask, redirect, url_for, request, render_template
app3 = Flask(__name__)

x = "default"


@app3.route('/success')
def success():
    return x


@app3.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        global x
        x = user
        return redirect(url_for('success'))


@app3.route('/home')
def homepage():
    return render_template("exp.html")

app3.run()


class Person:

    def __init__(self, name="default"):
    self.name = name


