from flask import Flask, render_template, request, redirect, url_for, session
import re
import sys 
import db_Msql
from flask_mysqldb import MySQL
import MySQLdb.cursors
from numpy import random
import mail_config

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

				return redirect('Company/Admin')
	
	
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
				return redirect('Employe')

				
		else: 
			# Account does not exist on any TABLE
				# (Company, Employees or SuperUser) 
			msg = "Incorrect username / password"
	
	return render_template('index.html', msg="")

@app.route('/Home/Logout')
def Log_out():

	return render_template('index.html')

##############################
#Recovery of account
@app.route('/accounts', methods=['GET', 'POST']) 
def find_email():
    Email_locate = ""


    #DESTROY ANY existing session 
    session.clear()
    #This variable change if the email is found under a account
    session['account'] = False
    

    #Defining the mysql Cursor 
    cursor = mYSQL.connection.cursor(MySQLdb.cursors.DictCursor)

    #Request email from website template 
    email = request.form.get('Email')
    print(email)
    if (email != None):
    
        #if the email enter by user is in the database the allow the user to await for recovery password 
        if (db_Msql.Find_account_email(email, cursor, MySQL) == True):
            Email_locate = True
        
            #store the random generated key 6 random numbers
            generate_key = random.randint(1000000)

        
            #Create the session for the user
            session["loggedin"] = False
            session["email"] = email
            session["generate"] = generate_key
            session['account'] = True


        
            #Email user the recovery key
            mail_config.send_recovery_key(email, app, generate_key)

            return redirect(url_for('Validate_email'))
        
        elif(db_Msql.Find_account_email(email, cursor, MySQL) == False):
            Email_locate = False
            #Flash there is no account under this email 
            print("Email not in the database ")
            return render_template('Recovery/validator.html', Email_locate=Email_locate)
  
    return render_template('Recovery/validator.html')


@app.route('/validate_email', methods=['GET', 'POST'])
def Validate_email():
    Valid_code = True 
    key = request.form.get('key')
    if (key != None):
        if (str(key) == str(session["generate"])):
            session['loggedin'] = True


            #Redirect to new password 
            return redirect(url_for('New_password'))

        else:
            Valid_code = False
            #flash message (The key not valide)
            print(" Invalide key ")

    return render_template('Recovery/validator_email.html', account_found=session["account"], email= str(session["email"]), Valid_code=Valid_code) 

@app.route('/new_password', methods=['GET' , 'POST'])
def New_password():
    pass1 = request.form.get('pass')
    pass2 = request.form.get('passw')
    if (pass1 != None):
        if(pass2 != None):
            if (session['loggedin'] == True):

                #Generate the mysql cursor 
                cursor = mYSQL.connection.cursor(MySQLdb.cursors.DictCursor)

                print(pass1)
        
                #If Both password are the same 
                if (pass1 == pass2):
        
                    print(pass1)
                    print(pass2)
                    #update the database 
                    db_Msql.Update_Password(session["email"],pass2, cursor, mYSQL)
            
                    print("Update successfully")
                    session.clear()
                    return redirect(url_for('Login'))
                else:
                    return render_template('Recovery/New_password.html', pass_value= False)
                            
            return render_template('Recovery/New_password.html', pass_value= False)
    else:
        # The password is inconsistant
        print("Invalide user ")
    return render_template('Recovery/New_password.html', pass_value=True)
    



@app.route('/test')
def test():

    return render_template('test.html')

#Run the application 
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=80, debug=True)



