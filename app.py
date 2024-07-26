from flask import Flask, request, jsonify, render_template
import sqlite3
# add cors to allow cross origin requests
from flask_cors import CORS

from db import (
    get_seats as get_seats_db,
    book_seats as book_seats_db,
    login as login_db,
    register_user as register_user_db,
    get_flight,
    get_users,
    get_flights as get_flights_db
)

from algorithm import Flight, Seat, Passenger

app = Flask(__name__)
CORS(app)


# Sample users
users = {
    "user1": "password1",
    "user2": "password2"
}

# Sample seat map
seats = [0] * 30


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    connection = sqlite3.connect('db.sqlite3')

    user_id = login_db(connection, username, password)
    print(user_id)
    if user_id:
        return jsonify({
            'status': 'success',
            'user_id': user_id
        })
    else:
        return jsonify({"status": "failure"}), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    email = data['email']
    username = data['username']
    password = data['password']
    connection = sqlite3.connect('db.sqlite3')

    register_user_db(connection, name, email, username, password)
    return jsonify({"status": "success"})


@app.route('/flights', methods=['GET'])
def get_flights():
    connection = sqlite3.connect('db.sqlite3')
    flights = get_flights_db(connection)
    return jsonify(flights)


@app.route('/seats/<int:flight_id>', methods=['GET'])
def get_seats(flight_id):
    connection = sqlite3.connect('db.sqlite3')
    passenger_ids = request.args.getlist('passenger_ids')
    passengers = get_users(connection, passenger_ids)

    flight = get_flight(connection, flight_id)
    flight = Flight(*flight)
    flight.populate_layout()

    seats = flight.get_available_seats(passengers)
    seats = flight.rank_options(passengers=passengers, seat_list=seats)
    options = []
    for seat in seats:
        option = []
        for row in seat:
            option.append({
                'id': row.id_,
                'row': row.row,
                'column': row.column,
                'price': row.price
            
            })
        options.append(option)
    j = jsonify(options[:10])
    return j


@app.route('/book', methods=['POST'])
def book_seats():
    data = request.json
    selected_seats = data['selectedSeats']
    print(selected_seats)
    for seat in selected_seats:
        if seats[seat] == 0:
            seats[seat] = 1
        else:
            return jsonify({"status": "failure"}), 400
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(debug=True)
