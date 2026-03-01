from FlightSelectorPage import FlightSelectorPage
import pytest

def test_OriginSelection(flightSelector):

    flightSelector.choose_flight("Paris", "New York Coty")

    assert True