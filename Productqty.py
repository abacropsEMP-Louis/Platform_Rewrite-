from flask import Flask, render_template, request, flash, redirect, url_for, session
import db_Msql
from datetime import datetime


app = Flask(__name__)

mYSQL = db_Msql.Initialize_Msql(app)


@app.route('/', methods=['POST', 'GET'])
def process_product():
    """ Function that retirves the Products qty info """

    if request.method == "POST":

        # Product qty amout
        product_qty = request.form['ProductQuantity.Amount']
        # Mesurement (oz., gr., etc)
        measurement_id = request.form['ProductQuantity.MeasurementId']
        # $$$
        product_price = request.form['ProductQuantity.Price']
        date_time = datetime.now()
        created_at = date_time.strftime("%m/%d/%Y, %H:%M:%S")
        # mm/dd/YY H:M:S format
        print(product_qty)
        print(measurement_id)
        print(product_price)
        print(created_at)

        # cursor = mYSQL.connection.cursor()
        # cursor.execute("INSERT INTO Platform_abacrop.Add_Lot (qty, measurement_id, price, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        #                (product_qty, measurement_id, product_price))
        # mYSQL.connection.commit()

    # Aquí podríamos hacer algo con los datos
    return render_template('AddProductqty.html')


if __name__ == "__main__":
    app.run(port=234, host="127.0.0.0", debug=True)
