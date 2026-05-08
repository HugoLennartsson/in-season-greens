import reflex as rx
from .data import (
    get_catalog_label,
    get_products,
    get_search_suggestions,
    search_products,
    Product,
    ProduceItem,
)


class State(rx.State):
    products: list[Product] = get_products()
    search_query: str = ""
    search_suggestions_open: bool = False
    menu_open: bool = False

    def open_menu(self):
        self.menu_open = True

    def close_menu(self):
        self.menu_open = False

    def set_search_query(self, query: str):
        self.search_query = query
        self.search_suggestions_open = bool(query.strip())

    def open_search_suggestions(self):
        self.search_suggestions_open = bool(self.search_query.strip())

    def close_search_suggestions(self):
        self.search_suggestions_open = False

    def handle_search_key(self, key: str):
        if key == "Enter":
            self.search_suggestions_open = False

    def submit_search(self):
        self.search_suggestions_open = False

    def apply_search_suggestion(self, name: str):
        self.search_query = name
        self.search_suggestions_open = False

    def clear_search(self):
        self.search_query = ""
        self.search_suggestions_open = False

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
        return self.search_suggestions_open and bool(self.search_suggestions)

    @rx.var
    def catalog_label(self) -> str:
        return get_catalog_label(len(self.filtered_products))
