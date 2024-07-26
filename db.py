from sqlite3 import Connection, connect

def get_flights(conn: Connection):
    return conn.execute('''
    SELECT Flight.id, Plane.plane_code, departure_airport.name, arrival_airport.name, departure_time, arrival_time
    FROM Flight
    JOIN Plane ON Flight.plane_id = Plane.id
    JOIN Airport departure_airport ON Flight.departure_airport_id = departure_airport.id
    JOIN Airport arrival_airport ON Flight.arrival_airport_id = arrival_airport.id
    ''').fetchall()

def get_flight(conn: Connection, flight_id: int):
    return conn.execute('''
    SELECT Flight.id, Plane.id, departure_airport.name, arrival_airport.name, departure_time, arrival_time
    FROM Flight
    JOIN Plane ON Flight.plane_id = Plane.id
    JOIN Airport departure_airport ON Flight.departure_airport_id = departure_airport.id
    JOIN Airport arrival_airport ON Flight.arrival_airport_id = arrival_airport.id
    WHERE Flight.id = ?
    ''', (flight_id,)).fetchone()

def get_seats(conn: Connection, flight_id: int):
    return conn.execute('''
    SELECT row, column
    FROM Seat
    WHERE plane_id = (
        SELECT plane_id
        FROM Flight
        WHERE id = ?
    )
    ''', (flight_id,)).fetchall()

def book_seats(conn: Connection, flight_id: int, selected_seats: list):
    plane_id = conn.execute('''
    SELECT plane_id
    FROM Flight
    WHERE id = ?
    ''', (flight_id,)).fetchone()[0]
    for row, column in selected_seats:
        conn.execute('''
        INSERT INTO Booking (plane_id, row, column)
        VALUES (?, ?, ?)
        ''', (plane_id, row, column))
    conn.commit()

def get_bookings(conn: Connection, flight_id: int, user_id: int):
    return conn.execute('''
    SELECT row, column
    FROM Booking
    WHERE plane_id = (
        SELECT plane_id
        FROM Flight
        WHERE id = ?
    )
    AND user_id = ?
    ''', (flight_id, user_id)).fetchall()

def get_user_id(conn: Connection, username: str, password: str):
    return conn.execute('''
    SELECT id
    FROM User
    WHERE username = ?
    AND password = ?
    ''', (username, password)).fetchone()[0]

def register_user(conn: Connection, name: str, email: str, username: str, password: str):
    conn.execute('''
    INSERT INTO User (name, email, username, password)
    VALUES (?, ?, ?, ?)
    ''', (name, email, username, password))
    conn.commit()

def get_user_bookings(conn: Connection, user_id: int):
    return conn.execute('''
    SELECT row, column
    FROM Booking
    WHERE user_id = ?
    ''', (user_id,)).fetchall()

def login(conn: Connection, username: str, password: str):
    user_id = conn.execute('''
    SELECT id
    FROM User
    WHERE username = ?
    AND password = ?
    ''', (username, password)).fetchone() 
    print(user_id, username, password)
    if user_id is not None:
        return user_id
    else:
        return None
    
def get_users(conn: Connection, user_ids: list):
    return conn.execute('''
    SELECT name, email, username
    FROM User
    WHERE id IN ({})
    '''.format(', '.join('?' * len(user_ids))), user_ids).fetchall()