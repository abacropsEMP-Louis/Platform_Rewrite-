import MySQLdb.cursors
from flask_mysqldb import MySQL


# This function intialize the mysql function 
def Initialize_Msql(app):

	#This is the database connection details below 
	app.config['MYSQL_HOST'] = 'localhost'; # The ip address of the database
	app.config['MYSQL_USER'] = 'dev'; #This is username with access to the database
	app.config['MYSQL_PASSWORD'] ='dinero0123'; #This is the password of the username
	app.config['MYSQL_DB'] = 'Platform_abacrop'; # The name of the database
	
	#Initialize MYSQl
	mysql = MySQL(app);
	
	return mysql; 


#This function extract company information from the company table by company id 

def Company_by_id(id, cursor):
	#Allocated memory for the company information (TYPE: ARRAY OR LIST )
	Company = []

	#cursor Execute command in mysql Defition of the command: 
	# "select from Company.company_id if found return all the data in that row."
	cursor.execute('SELECT * FROM Company WHERE company_id = %s', (id,))

	# get data from cursor.Company.* 
	Company = cursor.fetchone()

	#Return the company data to caller;
	return Company;

#################################################
#  This fuction extract company name from array	#
#################################################
def Get_company_name(id, cursor):
	
	#Extract the company name from the dictionary
	Company_info = Company_by_id(id, cursor)
	
	#return the company name
	return Company_info['Name']



#This function looks for a account in the database and returns a (BOOL VALUE)
def Find_account_email(Email, cursor, mYSQL):
	if(True == cursor.execute('SELECT * FROM Employees WHERE Email = %s', (Email,)) ):
	#Write command to mysql this command writes to the Employees.table
		return True
		
	if(True == cursor.execute('SELECT * FROM Company WHERE Email = %s', (Email,)) ):
		return True

	return False


#IF Change needed to any account password this is the function to call
#Change the account by email
def Update_Password(Email, New_Password, cursor, mYSQL):

	if(True == cursor.execute('SELECT * FROM Employees WHERE Email = %s', (Email,)) ):
		#Write command to mysql this command writes to the Employees.table
		cursor.execute('UPDATE Employees set Password = %s WHERE Email = %s', (New_Password, Email,))
		#Commit the execute command
		mYSQL.connection.commit()

	if(True == cursor.execute('SELECT * FROM Company WHERE Email = %s', (Email,)) ):
		# Write command to mysql This command writes to the company.table
		cursor.execute('UPDATE Company set Password = %s WHERE Email = %s', (New_Password, Email,))
		#Commit the execute command
		mYSQL.connection.commit()



###########################################################################
#                            PRODUCTS SECTION                             #
###########################################################################


def Create_product(cursor, mYSQL, company_id, classification_id,   Brand, Name, PHI, REI ,EPA, temp_type, temp):




		command = """  INSERT INTO Create_Products 
		(company_id, classification_id, product_id, Brand, Name, EPA, PHI, REI, Temp_Type, Temp) 
		values  (%s, %s, %s, %s, %s, %s, %s, %s, %s ,%s ); """

		product_id = generate_product_id(company_id=company_id, cursor=cursor)
#                
		Values = (company_id, classification_id, product_id, Brand ,Name, EPA, PHI , REI, temp_type , temp,)


		cursor.execute(command, Values)
		mYSQL.connection.commit()
		

#Read products from mysql (By company id )
def Get_product(cursor, mYSQL, company_id):
	#write command to mysql 
	cursor.execute('SELECT * FROM Create_Products WHERE company_id= %s', (company_id) )
	#Fetch all data 
	data = cursor.fetchall()
	# Close the connection
	mYSQL.connection.commit()
	
	#return the data 
	return data



#This function create new product id 
#the product id is classification for (NAME AND BRAND )
def generate_product_id(company_id, cursor):

# Product list under company_id 
	Products = []

	cursor.execute('SELECT * FROM Create_Products WHERE company_id= %s', (company_id,))


	Products = cursor.fetchall();

	#if There is now product created under this table 
	if(len(Products) == (0)):
	# then the value return will  be 1 
		new_lot = 1


	else:
		for t in Products:

		# Await for the last value 
			last_product = t

		#Get the last lot_id Convert the value into a integer  & add 1
		new_lot =  1 + int(last_product['product_id'])



	#Return the value to the CALLER
	return new_lot;



#REDIFINE THIS FOR LOT TABLE 
	
#This function create new  lot_id under the  company 
def Create_lot_id(company_id, cursor):
#	Products list for the mysql lib
	Products = []

	#From the table Product extract only from were the company_id is the same
	cursor.execute('SELECT * FROM Products WHERE company_id = %s', (company_id,))

	#Extract all values belonging to the company_id
	Products = cursor.fetchall()
	

	#if There is now product created under this table 
	if(len(Products) == (0)):
	# then the value return will  be 1 
		new_lot = 1


	else:
		for t in Products:

		# Await for the last value 
			last_product = t

		#Get the last lot_id Convert the value into a integer  & add 1
		new_lot =  1 + int(last_product['Lot_id'])



	#Return the value to the CALLER
	return new_lot;
