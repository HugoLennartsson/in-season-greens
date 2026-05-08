import pytest
from unittest.mock import MagicMock, patch
from in_season_greens.location_state import LocationState  # Adjust import path


@pytest.fixture
def state():
    """Provides a fresh instance of LocationState for every test."""
    return LocationState()


def test_initial_location_display(state):
    """Test the @rx.var logic for initial state."""
    assert state.location_display == "Locating..."
    assert state.city == ""


def test_handle_location_success(state):
    """Test the state update when JS returns successful coordinates."""
    # Mocking the internal reverse_geocode so we don't hit the internet
    with patch.object(LocationState, "_reverse_geocode", return_value="Berlin"):
        state.handle_location_result([52.52, 13.405])

    assert state.lat == 52.52
    assert state.lon == 13.405
    assert state.city == "Berlin"
    assert state.location_display == "Berlin"


def test_handle_location_error(state):
    """Test the state update when the browser returns an error."""
    state.handle_location_result(["ERROR", "User denied Geolocation"])

    assert state.error == "User denied Geolocation"
    assert state.lat is None
    assert state.location_display == "Locating..."


@patch("in_season_greens.location_state.Nominatim")
def test_reverse_geocode_api_success(mock_nominatim, state):
    """Test the logic inside the geocoder helper."""
    # Setup mock response
    mock_geolocator = MagicMock()
    mock_nominatim.return_value = mock_geolocator
    mock_geolocator.reverse.return_value.raw = {"address": {"city": "New York"}}

    result = state._reverse_geocode(40.71, -74.00)
    assert result == "New York"


@patch("in_season_greens.location_state.Nominatim")
def test_reverse_geocode_api_failure(mock_nominatim, state):
    """Test the helper's try/except block."""
    mock_nominatim.side_effect = Exception("API Down")

    result = state._reverse_geocode(0, 0)
    assert result == "City Lookup Failed"
