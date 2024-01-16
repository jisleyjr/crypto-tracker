from flask import Flask, jsonify
from mysql.connector import errorcode
from helpers import get_coins, get_context, get_current_positions

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

    return jsonify(coins)

@app.route('/positions', methods=['GET'])
def positions():
    cnx = get_context()
    positions = get_current_positions(cnx)
    cnx.close()

    return jsonify(positions)

if __name__ == '__main__':
    app.run(debug=True)