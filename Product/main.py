from flask import Flask, render_template, request, redirect, url_for, session
import re
import sys 

# Initialize the mysql platform 
app = Flask(__name__)

app.secret_key = 'key'





@app.route('/', methods=['GET', 'POST'])
def products():
    msg = False
    test = ""
    value = request.form.get('Classification')

    # Option for the dropdown 
    if (value == "1"):
        msg = True
        test = "Semillas"
        return render_template('submit_Auto.html', msg= msg, test=test)
 
    return render_template('submit_Auto.html', msg= msg)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port= 80, debug=True)
