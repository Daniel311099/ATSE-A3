import sqlite3

# Create a connection to the database
conn = sqlite3.connect('db.sqlite3')

# Create a User table
conn.execute('''
CREATE TABLE User (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
''')

# Create a Plane table
conn.execute('''
CREATE TABLE Plane (
    id INTEGER PRIMARY KEY,
    plane_code TEXT NOT NULL,
    name TEXT NOT NULL
);
''')

# Create an Airport table
conn.execute('''
CREATE TABLE Airport (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL
);
''')

# Create a Seat table
conn.execute('''
CREATE TABLE Seat (
    id INTEGER PRIMARY KEY,
    plane_id INTEGER NOT NULL,
    row INTEGER NOT NULL,
    column INTEGER NOT NULL,
    price REAL NOT NULL,
    locked BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (plane_id) REFERENCES Plane(id)
);
''')

# Create a Flight table
conn.execute('''
CREATE TABLE Flight (
    id INTEGER PRIMARY KEY,
    plane_id INTEGER NOT NULL,
    departure_airport_id INTEGER NOT NULL,
    arrival_airport_id INTEGER NOT NULL,
    departure_time TEXT NOT NULL,
    arrival_time TEXT NOT NULL,
    FOREIGN KEY (plane_id) REFERENCES Plane(id),
    FOREIGN KEY (departure_airport_id) REFERENCES Airport(id),
    FOREIGN KEY (arrival_airport_id) REFERENCES Airport(id)
);
''')

# Create a Booking table
conn.execute('''
CREATE TABLE Booking (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    flight_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (flight_id) REFERENCES Flight(id)
);
''')

# Create a booking seats table
conn.execute('''
CREATE TABLE BookingSeats (
    id INTEGER PRIMARY KEY,
    booking_id INTEGER NOT NULL,
    seat_id INTEGER NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES Booking(id),
    FOREIGN KEY (seat_id) REFERENCES Seat(id)
);
''')