import reflex as rx
from geopy.geocoders import Nominatim
from in_season_greens.weather_state import WeatherState

from .data import COUNTRY, is_supported_country_code, normalize_country_code


class LocationState(rx.State):
    lat: float | None = None
    lon: float | None = None
    country_code: str = COUNTRY
    country_code_is_fallback: bool = True
    city: str = ""
    error: str = ""

    typed_city: str = ""

    avg_temp: str = "Awaiting Location.."
    rain_outlook: str = "Awaiting Location.."
    harvest_outlook: str = "Awaiting Location.."

    suggestions: list[str] = []

    def _set_country_code(self, code: str | None):
        self.country_code = normalize_country_code(code)
        self.country_code_is_fallback = not is_supported_country_code(code)

    def _reverse_geocode(self, lat: float, lon: float) -> str:
        try:
            geolocator = Nominatim(user_agent="reflex_app")
            location = geolocator.reverse(
                f"{lat}, {lon}",
                timeout=5,
                addressdetails=True,
            )
            if location and "address" in location.raw:
                address = location.raw["address"]
                self._set_country_code(address.get("country_code"))
                return (
                    address.get("city")
                    or address.get("town")
                    or address.get("village")
                    or address.get("municipality")
                    or "Unknown Location"
                )
            self._set_country_code(None)
            return "Unknown Location"

        except Exception:
            self._set_country_code(None)
            return "City Lookup Failed"

    @rx.var
    def location_display(self) -> str:
        if self.lat is None or self.lon is None:
            return "Locating..."

        return self.city

    @rx.event
    def set_error(self, message: str):
        self.error = message

    @rx.event
    def get_location(self):
        return rx.call_script(
            """
            new Promise((resolve) => {
                navigator.geolocation.getCurrentPosition(
                    (pos) => {
                        resolve([
                            pos.coords.latitude,
                            pos.coords.longitude
                        ]);
                    },
                    (err) => {
                        resolve(["ERROR", err.message]);
                    }
                );
            })
            """,
            callback=LocationState.handle_location_result,
        )

    @rx.event
    def handle_location_result(self, result):
        if result is None:
            return

        if result[0] == "ERROR":
            self.error = result[1]
            return

        lat, lon = result

        self.lat = lat
        self.lon = lon

        self.city = self._reverse_geocode(lat, lon)
        self.typed_city = self.city
        from .state import State

        yield State.set_user_location(
            lat,
            lon,
            self.country_code,
            self.country_code_is_fallback,
        )

        yield LocationState.fetch_weather

    @rx.event
    def validate_city(self):
        val = self.typed_city.strip()

        if not val:
            self.error = "City cannot be empty"
            return

        try:
            geolocator = Nominatim(user_agent="reflex_app")

            location = geolocator.geocode(
                val,
                exactly_one=True,
                timeout=5,
                addressdetails=True,
            )

            if location is None:
                self.error = "Invalid city"
                return

            address = location.raw.get("address", {})

            city_name = (
                address.get("city")
                or address.get("town")
                or address.get("village")
                or address.get("municipality")
                or address.get("county")
                or address.get("state")
            )

            if not city_name:
                self.error = "Please enter a valid city"
                return

            self.city = city_name
            self.typed_city = city_name

            self.lat = location.latitude
            self.lon = location.longitude
            address = location.raw.get("address", {})
            self._set_country_code(address.get("country_code"))
            self.error = ""
            self.suggestions = []
            from .state import State

            yield State.set_user_location(
                self.lat,
                self.lon,
                self.country_code,
                self.country_code_is_fallback,
            )

            yield LocationState.fetch_weather

        except Exception as e:
            print(e)
            self.error = "City lookup failed"

    @rx.event
    def handle_key_down(self, key):
        if key == "Enter":
            return LocationState.validate_city

    @rx.event
    def fetch_weather(self):
        if self.lat is None or self.lon is None:
            self.avg_temp = "Locating..."
            return

        self.avg_temp = WeatherState.get_avg_temp(
            self.lat,
            self.lon,
        )

        self.rain_outlook = WeatherState.get_rain_outlook(
            self.lat,
            self.lon,
        )

        self.harvest_outlook = WeatherState.get_harvest_outlook(
            self.lat,
            self.lon,
        )

    @rx.event
    def set_typed_city(self, val: str):
        import requests
        import urllib.parse

        self.typed_city = val

        clean_val = val.strip()

        if len(clean_val) < 2:
            self.suggestions = []
            return

        try:
            encoded_query = urllib.parse.quote(clean_val)

            url = f"https://photon.komoot.io/api/" f"?q={encoded_query}&limit=5"

            print(f"[DEBUG] Fetching: {url}")
            response = requests.get(
                url,
                timeout=5,
                headers={"User-Agent": "Mozilla/5.0 (compatible; InSeasonGreens/1.0)"},
            )
            print(f"[DEBUG] Status: {response.status_code}")  # ← add this
            print(f"[DEBUG] Data: {response.json()}")

            if response.status_code != 200:
                self.suggestions = []
                return

            data = response.json()

            results = []

            for feature in data.get("features", []):
                properties = feature.get("properties", {})

                city_name = properties.get("city") or properties.get("name")

                country = properties.get("country")

                if city_name:
                    display = f"{city_name}, {country}" if country else city_name

                    if display not in results:
                        results.append(display)

            self.suggestions = results

            print("Suggestions:", results)

            print(f"[DEBUG] Suggestions set to: {self.suggestions}")

        except Exception as e:
            print("Autocomplete error:", e)
            print(f"[DEBUG] Exception: {e}")
            self.suggestions = []

    @rx.event
    def select_suggestion(self, selected_city: str):
        if "," in selected_city:
            self.typed_city = selected_city.split(",")[0].strip()
        else:
            self.typed_city = selected_city

        self.suggestions = []

        return LocationState.validate_city
