import unittest
import sqlite3
from algorithm import Passenger, Seat, Flight
from behave import *

@given('a passenger named "{name}" who accepts fire exit seats')
def step_impl(context, name):
    context.passenger = Passenger(age=30, name=name, accept=True)

@when('she searches for available seats')
def step_impl(context):
    context.flight = Flight(id=1, plane_id=1, departure_airport_id=1, arrival_airport_id=2, departure_time="2024-06-01 10:00", arrival_time="2024-06-01 12:00")
    context.flight.populate_layout()
    context.result = context.flight.get_available_seats([context.passenger])

@then('she should see available seats')
def step_impl(context):
    assert context.result

@given('two passengers named "{name1}" and "{name2}" who accept fire exit seats')
def step_impl(context, name1, name2):
    context.passengers = [
        Passenger(age=30, name=name1, accept=True),
        Passenger(age=35, name=name2, accept=True)
    ]

@when('they search for available seats')
def step_impl(context):
    context.flight = Flight(id=1, plane_id=1, departure_airport_id=1, arrival_airport_id=2, departure_time="2024-06-01 10:00", arrival_time="2024-06-01 12:00")
    context.flight.populate_layout()
    context.result = context.flight.get_available_seats(context.passengers)

@then('they should see available pairs of seats')
def step_impl(context):
    assert context.result

@given('a group of more than six passengers')
def step_impl(context):
    context.passengers = [
        Passenger(age=30, name="Passenger1", accept=True),
        Passenger(age=30, name="Passenger2", accept=True),
        Passenger(age=30, name="Passenger3", accept=True),
        Passenger(age=30, name="Passenger4", accept=True),
        Passenger(age=30, name="Passenger5", accept=True),
        Passenger(age=30, name="Passenger6", accept=True),
        Passenger(age=30, name="Passenger7", accept=True)
    ]

@when('they try to book seats')
def step_impl(context):
    context.flight = Flight(id=1, plane_id=1, departure_airport_id=1, arrival_airport_id=2, departure_time="2024-06-01 10:00", arrival_time="2024-06-01 12:00")
    context.flight.populate_layout()
    context.result = context.flight.get_available_seats(context.passengers)

@then('the system should not allow them to book more than six seats at once')
def step_impl(context):
    assert context.result == []
