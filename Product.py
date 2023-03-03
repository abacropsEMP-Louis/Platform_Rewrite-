from flask import Flask, render_template, request, flash, redirect, url_for, session
import db_Msql
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

mYSQL = db_Msql.Initialize_Msql(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['POST', 'GET'])
def Products():
    """Function gets info from the DB and render it in Products.html table"""
    cursor = mYSQL.connection.cursor()
    cursor.execute('select * from Platform_abacrop.Products')
    # data == toda la data que esta almacenada en la base de datos.
    data = cursor.fetchall()
    print(data)
    return render_template('Products.html', products=data)


@app.route('/EditProduct/<string:id>', methods=['POST', 'GET'])
def EditProduct(id):
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
        cursor.execute("""
               UPDATE Platform_abacrop.Products SET
               Name = %s, 
               Brand = %s, 
               ClassificationId = %s, 
               EPA = %s, 
               PHI = %s,
               REI = %s, 
               Temperature = %s, 
               TemperatureTypeId = %s
               WHERE productId = %s
               """, (name, brand, classificationId, epa, phi, rei, temperature, temperatureTypeId, id))
        mYSQL.connection.commit()
        flash("Product deleted")
        return Products()
    return render_template('ProductEdit.html')


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
        return Products()
    # El html que estoy usando para agregar los producto se llama base
    # Products.html por algun motivo no me renderiza el CSS.
    return render_template('AddProduct.html')


if __name__ == "__main__":
    app.run(port=5010, host='127.0.0.1', debug=True)
