from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def btn_detection():
	btn=False
	mess='email'
	if (request.method == "POST"):
		btn = True
		if (mess == 'email'):
			mess = True
		
		return render_template("index.html", btn=btn, mess=True)

	return render_template('index.html', btn=btn, mess=False)
if __name__ == "__main__":

	app.run(host='127.0.0.1', port=80, debug=True)
