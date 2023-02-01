from flask import Flask, render_template, request, redirect, url_for, session
import re
import sys 
import db_Msql
from flask_mysqldb import MySQL
import MySQLdb.cursors



# Initialize the mysql platform 
app = Flask(__name__)

app.secret_key = 'key'

# Initializing The handler for mysql 
mYSQL = db_Msql.Initialize_Msql(app)





#This function verifices the user account 
@app.route('/',  methods=['GET', 'POST'])
def Login():	
	msg = ''
	# Check for incoming POST Request from user trying to log-in 
	if (request.method == 'POST' and 'Email' in request.form and 'Password' in request.form):
		
		#Request the user { Email }  from website post  
		Email = request.form.get('Email'); 

		#Request the user { Password } from the website post 
		Password = request.form.get('Password')
		

		#Check if the account exist
		cursor = mYSQL.connection.cursor(MySQLdb.cursors.DictCursor)

		if(True == cursor.execute('SELECT * FROM Company WHERE Email = %s AND Password = %s', (Email,Password,)) ):

			account = cursor.fetchone();
			if account:
				session['loggedin'] = True
				session['id'] = account['company_id']
				session['employees'] = account['Amount_Employes']
				session['email'] = account['Email']
				session['password'] = account['Password']
				session['Company_Name'] = account['Name']
				#To be re-define
				session['Role'] = "Company"

				return redirect(url_for('Company/Administrator'))
	
	
	################################################################################################################
	# if The Credentials were not found in the company table then the program will look at the employee table      # 
	################################################################################################################			
		if(True == cursor.execute('SELECT * FROM Employees WHERE Email = %s AND Password = %s', (Email,Password,)) ):
			
			#Fetch the user information from the table 
			account = cursor.fetchone();
			
			if account: # account equals true then 

			#START WRITING THE SESSION FOR THIS USER  				
				
				#Return the the user Validation for successfully log-in
				session['loggedin'] = True
				
				#
				session['user_id'] = account["user_id"]
				
				session['company_id'] = account["company_id"]
				
				#This Function alocates the company name by id (for easy interaction)
				session['Company_Name'] = db_Msql.Get_company_name(session['company_id'], cursor)


				session['email'] = account['Email']
				
				session['password'] = account['Password']
				
				session['First_Name'] = account['First_name']
				
				session['Last_Name'] = account['Last_name']
				
				#To be re assing
				session['Role'] = "employe";

				return redirect(url_for('emp'))
		else: 
			# Account does not exist on any TABLE
				# (Company, Employees or SuperUser) 
			msg = "Incorrect username / password"
	
	return render_template('index.html', msg="")

######### DEMO ############################
# TEST FOR THE employe login
@app.route('/employe', methods=['GET', 'POST'])
def emp():
	fn = session['First_Name']
	ln = session['Last_Name']

	full_name = str(fn) + " " + str(ln)
	msg = str("Welcome, " + full_name)

	return render_template('/employe/Dashboard.html', UserName= full_name)

@app.route('/Company/Administrator', methods=['GET', 'POST'])
def comp():

	company_name = session['Company_Name']

	msg = str("Welcome, back " + company_name)
	
	return msg

#Run the application 
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=80, debug=True)



