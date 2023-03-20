from flask import Flask, render_template, request, redirect, url_for, session
import re
import sys 
import db_Msql
from flask_mysqldb import MySQL
import MySQLdb.cursors
from numpy import random
import mail_config
from datetime import datetime

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
		test

		#Check if the account exist
		cursor = mYSQL.connection.cursor(MySQLdb.cursors.DictCursor)

		if(True == cursor.execute('SELECT * FROM Company WHERE Email = %s AND Password = %s', (Email,Password,)) ):

			account = cursor.fetchone();
			if account:
				session['loggedin'] = True
				session['company_id'] = account['company_id']
				session['employees'] = account['Amount_Employes']
				session['email'] = account['Email']
				session['password'] = account['Password']
				session['Company_Name'] = account['Name']
				#To be re-define
				session['Role'] = "Company"

				return redirect('Dashboard')
	
	
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
                                
				return redirect('Dashboard')

				
		else: 
			# Account does not exist on any TABLE
				# (Company, Employees or SuperUser) 
			msg = "Incorrect username / password"
	
	return render_template('index.html', msg="")

@app.route('/Home/Logout')
def Log_out():

	return render_template('index.html')



#This is for the admin dashboard
@app.route('/Admin', methods=['Get', 'POST'])
def administrator():
     


    return render_template('admin.html')

############ Products List ################

@app.route('/Products', methods=['GET', 'POST'])
def Products():
    cursor = mYSQL.connection.cursor(MySQLdb.cursors.DictCursor)
    
    data = db_Msql.Get_product(cursor=cursor, mYSQL=mYSQL, company_id=str(session['company_id']))
    return render_template('Products.html', User_Name = session['Company_Name'], Company_name=session['Company_Name'], products=data)


@app.route('/AddLot', methods=['GET', 'POST'] )
def AddLot():

    if (request.method == "POST"):
        cursor = mYSQL.connection.cursor(MySQLdb.cursors.DictCursor)
        Product_Amount = request.form.get('Product_QTY_Amount')
        Measurement_id = request.form.get('Product_QTY_Measurement')
        Product_price = request.form.get('Product_QTY_Price')
        product_Lot_Number = request.form.get('Product_LOT_Number')

        date_time = datetime.now()
        created_at = date_time.strftime("%m/%d/%Y")
        print(product_Lot_Number)
#        db_Msql.Create_Lot(cursor=cursor, mYSQL=mYSQL, Product_Name='TEST NAME' ,company_id=session['company_id'],classification_id='1', product_id='1', qty=Product_Amount, measurement_id=Measurement_id, price=Product_price, created_at=created_at)

    return render_template('AddLot.html', User_Name=session['Company_Name'], Product_Name="Product Name Example")



############# Add New Product ##################
@app.route('/AddProduct', methods=['GET', 'POST'])
def AddProducts():
    if (session['Role'] == 'Company'):
        if (request.method == "POST"):
            print("Method Request")
            #EXTRACT DATA FROM TEMPLATE 
        
        ###############################################
        
            # requesting ( NAME & BRAND )
            Product_Name = request.form.get('Product_Name')
            Brand_Name =  request.form.get('Product_Brand')
            
            # requesting ( EPA | PHI | REI )
            EPA = request.form.get('Product.Epa')
            PHI = request.form.get('Product.Phi')
            REI = request.form.get('Product.Rei')

            # requesting (Tempeture | Mesurment )
            Storage_temp = request.form.get('Product.TemperatureStorage')
            Mesurment_temp = request.form.get('Product.TemperatureTypeId')

            # Product classification
            clasification_value = request.form.get('Classification')

            # Validate the DATA 

            #validate input to write it to databases;
            #if the len of PHI is equal to 0 the value goes null 
            if (len(PHI) == 0):
                PHI = None; 


        # if the len of REI is Equal to 0 the value goes null
            if (len(REI) == 0):
                REI = None;

            if (len(EPA) == 0 ):
                EPA =None


        #if Storage tempeture (int) == 0 value goes nul 
            if (len(Storage_temp) == 0 ):
                Storage_temp = None;
                Mesurment_temp = None;



    #Write data to databases
            cursor = mYSQL.connection.cursor(MySQLdb.cursors.DictCursor)


            db_Msql.Create_product(cursor=cursor, mYSQL=mYSQL, company_id=str(session['company_id']) ,  classification_id=clasification_value, Brand=Brand_Name, Name=Product_Name, PHI=PHI, REI=REI, EPA=EPA, temp_type=Mesurment_temp, temp=Storage_temp)


            return redirect(url_for('Products'))
    
        return render_template('AddProduct.html')

############# AddProduct ##################



############## Product ####################


#This function go to dashboard
@app.route('/Dashboard', methods=['GET', 'POST'])
def Dashboard():

    if (session['loggedin'] == True):
        name = ""
        company_msg = False 
        if (session['Role'] == "Company"):
            
            company_msg = True
            name = session['Company_Name']


        if (session['Role'] == "employe"):
            # full name of user             
            name = (session['First_Name'] + " " + session['Last_Name'])

            company_msg = False

        return render_template('Dashboard.html', company_msg= company_msg, username=name)




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



