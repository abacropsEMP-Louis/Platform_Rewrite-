from flask import Flask, render_template, request, redirect, url_for, session
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
def valid():
    #This variable change if the email is found under a account
    account_found = False
    

    session['generate'] = 0


    #Defining the mysql Cursor 
    cursor = mYSQL.connection.cursor(MySQLdb.cursors.DictCursor)

    #Request email from website template 
    email = request.form.get('Email')

    
    #if the email enter by user is in the database the allow the user to await for recovery password 
    if (db_Msql.Find_account_email(email, cursor, MySQL) == True):
        
        #store the random generated key 6 random numbers
        generate_key = random.randint(1000000)

        
        #Create the session for the user
        session["loggedin"] = False
        session["email"] = email
        session["generate"] = generate_key

        #Send bool value to website jinja 
        account_found = True



        
        #Email user the recovery key
        mail_config.send_recovery_key(email, app, generate_key)
    
    # if the request.form.get(input of user of the recovery key)
    # == the store string in session[Under generate] if This is true 
    #the link will be redirect
    ba= request.form.get('Recover_key')
    print(ba)
    print(session['generate'])
    if( str(session['generate']) == request.form.get('Recover_key')):
        
        
        #Send user to the new_password link 
        print("success")
        return redirect('/New_password')

    else:
        #Throw a message to the html that the code send does not match the input by user 
        print("error")


    return render_template('validator.html', account_found= account_found, email=email)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
