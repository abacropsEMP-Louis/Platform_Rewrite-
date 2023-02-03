from flask import Flask, request, render_template, redirect, url_for, session
from flask_mail import Mail, Message
import re
import sys
import db_Msql
from flask_mysqldb import MySQL
import MySQLdb.cursors
from numpy import random
from os import getenv


app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
# Email address used to send the the email to the customers
app.config['MAIL_USERNAME'] = 'example@gmail.com'
# password of MAIL_PASSWORD
app.config['MAIL_PASSWORD'] = 'xxxx xxxx xxxx xxxx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail()

mail.init_app(app)


@app.route('/recovery_pw', methods=['POST', 'GET'])
def recovery():
    ''' Check if the the Email exist in the company DB or Employees DB'''
    if (request.method == 'POST' and 'Email'):

        Email = request.form.get('Email')

        cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)

        if (True == cursor.execute('SELECT * FROM Company WHERE Email = %s', (Email))):
            account = cursor.fetchone()
            if account:
                session['recovery_password'] = True
                session['email'] = account['Email']
                session['password'] = account['Password']
                session['Recovery_key'] = random.randint(1000000)

                send_auth_email(session['email'], session['Recovery_key'])

        if (True == cursor.execute('SELECT * FROM Employees WHERE Email = %s'), (Email)):
            account = cursor.fetchone()
            if account:
                session['recovery_password'] = True
                session['email'] = account['Email']
                session['password'] = account['Password']
                session['Recovery_key'] = random.randint(1000000)

                send_auth_email(session['email'], session['Recovery_key'])
            else:
                raise Exception("Sorry, the email you provide is not found")


def send_auth_email(email, Recovery_key):
    '''Send's the Recovery key in a passowrd in Email'''

    message = """
        (Max Length)
        ##################################
        Aqui se esta enviando el recovery 
        key.{}
          
    """.format(session[Recovery_key])
    msg = Message(
        'Platform Recovery Key',
        body=message,
        sender='confirmation.abacrops@gmail.com',
        recipients=[email]
    )
    mail.send(msg)
    return "Success"


def key_authentication():
    '''Verify if the key that the user gives matches with the original one'''


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)
