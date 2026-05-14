import reflex as rx
from typing import Optional
from .data import (
    ALL_COUNTRIES_FILTER,
    ALL_SEASON_FILTER,
    DEFAULT_LAT,
    DEFAULT_LON,
    DEFAULT_NUTRIENT_SORT,
    filter_products,
    get_catalog_label,
    get_products,
    get_search_suggestions,
    ProduceItem,
)


class State(rx.State):
    products: list[ProduceItem] = get_products()
    search_query: str = ""
    search_suggestions_open: bool = False
    filters_open: bool = False
    country_filter: str = ALL_COUNTRIES_FILTER
    season_filter: str = ALL_SEASON_FILTER
    nutrient_sort: str = DEFAULT_NUTRIENT_SORT
    # MOCK EMISSIONS LOGIC: start with the app's default location so product
    # cards can show emission values before browser geolocation returns.
    user_lat: float | None = DEFAULT_LAT
    user_lon: float | None = DEFAULT_LON
    menu_open: bool = False
    modal_open: bool = False
    modal_product: Optional[ProduceItem] = None

    def open_menu(self):
        self.menu_open = True

    def close_menu(self):
        self.menu_open = False

    def open_filters(self):
        self.filters_open = True

    def close_filters(self):
        self.filters_open = False

    def toggle_filters(self):
        self.filters_open = not self.filters_open

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

    def set_country_filter(self, value: str):
        self.country_filter = value

    def set_season_filter(self, value: str):
        self.season_filter = value

    def set_nutrient_sort(self, value: str):
        self.nutrient_sort = value

    def clear_filters(self):
        self.country_filter = ALL_COUNTRIES_FILTER
        self.season_filter = ALL_SEASON_FILTER
        self.nutrient_sort = DEFAULT_NUTRIENT_SORT

    def set_user_location(self, lat: float, lon: float):
        self.user_lat = lat
        self.user_lon = lon

    def open_modal(self, product_id: str):
        for product in self.filtered_products:
            if product["id"] == product_id:
                self.modal_product = product
                self.modal_open = True
                break

    def close_modal(self):
        self.modal_open = False
        self.modal_product = None

    @rx.var
    def filtered_products(self) -> list[ProduceItem]:
        return filter_products(
            products=self.products,
            query=self.search_query,
            country_filter=self.country_filter,
            season_filter=self.season_filter,
            nutrient_sort=self.nutrient_sort,
            user_lat=self.user_lat,
            user_lon=self.user_lon,
        )

    @rx.var
    def search_suggestions(self) -> list[ProduceItem]:
        return get_search_suggestions(self.search_query)

    @rx.var
    def has_search_query(self) -> bool:
        return bool(self.search_query.strip())

    @rx.var
    def has_active_filters(self) -> bool:
        return any(
            [
                self.country_filter != ALL_COUNTRIES_FILTER,
                self.season_filter != ALL_SEASON_FILTER,
                self.nutrient_sort != DEFAULT_NUTRIENT_SORT,
            ]
        )

    @rx.var
    def has_search_suggestions(self) -> bool:
        return self.search_suggestions_open and bool(self.search_suggestions)

    @rx.var
    def catalog_label(self) -> str:
        return get_catalog_label(len(self.filtered_products))
