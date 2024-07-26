import sqlite3
from typing import List, TypedDict
from itertools import combinations, product
from dataclasses import dataclass

@dataclass
class Passenger():
    # id: int
    age: int
    name: str
    accept: bool

@dataclass
class Seat():
    def __init__(self, id, plane_id, row, column, price, booked=False):
        self.id_ = id
        self.plane_id = plane_id
        self.row = row
        self.column = column
        self.price = price
        self.locked = False
        self.booked = booked
        self.conn = sqlite3.connect('db.sqlite3')

    def calculate_price(self, passenger: Passenger):
        ...

@dataclass
class Flight:
    def __init__(self, id, plane_id, departure_airport_id, arrival_airport_id, departure_time, arrival_time):
        self.id_ = id
        self.plane_id = plane_id
        self.fire_row = 10
        self.departure_airport_id = departure_airport_id
        self.arrival_airport_id = arrival_airport_id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.layout: List[List[Seat]] = []
        self.conn = sqlite3.connect('db.sqlite3')

    def get_available_seats(self, passengers: List[Passenger]):
        if len(passengers) == 0:
            return []
        elif len(passengers) > 6:
            print('Cannot book more than 6 passengers at a time')
            return []

        if len(passengers) <= 3:
            return self.handle_3(passengers)

    def handle_3(self, passengers: List[Passenger]):
        if len(passengers) == 1:
            return self.get_single_seats(passengers)
        elif len(passengers) == 2:
            pairs = self.get_pairs()
            if pairs:
                return pairs
            else:
                return self.get_single_seats(passengers)
        elif len(passengers) == 3:
            threes = self.get_empty_3()
            if threes:
                return threes
            else:
                pairs = self.get_pairs()
                if pairs:
                    singles = self.get_single_seats(passengers)
                    return pairs + singles
                else:
                    return self.get_single_seats(passengers)

    def get_empty_3(self):
        empty_3 = []
        for row in self.layout:
            left = row[:3]
            right = row[-3:]
            if all(not (seat.locked or seat.booked) for seat in left):
                empty_3.append(left)
            elif all(not (seat.locked or seat.booked) for seat in right):
                empty_3.append(right)
        return empty_3

    def get_pairs(self):
        pairs = []
        for row in self.layout:
            for i in range(3):
                if not (row[i].locked or row[i].booked) and not (row[i+3].locked or row[i+3].booked):
                    pairs.append([row[i], row[i+3]])
        return pairs

    def get_single_seats(self, passengers: List[Passenger]):
        singles = []
        for row in self.layout:
            if passengers and (not passengers[0].accept) and row[0].row == self.fire_row:
                print('Cannot allocate seat near fire exit for passenger who does not accept it', row[0].row)
                continue
            for seat in row:
                if not (seat.locked or seat.booked):
                    if seat.column == 0:
                        if row[1].locked or row[1].booked:
                            singles.append(seat)
                    elif seat.column == 5:
                        if row[4].locked or row[4].booked:
                            singles.append(seat)
                    else:
                        if (
                            (row[seat.column - 1].locked or row[seat.column - 1].booked) and
                            (row[seat.column + 1].locked or row[seat.column + 1].booked)
                        ):
                            singles.append(seat)
        if len(singles) < 1 or (singles[0].row == self.fire_row):
            flat_layout = [[seat] for row in self.layout for seat in row if row[0].row != self.fire_row]
            return flat_layout
        return singles

    def rank_options(self, passengers: List[Passenger], seat_list: List[List[Seat]]):
        if len(passengers) == 1:
            if passengers[0]['accept']:
                return seat_list
            return list(filter(
                lambda seat: seat[0].row != self.fire_row,  
                seat_list
            ))
        elif len(passengers) == 2:
            pairs = list(filter(
                lambda seats: len(seats) == 2,
                seat_list
            ))
            if pairs: 
                return pairs
            else:
                singles = list(filter(
                    lambda seat: len(seat) == 1,
                    seat_list
                ))
                possible_pairs = list(combinations(singles, 2))
                return sorted(possible_pairs, key=self.sort_pairs)
        elif len(passengers) == 3:
            threes = list(filter(
                lambda seats: len(seats) == 3,
                seat_list
            ))
            if threes:
                return threes
            else:
                pairs = list(filter(
                    lambda seats: len(seats) == 2,
                    seat_list
                ))
                if pairs:
                    singles = list(filter(
                        lambda seat: len(seat) == 1,
                        seat_list
                    ))
                    possible_triplets = list(product(pairs, singles))
                    possible_triplets = [[*pair, single] for pair, single in possible_triplets]
                    return sorted(possible_triplets, key=self.sort_triplets)
                else:
                    singles = list(filter(
                        lambda seat: len(seat) == 1,
                        seat_list
                    ))
                    possible_triplets = list(combinations(singles, 3))
                    return sorted(possible_triplets, key=self.sort_triplets)

    def sort_pairs(self, pair):
        x = pair[0].column - pair[1].column
        y = pair[0].row - pair[1].row
        return (x ** 2 + y ** 2) ** 0.5
    
    def sort_triplets(self, triplet):
        pairs = list(combinations(triplet, 2))
        return sum(self.sort_pairs(pair) for pair in pairs)

    def chose_option(self, passengers: List[Passenger], seat_list: List[List[Seat]]):
        options = self.rank_options(passengers, seat_list)
        return options[0]

    def lock_seats(self, seats: List[int]):
        for row in self.layout:
            for seat in row:
                if seat.id_ in seats:
                    seat.locked = True

    def populate_layout(self):
        seats = self.conn.execute('''
        SELECT id, row, column, price
        FROM Seat
        WHERE plane_id = ?
        ''', (self.plane_id,)).fetchall()
        seats = [
            dict(zip(['id', 'row', 'column', 'price'], seat))
            for seat in seats
        ]
        seats = [Seat(plane_id=self.plane_id, **seat) for seat in seats]
        first_row = seats[0].row
        last_row = seats[-1].row
        for row in range(first_row, last_row + 1):
            self.layout.append([seat for seat in seats if seat.row == row])
        # print(self.layout)

    def print_layout(self):
        for row in self.layout:
            # row is a list of Seat objects so print it in a readable format
            for seat in row:
                print(seat, end=' ')

    def book_seats(self, passengers: List[Passenger], seat_ids: List[int] = None):
        ...
