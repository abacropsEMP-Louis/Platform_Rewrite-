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




######### PRODUCTS SECTION ############


#######################################
#		  Find Lot_by_id              #
#######################################

def find_lot_by_company(company_id, cursor):
	cursor.execute('SELECT * FROM Products WHERE company_id = %s' , (company_id, ))

	company_LOTS = cursor.fetchall()

	print( str(company_LOTS[0]))
#######################################
#		  Find Lot_by_id              #
#######################################




def add_product(Lot_id,Name,Brand,product_id, company_id, EPA,PHI,REI, Temp_type, Temp ,cursor, mYSQL):
	#auto Generate Lot_id
	#
	#Lot_id =''

	#product id Definition 
	# product 1 (semillas)
	# product 2 (fertilizantes)
	# product 3 (Control de plagas)
	# product 4 (Insumos de mantenimiento)
	# product 5 (Uso humano)

	cursor.execute("INSERT INTO Platform_abacrop.Products (Lot_id, company_id, product_id, Name, Brand, EPA, PHI, REI, Temperature, TemperatureTypeId) VALUES (%s, %s, %s, %s,     %s,  %s,  %s,  %s, %s)", (Lot_id, company_id, product_id, Name, Brand, EPA, PHI, REI, Temp_type, Temp))
	mYSQL.connection.commit()
######### PRODUCTS SECTION ############
