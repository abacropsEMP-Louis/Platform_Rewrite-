#! /bin/bash

sudo apt-get update 

sudo apt-get upgrade 

sudo apt-get install mysql-server-8.0 

sudo mysql  -Bse "show Databases;"

#Create Databases 
sudo mysql -Bse "CREATE DATABASE IF NOT EXISTS Platform_abacrop; use Platform_abacrop;  SHOW TABLES; "

#Create The user for the database

sudo mysql -Bse "CREATE USER IF NOT EXISTS 'dev'@'%' IDENTIFIED BY 'dinero0123';GRANT ALL PRIVILEGES ON Platform_abacrop.* TO 'dev'@'%';"

#Creating tables of the databases
    #Creating superuser 
sudo mysql -Bse "use Platform_abacrop; CREATE TABLE IF NOT EXISTS SuperUser( id_su INT NOT NULL, Email VARCHAR(45) NOT NULL, Password VARCHAR(100) NOT NULL, PRIMARY KEY (id_su));"

    # Creating Company table
sudo mysql -Bse "use Platform_abacrop; CREATE TABLE IF NOT EXISTS Company( company_id int NOT NULL, Name varchar(45) NOT NULL, Tax_id varchar(15) DEFAULT NULL, Email varchar(45) NOT NULL, Password varchar(75) NOT NULL,Amount_Employes int NOT NULL,PRIMARY KEY (company_id, Name));"

# Creating Employees table 
sudo mysql -Bse "use Platform_abacrop; Create TABLE IF NOT EXISTS Employees(user_id INT PRIMARY KEY NOT NULL, company_id INT, First_name VARCHAR(45) NOT NULL, Last_name VARCHAR(45) NOT NULL, Email VARCHAR(100) NOT NULL, FOREIGN KEY (company_id) REFERENCES Company(company_id));"

# Creating Product table
sudo mysql -Bse "use Platform_abacrop; Create TABLE IF NOT EXISTS Create_Products( company_id INT NOT NULL,  classification_id INT NOT NULL, product_id INT NOT NULL, Brand  VARCHAR(25) NOT NULL, Name VARCHAR(25) NOT NULL, EPA VARCHAR(15) NULL,  PHI INT NULL, REI INT NULL,  Temp_Type VARCHAR(1) NULL, Temp INT NULL, 
 FOREIGN KEY (company_id) REFERENCES Company(company_id));"



# Product Lot  table 
sudo mysql -Bse "use Platform_abacrop; Create TABLE IF NOT  EXISTS Add_Lot (company_id INT NOT NULL, classification_id INT NOT NULL, product_id INT NOT NULL, 
    
    lot_id INT NOT NULL, qty INT NOT NULL, measurement_id INT NOT NULL, 
    
    price int NOT NULL,  created_at  varchar(10) NULL,
    
    FOREIGN KEY (company_id) REFERENCES Company(company_id) );"


# Report Product Report product 
sudo mysql -Bse "use Platform_abacrop; Create TABLE IF NOT EXISTS Report_Product(
    company_id INT NOT NULL,
    classification_id INT NOT NULL, 
    product_id INT NOT NULL,
    lot_id INT NOT NULL,
    Brand VARCHAR(25) ,
    Name VARCHAR(25),
    Amout INT NOT NULL,
    measurement_id INT NOT NULL,
    price int NOT NULL,
    created_at VARCHAR(10) NULL,
    ended_at VARCHAR(10) NULL,
    FOREIGN KEY (company_id) REFERENCES Company(company_id) );"

