from flask import Flask, redirect, url_for, request
app = Flask(__name__)


@app.route('/success/<int:name>')
def success(name):
    str1 ='''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    .button {
      border: none;
      color: white;
      padding: 16px 32px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 16px;
      margin: 4px 2px;
      transition-duration: 0.4s;
      cursor: pointer;
    }
    </style>
    </head>
    <body>
    
    '''
    if name == 1:
        str1 = str1 + "<button class='button button1'>Green</button></body?</html>"
    if name == 2:
        str1 = str1 + "<button class='button button1'>Yellow</button></body?</html>"

    return str1


@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success', name=int(user)))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success', name=int(user)))


if __name__ == '__main__':
   app.run(debug = True)