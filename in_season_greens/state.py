import reflex as rx
from typing import Optional
from .data import (
    CATEGORY_FILTER_OPTIONS,
    COUNTRY_FILTER_OPTIONS,
    DEFAULT_LAT,
    DEFAULT_LON,
    SEASON_FILTER_OPTIONS,
    SORT_ASC,
    SORT_DESC,
    SORT_FIELD_OPTIONS,
    filter_products,
    get_catalog_label,
    get_products,
    get_search_suggestions,
    normalize_search_text,
    ProduceItem,
)


class State(rx.State):
    products: list[ProduceItem] = get_products()
    search_query: str = ""
    search_suggestions_open: bool = False
    filters_open: bool = False
    country_search_query: str = ""
    selected_country_codes: list[str] = []
    selected_season_statuses: list[str] = []
    selected_categories: list[str] = []
    sort_key: str = ""
    sort_direction: str = ""
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

    def set_country_search_query(self, value: str):
        self.country_search_query = value

    def toggle_country_filter(self, country_code: str):
        if country_code in self.selected_country_codes:
            self.selected_country_codes = [
                code for code in self.selected_country_codes if code != country_code
            ]
            return
        self.selected_country_codes = [*self.selected_country_codes, country_code]

    def remove_country_filter(self, country_code: str):
        self.selected_country_codes = [
            code for code in self.selected_country_codes if code != country_code
        ]

    def clear_country_filters(self):
        self.selected_country_codes = []

    def toggle_season_filter(self, season_status: str):
        if season_status in self.selected_season_statuses:
            self.selected_season_statuses = [
                status
                for status in self.selected_season_statuses
                if status != season_status
            ]
            return
        self.selected_season_statuses = [*self.selected_season_statuses, season_status]

    def toggle_category_filter(self, category: str):
        if category in self.selected_categories:
            self.selected_categories = [
                selected_category
                for selected_category in self.selected_categories
                if selected_category != category
            ]
            return
        self.selected_categories = [*self.selected_categories, category]

    def toggle_sort(self, sort_key: str):
        if self.sort_key != sort_key:
            self.sort_key = sort_key
            self.sort_direction = SORT_ASC
            return
        if self.sort_direction == SORT_ASC:
            self.sort_direction = SORT_DESC
            return
        self.sort_key = ""
        self.sort_direction = ""

    def clear_filters(self):
        self.country_search_query = ""
        self.selected_country_codes = []
        self.selected_season_statuses = []
        self.selected_categories = []
        self.sort_key = ""
        self.sort_direction = ""

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
            country_filters=self.selected_country_codes,
            season_filters=self.selected_season_statuses,
            category_filters=self.selected_categories,
            sort_key=self.sort_key,
            sort_direction=self.sort_direction,
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
                bool(self.selected_country_codes),
                bool(self.selected_season_statuses),
                bool(self.selected_categories),
                bool(self.sort_key),
            ]
        )

    @rx.var
    def has_search_suggestions(self) -> bool:
        return self.search_suggestions_open and bool(self.search_suggestions)

    @rx.var
    def catalog_label(self) -> str:
        return get_catalog_label(len(self.filtered_products))

    @rx.var
    def selected_country_options(self) -> list[dict]:
        selected_codes = set(self.selected_country_codes)
        return [
            option
            for option in COUNTRY_FILTER_OPTIONS
            if option["value"] in selected_codes
        ]

    @rx.var
    def country_options(self) -> list[dict]:
        query = normalize_search_text(self.country_search_query)
        selected_codes = set(self.selected_country_codes)
        return [
            {
                "value": option["value"],
                "label": option["label"],
                "selected": option["value"] in selected_codes,
            }
            for option in COUNTRY_FILTER_OPTIONS
            if not query
            or query in normalize_search_text(option["label"])
            or query in normalize_search_text(option["value"])
        ]

    @rx.var
    def season_options(self) -> list[dict]:
        selected_statuses = set(self.selected_season_statuses)
        return [
            {
                "value": option["value"],
                "label": option["label"],
                "selected": option["value"] in selected_statuses,
            }
            for option in SEASON_FILTER_OPTIONS
        ]

    @rx.var
    def category_options(self) -> list[dict]:
        selected_categories = set(self.selected_categories)
        return [
            {
                "value": option["value"],
                "label": option["label"],
                "selected": option["value"] in selected_categories,
            }
            for option in CATEGORY_FILTER_OPTIONS
        ]

    @rx.var
    def sort_options(self) -> list[dict]:
        return [
            {
                "value": option["value"],
                "label": option["label"],
                "direction": self.sort_direction
                if self.sort_key == option["value"]
                else "",
            }
            for option in SORT_FIELD_OPTIONS
        ]

    @rx.var
    def active_sort_label(self) -> str:
        if not self.sort_key:
            return "No sort"
        for option in SORT_FIELD_OPTIONS:
            if option["value"] == self.sort_key:
                direction = "ascending" if self.sort_direction == SORT_ASC else "descending"
                return f"{option['label']} {direction}"
        return "No sort"
