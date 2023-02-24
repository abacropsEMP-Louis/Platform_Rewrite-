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


# This function verifices the user account
@app.route('/',  methods=['GET', 'POST'])
def sign_in():
    """  """
    if request.method == 'POST':
        FirstName = request.form['FirstName']
        LastName = request.form['LastName']
        CompanyName = request.form['CompanyName']
        CompanyRole = request.form['CompanyRole']
        # City = request.form['City']
        # State = request.form['State']
        # Country = request.form['Country']
        # zip_code = request.form['zip_code']
        Email = request.form['Email']
        Password = request.form['Password']
        company_id = '12'
        Amount_Employes = '10'

        cursor = mYSQL.connection.cursor()
        cursor.execute("INSERT INTO Platform_abacrop.Company (FirstName, LastName, CompanyName, CompanyRole, Email, Password, company_id, Amount_Employes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (FirstName, LastName, CompanyName, CompanyRole, Email, Password, company_id, Amount_Employes))
        mYSQL.connection.commit()
        return redirect(url_for('dashboard'))
    return render_template('sign-up.html')


@app.route('/Dashboard')
def dashboard():
    return render_template('Dashboard.html')


if __name__ == '__main__':
    app.run(debug=True, port=862, host='127.0.0.1')
