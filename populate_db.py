import sqlite3
from typing import TypedDict, List

conn = sqlite3.connect('db.sqlite3')

User = TypedDict('User', {'id': int, 'name': str, 'email': str, 'username': str, 'password': str})
plane = TypedDict('Plane', {'id': int, 'plane_code': str, 'name': str})
Seat = TypedDict('Seat', {'id': int, 'plane_id': int, 'row': int, 'column': int})
Airport = TypedDict('Airport', {'id': int, 'name': str, 'city': str, 'country': str})
Flight = TypedDict('Flight', {'id': int, 'plane_id': int, 'departure_airport_id': int, 'arrival_airport_id': int, 'departure_time': str, 'arrival_time': str})
Booking = TypedDict('Booking', {'id': int, 'flight_id': int, 'user_id': int, 'seat_id': int})



users: List[User] = [
    {'name': 'Alice', 'email': 'alice@gmail.com', 'date_of_birth': '01-12-2000', 'username': 'alice101', 'password': 'password1'},
    {'name': 'Bob', 'email': 'bob@gmail.com', 'date_of_birth': '01-12-2010', 'username': 'bob202', 'password': 'password2'},
    {'name': 'Charlie', 'email': 'charlie@gmail.com', 'date_of_birth': '31-10-1999', 'username': 'charlie303', 'password': 'password3'}
]

planes = [
    {'plane_code': 'A1', 'name': 'Boeing 747'},
    {'plane_code': 'B2', 'name': 'Airbus A380'},
    {'plane_code': 'C3', 'name': 'Boeing 777'}
]

airports = [
    {'name': 'San Francisco International Airport', 'city': 'San Francisco', 'country': 'United States'},
    {'name': 'Los Angeles International Airport', 'city': 'Los Angeles', 'country': 'United States'},
    {'name': 'John F. Kennedy International Airport', 'city': 'New York City', 'country': 'United States'}
]

plane_layout = [[0] * 6 for _ in range(30)]
seats = [
    {'plane_code': 'A1', 'row': i, 'column': j, 'price': 100}
    for i in range(30)
    for j in range(6)
] + [
    {'plane_code': 'B2', 'row': i, 'column': j, 'price': 200}
    for i in range(30)
    for j in range(6)
] + [
    {'plane_code': 'C3', 'row': i, 'column': j, 'price': 300}
    for i in range(30)
    for j in range(6)
]

flights = [
    {'plane_code': 'A1', 'departure_airport': 'San Francisco International Airport', 'arrival_airport': 'Los Angeles International Airport', 'departure_time': '2021-07-01 08:00:00', 'arrival_time': '2021-07-01 09:30:00'},
    {'plane_code': 'B2', 'departure_airport': 'Los Angeles International Airport', 'arrival_airport': 'John F. Kennedy International Airport', 'departure_time': '2021-07-01 10:00:00', 'arrival_time': '2021-07-01 13:00:00'},
    {'plane_code': 'C3', 'departure_airport': 'John F. Kennedy International Airport', 'arrival_airport': 'San Francisco International Airport', 'departure_time': '2021-07-01 14:00:00', 'arrival_time': '2021-07-01 17:00:00'}
]

def populate_users():
    conn.executemany('''
    INSERT INTO User (name, email, date_of_birth, username, password)
    VALUES (:name, :email, :date_of_birth, :username, :password)
    ''', users)

def populate_planes():
    conn.executemany('''
    INSERT INTO Plane (plane_code, name)
    VALUES (:plane_code, :name)
    ''', planes)

def populate_airports():
    conn.executemany('''
    INSERT INTO Airport (name, city, country)
    VALUES (:name, :city, :country)
    ''', airports)

def populate_seats():
    # Get plane IDs and airport IDs from the database
    plane_ids = conn.execute('''
    SELECT id, plane_code FROM Plane
    ''')

    plane_ids = {plane_code: id for id, plane_code in plane_ids}

    for plane in seats:
        conn.execute('''
        INSERT INTO Seat (plane_id, row, column, price)
        VALUES (?, ?, ?, ?)
        ''', (plane_ids[plane['plane_code']], plane['row'], plane['column'], plane['price']))

def populate_flights():
    # Get plane IDs
   
    plane_ids = conn.execute('''
    SELECT id, plane_code FROM Plane
    ''')
    plane_ids = {plane_code: id for id, plane_code in plane_ids}
    # Get airport IDs
    airport_ids = conn.execute('''
    SELECT id, name FROM Airport
    ''')
    airport_ids = {name: id for id, name in airport_ids}
    # Insert flight data
    for flight in flights:
        conn.execute('''
        INSERT INTO Flight (plane_id, departure_airport_id, arrival_airport_id, departure_time, arrival_time)
        VALUES (?, ?, ?, ?, ?)
        ''', (plane_ids[flight['plane_code']], airport_ids[flight['departure_airport']], airport_ids[flight['arrival_airport']], flight['departure_time'], flight['arrival_time']))

def main():
    populate_users()
    populate_planes()
    populate_airports()
    conn.commit()
    populate_seats()
    populate_flights()
    conn.commit()

if __name__ == '__main__':
    main()