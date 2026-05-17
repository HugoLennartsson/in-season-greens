import json
import re
from pathlib import Path
from typing import Any, Callable, TypedDict


class NutritionFacts(TypedDict):
    calories: float
    serving_size_g: float
    fat_total_g: float
    fat_saturated_g: float
    protein_g: float
    sodium_mg: int
    potassium_mg: int
    cholesterol_mg: int
    carbohydrates_total_g: float
    fiber_g: float
    sugar_g: float


class OverviewSignal(TypedDict):
    icon: str
    value: str
    label: str


class OverviewOutlook(TypedDict):
    icon: str
    text: str


class ProduceItem(TypedDict):
    id: str
    name_en: str
    category: str
    nutrients: list[NutritionFacts]


class NavItem(TypedDict):
    icon: str
    label: str
    subtitle: str


class ProductOrderChoice(TypedDict):
    key: str
    label: str


class ProductOrder:
    def __init__(
        self,
        key: str,
        label: str,
        sort_key: Callable[[ProduceItem], Any],
        reverse: bool = False,
    ):
        self.key = key
        self.label = label
        self.sort_key = sort_key
        self.reverse = reverse


APP_NAME = "InSeasonGreens"
MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
CURRENT_MONTH = 5

LOCATION = "Gothenburg"
COUNTRY = "SE"
SEARCH_SUGGESTION_LIMIT = 6
_ROOT = Path(__file__).resolve().parents[1]
_ALL_PRODUCE_PATH = _ROOT / "all_produce.json"

PRECIPITATION = "Normal"
AVG_TEMP = (16, 18)
HARVEST = "Favorable"

NAV_ITEMS: list[NavItem] = [
    {"icon": "home", "label": "Home", "subtitle": "Browse all products"},
    {"icon": "map_pin", "label": "Local", "subtitle": f"Grown near {LOCATION}"},
    {"icon": "wind", "label": "CO2 Tracker", "subtitle": "Compare CO2 per kg"},
    {"icon": "droplets", "label": "Water Usage", "subtitle": "Water per kg ratings"},
    {"icon": "bookmark", "label": "Saved", "subtitle": "Your saved products"},
    {"icon": "info", "label": "About", "subtitle": "Sources and methodology"},
]


PRODUCT_ORDER_OPTIONS: tuple[ProductOrder, ...] = (
    ProductOrder(
        key="name_asc",
        label="Name A-Z",
        sort_key=lambda product: normalize_search_text(product["name_en"]),
    ),
    ProductOrder(
        key="name_desc",
        label="Name Z-A",
        sort_key=lambda product: normalize_search_text(product["name_en"]),
        reverse=True,
    ),
)
DEFAULT_PRODUCT_ORDER_KEY = PRODUCT_ORDER_OPTIONS[0].key
PRODUCT_ORDER_CHOICES: list[ProductOrderChoice] = [
    {"key": option.key, "label": option.label} for option in PRODUCT_ORDER_OPTIONS
]
PRODUCT_ORDER_LABELS = [option.label for option in PRODUCT_ORDER_OPTIONS]


def _load_all_produce() -> list[ProduceItem]:
    with _ALL_PRODUCE_PATH.open(encoding="utf-8") as produce_file:
        return json.load(produce_file)


ALL_PRODUCE: list[ProduceItem] = _load_all_produce()


def normalize_search_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def levenshtein_distance(left: str, right: str) -> int:
    if left == right:
        return 0
    if not left:
        return len(right)
    if not right:
        return len(left)

    previous_row = list(range(len(right) + 1))
    for left_index, left_char in enumerate(left, start=1):
        current_row = [left_index]
        for right_index, right_char in enumerate(right, start=1):
            insert_cost = current_row[right_index - 1] + 1
            delete_cost = previous_row[right_index] + 1
            replace_cost = previous_row[right_index - 1] + (left_char != right_char)
            current_row.append(min(insert_cost, delete_cost, replace_cost))
        previous_row = current_row

    return previous_row[-1]


