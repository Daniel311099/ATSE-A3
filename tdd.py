import unittest
import sqlite3
from algorithm import Passenger, Seat, Flight

class TestSeatAllocation(unittest.TestCase):
    
    def setUp(self):
        # Setting up database connection and fetching flight details
        self.conn = sqlite3.connect('db.sqlite3')
        flight_data = self.conn.execute('''
        SELECT Flight.id, Plane.id, departure_airport.name, arrival_airport.name, departure_time, arrival_time
        FROM Flight
        JOIN Plane ON Flight.plane_id = Plane.id
        JOIN Airport departure_airport ON Flight.departure_airport_id = departure_airport.id
        JOIN Airport arrival_airport ON Flight.arrival_airport_id = arrival_airport.id
        ''').fetchone()
        
        self.flight = Flight(*flight_data)
        self.flight.populate_layout()

        self.passengers = [
            Passenger(name='Alice', age=14, accept=True),
            Passenger(name='Bob', age=30, accept=True),
            Passenger(name='Charlie', age=35, accept=True),
            Passenger(name='David', age=40, accept=False),
            Passenger(name='Eve', age=45, accept=True),
            Passenger(name='Frank', age=50, accept=True),
        ]
    
    def test_single_seat_allocation(self):
        result = self.flight.get_available_seats([self.passengers[0]])
        self.assertTrue(result, "Failed to allocate a single seat")

    def test_pair_seat_allocation(self):
        result = self.flight.get_available_seats(self.passengers[:2])
        self.assertTrue(result, "Failed to allocate a pair of seats")

    def test_three_seat_allocation(self):
        result = self.flight.get_available_seats(self.passengers[:3])
        self.assertTrue(result, "Failed to allocate three seats together")

    def test_more_than_six_passengers(self):
        extra_passenger = Passenger(name='Grace', age=55, accept=True)
        passengers = self.passengers + [extra_passenger]
        result = self.flight.get_available_seats(passengers)
        self.assertEqual(result, [], "Should not allocate more than six passengers at once")

    def test_seat_allocation_near_fire_exit(self):
        passenger = self.passengers[3]
        result = self.flight.get_available_seats([passenger])
        for seat in result:
            if not passenger.accept:
                self.assertNotEqual(seat[0].row, self.flight.fire_row, "Allocated seat near fire exit for a passenger who does not accept it")
            else:
                self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
