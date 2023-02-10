from flask import Flask, render_template, request, redirect, url_for, session
import re
from flask_mail import Mail, Message
from numpy import random
import sys 
import db_Msql
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mail_config


app = Flask(__name__)
app.secret_key = '%$^$TGSGFB'

#Initializing the Handler for mysql

mYSQL = db_Msql.Initialize_Msql(app)

email = "louiscastro.abacrops@gmail.com"


@app.route('/', methods=['GET', 'Post'])
def New_password():

    #Define the mysql Cursor
    cursor = mYSQL.connection.cursor(MySQLdb.cursors.DictCursor)


    first_password = request.form.get('Password1')
    second_password = request.form.get('Password2')
    if (first_password == second_password):
        db_Msql.Update_Password(email, New_Password=first_password, )

    else:
        #alert 
        print("Error")
    return render_template('New_password.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)