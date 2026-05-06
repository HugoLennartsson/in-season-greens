import reflex as rx


class LocationState(rx.State):
    lat: float | None = None
    lon: float | None = None
    error: str = ""

    @rx.var
    def location_display(self) -> str:
        """Human-readable location string."""
        if self.lat is None or self.lon is None:
            return "Locating..."

        return f"{self.lat:.4f}, {self.lon:.4f}"

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