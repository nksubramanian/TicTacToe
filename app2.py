from flask import Flask, request, redirect, url_for


app2 = Flask(__name__)
positions = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

x = ['x', 'o']


@app2.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    y = x[0]
    if request.method == 'POST':
        if request.form.get('sub') == '00':
            positions[0][0] = y
        if request.form.get('sub') == '01':
            positions[0][1] = y
        if request.form.get('sub') == '02':
            positions[0][2] = y
        if request.form.get('sub') == '10':
            positions[1][0] = y
        if request.form.get('sub') == '11':
            positions[1][1] = y
        if request.form.get('sub') == '12':
            positions[1][2] = y
        if request.form.get('sub') == '20':
            positions[2][0] = y
        if request.form.get('sub') == '21':
            positions[2][1] = y
        if request.form.get('sub') == '22':
            positions[2][2] = y

    x.reverse()

    string1 = " "
    for i in range(0, 3):
        for j in range(0, 3):
            string1 = string1 + str(positions[i][j])
    return redirect(url_for("computation"))


@app2.route("/xxx")
def computation():

    top = '''
        <!DOCTYPE html>
            <html>
                <body>

                    <form method="post" action="http://localhost:5000/">
                            
        '''
    bottom = '''  
                    </form>
                </body>
            </html>
        '''

    middle = " "
    for i in range(0, 3):
        middle = middle+"<p>"
        for j in range(0, 3):
            if positions[i][j] == 0:

                middle = middle+'''<button name="sub" type="submit" value="%s">..</button>''' % (str(i)+str(j))
            else:
                middle = middle+'''<button type="submit"  disabled> %s</button>''' % (str(positions[i][j]))
        middle = middle + "</p>"

    return top+middle+bottom


app2.run()
