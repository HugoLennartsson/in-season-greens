import reflex as rx
from typing import Optional
from .data import (
    DEFAULT_PRODUCT_ORDER_KEY,
    get_catalog_label,
    get_product_order_key,
    get_product_order_label,
    get_products,
    get_search_suggestions,
    order_products,
    search_products,
    ProduceItem,
)


class State(rx.State):
    products: list[ProduceItem] = get_products()
    search_query: str = ""
    search_suggestions_open: bool = False
    menu_open: bool = False
    modal_open: bool = False
    modal_product: Optional[ProduceItem] = None
    product_order_key: str = DEFAULT_PRODUCT_ORDER_KEY

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

    def set_product_order(self, order_label: str):
        self.product_order_key = get_product_order_key(order_label)

    def open_modal(self, product_id: str):
        for product in self.products:
            if product["id"] == product_id:
                self.modal_product = product
                self.modal_open = True
                break

    def close_modal(self):
        self.modal_open = False
        self.modal_product = None

    @rx.var
    def filtered_products(self) -> list[ProduceItem]:
        return order_products(
            search_products(self.search_query, self.products),
            self.product_order_key,
        )

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

    @rx.var
    def product_order_label(self) -> str:
        return get_product_order_label(self.product_order_key)
