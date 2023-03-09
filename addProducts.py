from flask import Flask, render_template, request, redirect, flash, url_for, session
import db_Msql
from flask_mysqldb import MySQL
import MySQLdb.cursors


# Initialize the mysql platform
app = Flask(__name__)

app.secret_key = 'key'

# Initializing The handler for mysql
mYSQL = db_Msql.Initialize_Msql(app)


@app.route('/AddProduct', methods=['POST', 'GET'])
def add_product():
    """ This function adds a product to the database using the POST request data, and renders the Products.html template on completion."""

    if request.method == 'POST':

        name = request.form['Product.Name']
        brand = request.form['Product.Brand']
        classificationId = request.form['Product.ClassificationId']
        epa = request.form['Product.Epa']
        phi = request.form['Product.Phi']
        rei = request.form['Product.Rei']
        temperature = request.form['Product.TemperatureStorage']
        temperatureTypeId = request.form['Product.TemperatureTypeId']

        cursor = mYSQL.connection.cursor()
        cursor.execute("INSERT INTO Platform_abacrop.Products (Name, Brand, ClassificationId, EPA, PHI, REI, Temperature, TemperatureTypeId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (name, brand, classificationId, epa, phi, rei, temperature, temperatureTypeId))
        mYSQL.connection.commit()
        flash("Product Added")
        return render_template('Products.html')
    return render_template('base.html')


# def AddProduct():
#     ''''''
#     classification = 1  # get_product_classification()
#     if (classification == '1'):
#         return render_template('semillas.html')
#     elif (classification == '2'):
#         return render_template('fertilizantes.html')
#     elif (classification == '3'):
#         return render_template('control_de_plagas.html')
#     elif (classification == '4'):
#         return render_template('mantenimiento.html')
#     elif (classification == '5'):
#         return render_template('uso_humano.html')
#     else:
#         return render_template('base.html')
# def get_product_classification():
#     product_classification = request.form.get('Product_ClassificationId')
#     print(product_classification)
#     return product_classification
if __name__ == '__main__':
    app.run(debug=True, port=501, host='127.0.0.1')
