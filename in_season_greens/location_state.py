import reflex as rx


class LocationState(rx.State):
    lat: str = ""
    lon: str = ""
    location_display: str = "Gothenburg, SE"
    is_loading: bool = False
    error_message: str = ""

    def update_location(self, pos: dict):
        print("wts")
        self.lat = str(pos["coords"]["latitude"])
        self.lon = str(pos["coords"]["longitude"])
        # For now just show coordinates; later you can reverse geocode
        self.location_display = f"{float(self.lat):.2f}, {float(self.lon):.2f}"

    def handle_error(self, error: dict):
        pass  # keep default fallback

    def get_location(self):
        return rx.call_script(f"""
            navigator.geolocation.getCurrentPosition(
                (position) => {{
                    applyDelta({{
                        name: "{self.get_full_name()}.update_location",
                        payload: {{pos: {{coords: {{latitude: position.coords.latitude, longitude: position.coords.longitude}}}}}}
                    }});
                }},
                (error) => {{
                    applyDelta({{
                        name: "{self.get_full_name()}.handle_error",
                        payload: {{error: {{message: error.message}}}}
                    }});
                }}
            );
        """)
