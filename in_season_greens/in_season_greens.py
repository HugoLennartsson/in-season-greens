import reflex as rx
from .data import get_seasonal_veggies

class State(rx.State):
    # This stores the list of veggies
    veggies: list[dict] = get_seasonal_veggies()

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("In-Season Greens", size="9"),
            rx.text("Current local favorites:"),
            rx.hstack(
                rx.foreach(
                    State.veggies,
                    lambda v: rx.badge(v["name"], color_scheme="grass", size="3")
                ),
            ),
            spacing="5",
        ),
        padding_top="10%",
    )

app = rx.App()
app.add_page(index)
