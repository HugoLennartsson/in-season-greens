import reflex as rx

from . import styles
from .data import (
    Product,
    ProduceItem,
    get_catalog_label,
    get_products,
    get_search_suggestions,
    search_products,
)
from .components.navigation import (
    desktop_header,
    drawer,
    mobile_header,
    mobile_sticky_filters,
)
from .components.overview import overview_section
from .components.product_card import product_card
from .components.ui import product_modal

from .state import State
from .location_state import LocationState


def catalog() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                rx.text(
                    State.catalog_label,
                    class_name=styles.catalog.count,
                ),
                rx.heading(
                    "Product Catalog",
                    class_name=styles.catalog.title,
                ),
            ),
            class_name=styles.catalog.header,
        ),
        rx.grid(
            rx.foreach(
                State.filtered_products,
                lambda product: product_card(product, State),
            ),
            class_name=styles.catalog.grid,
        ),
        class_name=styles.catalog.shell,
    )


def home_view() -> rx.Component:
    return rx.box(
        product_modal(State),
        drawer(State),
        desktop_header(State),
        mobile_header(State),
        overview_section(),
        mobile_sticky_filters(State),
        catalog(),
        class_name=styles.app.page,
    )


def index() -> rx.Component:
    return rx.box(home_view(), on_mount=LocationState.get_location)


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,400;0,600;0,700;0,800;0,900;1,400&display=swap",
    ],
)
app.add_page(index, route="/")
