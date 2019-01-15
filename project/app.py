from flask import Flask
from flask import render_template
from flask import request
import logging
import pymongo


app = Flask(__name__)
app.logger.setLevel( logging.DEBUG )


@app.route( '/', methods=[ 'GET', 'POST' ] )
def home():
    if request.method == 'POST':
        store_customer(
            request.form[ 'email' ],
            request.form[ 'first_name' ],
            request.form[ 'last_name' ],
            request.form[ 'address' ],
            request.form[ 'city' ],
            request.form[ 'zip_code' ]
        )

    customers = get_customers()

    return render_template( 'home.html', customers=customers )


@app.route( '/clear-customers', methods=[ 'POST' ] )
def clear_customers():
    clear_all_customers()
    customers = get_customers()

    return render_template( 'home.html', customers=customers )
    


def get_database():
    database_connection = pymongo.MongoClient( 'keybright-test-mongodb' )
    
    return database_connection.keybright


def store_customer(
        _email,
        _first_name,
        _last_name,
        _address,
        _city,
        _zip_code
    ):

    database = get_database()

    document = {
        'email': _email,
        'first_name': _first_name,
        'last_name': _last_name,
        'address': _address,
        'city': _city,
        'zip_code': _zip_code
    }
    
    update_result = database.customers.update(
        document,
        {
            "$set": document,
        },
        upsert = True
    )


def get_customers():
    database = get_database()
    
    customers = []
    results = database.customers.find()
    for result in results:
        customer = {
            'email': result[ 'email' ],
            'first_name': result[ 'first_name' ],
            'last_name': result[ 'last_name' ],
            'address': result[ 'address' ],
            'city': result[ 'city' ],
            'zip_code': result[ 'zip_code' ]
        }
    
        customers.append( customer )
    
    return customers


def clear_all_customers():
    database = get_database()
    database.customers.remove( {} )


if __name__ == "__main__":
    app.run( host="0.0.0.0", debug=True )
