from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__)

app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def btn_detection():
    btn = False
    mess = 'email'
    if (request.method == "POST"):
        btn = True
        if (mess == 'email'):
            mess = True

        flash('Aqui va un mensaje', 'info')
        return render_template("index.html", btn=btn, mess=True)

    flash('2 Aqui va otro mensaje', 'info')
    return render_template('index.html', btn=btn, mess=False)


if __name__ == "__main__":

    app.run(host='127.0.0.1', port=909, debug=True)
