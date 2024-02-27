from flask import Flask, jsonify
from mysql.connector import errorcode
from helpers import get_coins, get_context, get_current_positions, get_current_positions_for_coin, get_sales_by_year

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify(message="Hello, World!")

@app.route('/greet/<string:name>', methods=['GET'])
def greet(name):
    return jsonify(message=f"Hello, {name}!")

@app.route('/coins', methods=['GET'])
def coins():
    cnx = get_context()
    coins = get_coins(cnx)
    cnx.close()

    response = jsonify(coins)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/positions', methods=['GET'])
def positions():
    cnx = get_context()
    positions = get_current_positions(cnx)
    cnx.close()

    response = jsonify(positions)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/positions/<string:coin>', methods=['GET'])
def coin_positions(coin):
    cnx = get_context()
    positions = get_current_positions_for_coin(cnx, coin)
    cnx.close()

    response = jsonify(positions)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/sales/<int:year>', methods=['GET'])
def sales_by_year(year):
    if year < 2020:
        return jsonify(message="Year must be greater than 2020"), 400

    cnx = get_context()
    sales = get_sales_by_year(cnx, year)
    cnx.close()

    response = jsonify(sales)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True)