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


class State(rx.State):
    products: list[Product] = get_products()
    search_query: str = ""
    menu_open: bool = False

    def open_menu(self):
        self.menu_open = True

    def close_menu(self):
        self.menu_open = False

    def set_search_query(self, query: str):
        self.search_query = query

    def apply_search_suggestion(self, name: str):
        self.search_query = name

    def clear_search(self):
        self.search_query = ""

    @rx.var
    def filtered_products(self) -> list[Product]:
        return search_products(self.search_query, self.products)

    @rx.var
    def search_suggestions(self) -> list[ProduceItem]:
        return get_search_suggestions(self.search_query)

    @rx.var
    def has_search_query(self) -> bool:
        return bool(self.search_query.strip())

    @rx.var
    def has_search_suggestions(self) -> bool:
        return bool(self.search_suggestions)

    @rx.var
    def catalog_label(self) -> str:
        return get_catalog_label(len(self.filtered_products))


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
                lambda product: product_card(product),
            ),
            class_name=styles.catalog.grid,
        ),
        class_name=styles.catalog.shell,
    )


def home_view() -> rx.Component:
    return rx.box(
        drawer(State),
        desktop_header(State),
        mobile_header(State),
        overview_section(),
        mobile_sticky_filters(State),
        catalog(),
        class_name=styles.app.page,
    )


def index() -> rx.Component:
    return home_view()


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,400;0,600;0,700;0,800;0,900;1,400&display=swap",
    ],
)
app.add_page(index, route="/")
