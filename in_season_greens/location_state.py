import reflex as rx
from geopy.geocoders import Nominatim


class LocationState(rx.State):
    lat: float | None = None
    lon: float | None = None
    city: str = ""
    error: str = ""

    def _reverse_geocode(self, lat: float, lon: float) -> str:
        """Helper to convert coordinates to a city name."""
        try:
            geolocator = Nominatim(user_agent="reflex_app")
            location = geolocator.reverse(f"{lat}, {lon}", timeout=5)
            if location and "address" in location.raw:
                address = location.raw["address"]
                return address.get("city")
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
    def set_location(self, lat: float, lon: float):
        print(f"[DEBUG] Received location: lat={lat}, lon={lon}")
        self.lat = lat
        self.lon = lon

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