def fuzzy_search_score(query: str, value: str) -> int | None:
    normalized_query = normalize_search_text(query)
    normalized_value = normalize_search_text(value)
    if not normalized_query:
        return None

    if normalized_value == normalized_query:
        return 0
    if normalized_value.startswith(normalized_query):
        return 10 + len(normalized_value) - len(normalized_query)
    if normalized_query in normalized_value:
        return 30 + normalized_value.index(normalized_query)

    max_distance = 1 if len(normalized_query) <= 5 else 2
    distance = levenshtein_distance(normalized_query, normalized_value)
    if distance <= max_distance:
        return 50 + distance * 5 + abs(len(normalized_value) - len(normalized_query))

    return None


def get_search_suggestions(query: str, limit: int = SEARCH_SUGGESTION_LIMIT) -> list[ProduceItem]:
    scored_items = [
        (score, item["name_en"], item)
        for item in ALL_PRODUCE
        if (score := fuzzy_search_score(query, item["name_en"])) is not None
    ]
    scored_items.sort(key=lambda match: (match[0], match[1]))
    return [item for _, __, item in scored_items[:limit]]


def search_products(query: str, products: list[ProduceItem] | None = None) -> list[ProduceItem]:
    products_to_search = products or get_products()
    if not normalize_search_text(query):
        return products_to_search

    scored_products = [
        (score, product["name_en"], product)
        for product in products_to_search
        if (score := fuzzy_search_score(query, product["name_en"])) is not None
    ]
    scored_products.sort(key=lambda match: (match[0], match[1]))
    return [product for _, __, product in scored_products]


def get_product_order(order_key: str) -> ProductOrder:
    return next(
        (
            option
            for option in PRODUCT_ORDER_OPTIONS
            if option.key == order_key or option.label == order_key
        ),
        PRODUCT_ORDER_OPTIONS[0],
    )


def get_product_order_label(order_key: str) -> str:
    return get_product_order(order_key).label


def get_product_order_key(order_label: str) -> str:
    return next(
        (
            option.key
            for option in PRODUCT_ORDER_OPTIONS
            if option.label == order_label or option.key == order_label
        ),
        DEFAULT_PRODUCT_ORDER_KEY,
    )


def order_products(
    products: list[ProduceItem],
    order_key: str = DEFAULT_PRODUCT_ORDER_KEY,
) -> list[ProduceItem]:
    order = get_product_order(order_key)
    return sorted(
        products,
        key=lambda product: (order.sort_key(product), product["id"]),
        reverse=order.reverse,
    )


def get_products() -> list[ProduceItem]:
    return ALL_PRODUCE


def get_all_produce() -> list[ProduceItem]:
    return ALL_PRODUCE


def get_seasonal_veggies() -> list[ProduceItem]:
    return get_products()


def get_nav_items() -> list[NavItem]:
    return NAV_ITEMS


def get_current_month_name() -> str:
    return MONTHS[CURRENT_MONTH]


def get_short_location() -> str:
    return f"{LOCATION}, {COUNTRY}"


def get_full_location() -> str:
    return f"{LOCATION}, {COUNTRY} · {get_current_month_name()}"


def get_temperature_range() -> str:
    return f"{AVG_TEMP[0]}-{AVG_TEMP[1]} C"


def get_catalog_label(product_count: int) -> str:
    return f"{product_count} PRODUCTS · {LOCATION.upper()} · {get_current_month_name().upper()}"


def get_overview_signals() -> list[OverviewSignal]:
    return [
        {"icon": "info", "value": get_current_month_name(), "label": "Current month"},
        {"icon": "thermometer", "value": get_temperature_range(), "label": "Avg temp normal"},
        {"icon": "cloud_rain", "value": PRECIPITATION, "label": "Rain outlook"},
        {"icon": "sprout", "value": HARVEST, "label": "Harvest outlook"},
    ]


def get_season_outlook() -> list[OverviewOutlook]:
    return [
        {
            "icon": "thermometer",
            "text": f"Average temperature is within {LOCATION}'s normal {get_current_month_name()} range.",
        },
        {
            "icon": "cloud_rain",
            "text": f"Rain outlook is {PRECIPITATION.lower()} for outdoor leafy greens and field crops.",
        },
        {
            "icon": "sprout",
            "text": f"Harvest outlook is {HARVEST.lower()} for local seasonal produce.",
        },
        {
            "icon": "leaf",
            "text": "Season status is based on local crop calendars and the current month.",
        },
    ]
