from flask import Flask, render_template, request, redirect, url_for, session, flash
import re
from flask_mail import Mail, Message
from numpy import random
import sys
from flask_mysqldb import MySQL
import MySQLdb.cursors

import db_Msql
import mail_config


app = Flask(__name__)
app.config["SECRET_KEY"] = '%$^$uujfjjfgjfjfhjghk,nbv,TGSGFB'

mYSQL = db_Msql.Initialize_Msql(app)


@app.route('/', methods=['GET', 'POST'])
def find_email():

    error_email = True
    # DESTROY ANY existing session
    session.clear()
    # This variable change if the email is found under a account
    session['account'] = False

    # Defining the mysql Cursor
    cursor = mYSQL.connection.cursor(MySQLdb.cursors.DictCursor)

    # Request email from website template
    email = request.form.get('Email')

    # if the email enter by user is in the database the allow the user to await for recovery password
    if (db_Msql.Find_account_email(email, cursor, MySQL) == True):

        # store the random generated key 6 random numbers
        generate_key = random.randint(1000000)

        # Create the session for the user
        session["loggedin"] = False
        session["email"] = email
        session["generate"] = generate_key
        session['account'] = True

        # Email user the recovery key
        mail_config.send_recovery_key(email, app, generate_key)

        return redirect(url_for('Validate_email'))
    else:
        # Flash there is no account under this email
        error_email = False

    return render_template('validator.html')


@app.route('/validate_email', methods=['GET', 'POST'])
def Validate_email():
    print()
    if (str(request.form.get('key')) == str(session["generate"])):
        session['loggedin'] = True

        # Redirect to new password
        return redirect(url_for('New_password'))

    else:
        # flash message (The key not valide)
        flash(" Invalide key ")

    return render_template('validator_email.html', account_found=session["account"], email=str(session["email"]))


@app.route('/new_password', methods=['GET', 'POST'])
def New_password():
    pass1 = request.form.get('pass')
    pass2 = request.form.get('passw')
    if (session['loggedin'] == True):

        # Generate the mysql cursor
        cursor = mYSQL.connection.cursor(MySQLdb.cursors.DictCursor)

        print(pass1)
        if (pass1 != None):
            # If Both password are the same
            if (pass1 == pass2):

                print(pass1)
                print(pass2)
            # update the database
                db_Msql.Update_Password(session["email"], pass2, cursor, mYSQL)

                flash("Update successfully")
                session.clear()
        flash("Empty")
    else:
        # The password is inconsistant
        flash("Invalide user ")

    return render_template('New_password.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=787, debug=True)
