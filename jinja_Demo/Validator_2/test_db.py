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

	#This is the database connection details below 
app.config['MYSQL_HOST'] = '0.0.0.0'; # The ip address of the database
app.config['MYSQL_USER'] = 'dev'; #This is username with access to the database
app.config['MYSQL_PASSWORD'] ='dinero0123'; #This is the password of the username
app.config['MYSQL_DB'] = 'Platform_abacrop'; # The name of the database
	
	#Initialize MYSQl
mysql = MySQL(app);


cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

db_Msql.Update_Password(Email='louiscastro.abacrops@gmail.com', New_Password="test",cursor=cursor, mYSQL=mysql)