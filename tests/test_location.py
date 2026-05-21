import pytest
from unittest.mock import MagicMock, patch
from in_season_greens.location_state import LocationState


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
    assert state.country_code == "SE"
    assert state.country_code_is_fallback
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
    mock_geolocator.reverse.return_value.raw = {
        "address": {"city": "New York", "country_code": "us"}
    }

    result = state._reverse_geocode(40.71, -74.00)
    assert result == "New York"
    assert state.country_code == "US"
    assert not state.country_code_is_fallback


def test_handle_location_result_none(state):
    """Triggers the 'if result is None' safety check."""
    state.handle_location_result(None)
    assert state.lat is None  # State should remain unchanged


@pytest.mark.parametrize(
    "raw_data",
    [
        {"address": {}},
        {"some_other_key": "data"},
    ],
)
@patch("in_season_greens.location_state.Nominatim")
def test_reverse_geocode_unknown_cases(mock_nominatim, state, raw_data):
    mock_geolocator = MagicMock()
    mock_nominatim.return_value = mock_geolocator
    mock_geolocator.reverse.return_value.raw = raw_data

    result = state._reverse_geocode(1.1, 1.1)

    assert result == "Unknown Location"
    assert state.country_code == "SE"
    assert state.country_code_is_fallback


def test_get_location_call(state):
    """Executes the event that triggers the JS injection."""
    command = state.get_location()
    assert command is not None


@patch("in_season_greens.location_state.Nominatim")
def test_reverse_geocode_exception(mock_nominatim, state):
    """Forces an exception during the .reverse() call to test the 'except' block."""
    mock_geolocator = MagicMock()
    mock_nominatim.return_value = mock_geolocator
    mock_geolocator.reverse.side_effect = Exception("Network Timeout")
    result = state._reverse_geocode(52.5, 13.4)
    assert result == "City Lookup Failed"
    assert state.country_code_is_fallback


def test_set_error(state):
    state.set_error("Manual Error")
    assert state.error == "Manual Error"


@patch("in_season_greens.location_state.Nominatim")
def test_validate_city_success(mock_nominatim, state):
    """Valid city should update state correctly."""

    state.typed_city = "Stockholm"

    mock_geolocator = MagicMock()
    mock_nominatim.return_value = mock_geolocator

    mock_location = MagicMock()
    mock_location.address = "Stockholm, Sweden"
    mock_location.latitude = 59.3293
    mock_location.longitude = 18.0686
    mock_location.raw = {
        "type": "city",
        "address": {"country_code": "se"},
    }

    mock_geolocator.geocode.return_value = mock_location

    state.validate_city()

    assert state.city == "Stockholm"
    assert state.typed_city == "Stockholm"
    assert state.lat == 59.3293
    assert state.lon == 18.0686
    assert state.country_code == "SE"
    assert not state.country_code_is_fallback
    assert state.error == ""


@patch("in_season_greens.location_state.Nominatim")
def test_validate_city_invalid_city(mock_nominatim, state):
    """Invalid city should show error."""

    state.typed_city = "asdasdasd"

    mock_geolocator = MagicMock()
    mock_nominatim.return_value = mock_geolocator

    mock_geolocator.geocode.return_value = None

    state.validate_city()

    assert state.error == "Invalid city"


def test_validate_city_empty_input(state):
    """Empty input should trigger validation error."""

    state.typed_city = "   "

    state.validate_city()

    assert state.error == "City cannot be empty"


@patch("in_season_greens.location_state.Nominatim")
def test_validate_city_invalid_place_type(mock_nominatim, state):
    """Non-city locations should be rejected."""

    state.typed_city = "Eiffel Tower"

    mock_geolocator = MagicMock()
    mock_nominatim.return_value = mock_geolocator

    mock_location = MagicMock()
    mock_location.raw = {"type": "attraction"}

    mock_geolocator.geocode.return_value = mock_location

    state.validate_city()

    assert state.error == "Please enter a valid city"


@patch("in_season_greens.location_state.Nominatim")
def test_validate_city_exception(mock_nominatim, state):
    """Geocoder exceptions should be handled."""

    state.typed_city = "Stockholm"

    mock_geolocator = MagicMock()
    mock_nominatim.return_value = mock_geolocator

    mock_geolocator.geocode.side_effect = Exception("Timeout")

    state.validate_city()

    assert state.error == "City lookup failed"


def test_set_typed_city(state):
    """Typing should update typed_city only."""

    state.set_typed_city("Berlin")

    assert state.typed_city == "Berlin"
    assert state.city == ""


def test_handle_key_down_enter(state):
    result = state.handle_key_down("Enter")
    assert result == LocationState.validate_city


def test_handle_key_down_other_key(state):
    result = state.handle_key_down("A")
    assert result is None
