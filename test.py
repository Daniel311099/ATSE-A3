import sqlite3
from algorithm import Flight, Seat, Passenger

conn = sqlite3.connect('db.sqlite3')

flight = conn.execute('''
SELECT Flight.id, Plane.id, departure_airport.name, arrival_airport.name, departure_time, arrival_time
FROM Flight
JOIN Plane ON Flight.plane_id = Plane.id
JOIN Airport departure_airport ON Flight.departure_airport_id = departure_airport.id
JOIN Airport arrival_airport ON Flight.arrival_airport_id = arrival_airport.id
''').fetchone()

print(flight)
flight = Flight(*flight)
print(flight)

flight.populate_layout()
# print(flight.layout)
# flight.print_layout()

passengers = [
    {
        'name': 'Alice',
        'age': 14,
        'accept': True
    },
    {
        'name': 'Bob',
        'age': 30,
        'accept': True
    },
    {
        'name': 'Charlie',
        'age': 35,
        'accept': True
    },
    {
        'name': 'David',
        'age': 40,
        'accept': False
    },
    {
        'name': 'Eve',
        'age': 45,
        'accept': True
    },
    {
        'name': 'Frank',
        'age': 50,
        'accept': True
    },
]

passengers = [Passenger(**passenger) for passenger in passengers]
# print(passengers)

available = flight.get_available_seats(passengers[:1])
print([[seat.id_ for seat in seats] for seats in available])
option = available[0]
print([seat.id_ for seat in option])