from flask import Flask, render_template, request, redirect, url_for, session
import re
from mail_config import get_config
from flask_mail import Mail, Message
from numpy import random
import sys
import mail_config



app = Flask(__name__)
app.secret_key= 'ke%$^#$y'


@app.route('/', methods=['GET', 'POST'])
def Send_Email():
	email='castrolwilliam@gmail.com'
	mail_config.send_recovery_key(email,app);
	print("Email Send\n")
	
	return "Email Send"

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
