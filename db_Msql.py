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

	


