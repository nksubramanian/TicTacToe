from flask import Flask, redirect, url_for

app3 = Flask(__name__)


@app3.route("/<x>")
def front_page(x):
    return x


@app3.route("/home")
def home():
    return redirect(url_for('front_page', x="I am redirected"))




app3.run()
