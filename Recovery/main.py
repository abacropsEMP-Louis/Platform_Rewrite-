from flask import Flask, render_template, request, redirect, url_for, session
import re
from mail_config import get_config
from flask_mail import Mail, Message
from numpy import random
import sys
import db_Msql
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'key'


# Initializing The handler for mysql
mYSQL = db_Msql.Initialize_Msql(app)


@app.route('/', methods=['GET', 'POST'])
def recovery_account():
    # This is the bool value that allows the user to enter the code
    account_found = False

    recovery_key_msg = False

    # this get the email from the website
    email = request.form.get('Email')
    # recovering access to the account
    input_recov = request.form.get('Recovery_key')
    random_Number = 0

    cursor = mYSQL.connection.cursor(MySQLdb.cursors.DictCursor)
    # If the email is in the database validate the (6 digit code input)
    if (db_Msql.Find_account_email(email, cursor, mYSQL) == True):

        session['recovery_password'] = True

        session['email'] = email

        # Tell The jinja that the account was fount
        account_found = True

        # Generate the 6 digit code and store it in session
        session['Recovery_key'] = random.randint(10000000)

        # Send the code to the email address
        print("Sending Code to " + str(email) +
              " " + str(session['Recovery_key']))

    if (session['Recovery_key'] == input_recov):
        recovery_key_msg = True
        print("Recovery key is same")

    else:
        # return alert of failed to find account
        print("not")

    return render_template('index.html', account_found=account_found, email=email, recovery_key_msg=recovery_key_msg)


########## TEST The Code ######################
def send_auth_email(email):
    '''Send's the Recovery key in a passowrd in Email'''
    get_config(app)
    message = """ (Max Length)
        ##################################
        Aqui se esta enviando el recovery 
        key.{}    
    """.format(session['Recovery_key'])

    msg = Message(
        'Platform Recovery Key',
        body=message,
        sender='confirmation.abacrops@gmail.com',
        recipients=[email])
    Mail.send(msg)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)
