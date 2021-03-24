from flask import Flask, render_template, request, redirect, url_for


app2 = Flask(__name__)
positions = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

x = [1, 2]


@app2.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    y = x[0]
    if request.method == 'POST':
        if request.form.get('00') == '00':
            positions[0][0] = y
        if request.form.get('01') == '01':
            positions[0][1] = y
        if request.form.get('02') == '02':
            positions[0][2] = y
        if request.form.get('10') == '10':
            positions[1][0] = y
        if request.form.get('11') == '11':
            positions[1][1] = y
        if request.form.get('12') == '12':
            positions[1][2] = y
        if request.form.get('20') == '20':
            positions[2][0] = y
        if request.form.get('21') == '21':
            positions[2][1] = y
        if request.form.get('22') == '22':
            positions[2][2] = y

    x.reverse()

    string1 = " "
    for i in range(0, 3):
        for j in range(0, 3):
            string1 = string1 + str(positions[i][j])
    return redirect(url_for("computation"))


@app2.route("/x")
def front_page():
    return render_template("index.html")


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
                middle = middle+'''<input type="submit" value="%s" name="%s"/>''' % (str(i)+str(j), str(i)+str(j))
            else:
                middle = middle+'''<input type="submit" value="%s"  disabled/> ''' % (str(positions[i][j]))
        middle = middle + "</p>"

    return top+middle+bottom


app2.run()
