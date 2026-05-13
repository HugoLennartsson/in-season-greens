import reflex as rx
from geopy.geocoders import Nominatim
from in_season_greens.weather_state import WeatherState

class LocationState(rx.State):
    lat: float | None = None
    lon: float | None = None
    city: str = ""
    error: str = ""
    typed_city: str = ""
    avg_temp: str = "Awaiting Location.."
    rain_outlook: str = "Awaiting Location.."
    harvest_outlook: str = "Awaiting Location.."

    def _reverse_geocode(self, lat: float, lon: float) -> str:
        """Helper to convert coordinates to a city name."""
        try:
            geolocator = Nominatim(user_agent="reflex_app")
            location = geolocator.reverse(f"{lat}, {lon}", timeout=5)
            if location and "address" in location.raw:
                address = location.raw["address"]
                return address.get("city", "Unknown Location")
            return "Unknown Location"
        except Exception:
            return "City Lookup Failed"

    @rx.var
    def location_display(self) -> str:
        """Human-readable location string."""
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
                        const lat = pos.coords.latitude;
                        const lon = pos.coords.longitude;

                        console.log("[DEBUG] Resolving:", lat, lon);
                        resolve([lat, lon]);
                    },
                    (err) => {
                        console.error("[DEBUG] Error:", err.message);
                        resolve(["ERROR", err.message]);
                    }
                );
            })
            """,
            callback=LocationState.handle_location_result,
        )

    @rx.event
    def handle_location_result(self, result):
        print(f"[DEBUG] Raw result: {result}")

        if result is None:
            print("[DEBUG] No result received")
            return

        if result[0] == "ERROR":
            self.error = result[1]
            print(f"[DEBUG] Error received: {self.error}")
            return

        lat, lon = result
        print(f"[DEBUG] Received location: lat={lat}, lon={lon}")

        self.lat = lat
        self.lon = lon
        self.city = self._reverse_geocode(lat, lon)
        self.typed_city = self.city
        
        yield LocationState.fetch_weather

    @rx.event
    def set_typed_city(self, val: str):
        self.typed_city = val

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

            allowed = {"city", "town", "village", "municipality"}

            place_type = location.raw.get("type", "")

            if place_type not in allowed:
                self.error = "Please enter a valid city"
                return

            self.city = location.address.split(",")[0]
            self.typed_city = self.city

            self.lat = location.latitude
            self.lon = location.longitude

            self.error = ""
            yield LocationState.fetch_weather

        except Exception:
            self.error = "City lookup failed"

    @rx.event
    def handle_key_down(self, key: str):
        if key == "Enter":
            return LocationState.validate_city
    
    @rx.event
    def fetch_weather(self):
        if self.lat is None or self.lon is None:
            self.avg_temp = "Locating..."
            return
            
        self.avg_temp = WeatherState.get_avg_temp(self.lat, self.lon)
        self.rain_outlook = WeatherState.get_rain_outlook(self.lat, self.lon)
        self.harvest_outlook = WeatherState.get_harvest_outlook(self.lat, self.lon)
