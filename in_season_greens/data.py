import json
import re
from pathlib import Path
from typing import TypedDict


class Product(TypedDict):
    id: str
    name: str
    category: str
    status: str
    months: list[int]
    co2: float | None
    origin: str
    local: bool | None
    nutrients: list[str]
    image_src: str


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


class NavItem(TypedDict):
    icon: str
    label: str
    subtitle: str


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

def _load_all_produce() -> list[ProduceItem]:
    with _ALL_PRODUCE_PATH.open(encoding="utf-8") as produce_file:
        return json.load(produce_file)


ALL_PRODUCE: list[ProduceItem] = _load_all_produce()


def get_all_produce_ids() -> set[str]:
    return {item["id"] for item in ALL_PRODUCE}


def product_from_produce(item: ProduceItem) -> Product:
    return {
        "id": item["id"],
        "name": item["name_en"],
        "category": item["category"],
        "status": "unknown",  # Legacy card field: all_produce.json has no season status.
        "months": [],  # Legacy card field: all_produce.json has no month calendar.
        "co2": None,  # Legacy card field: all_produce.json has no CO2 estimate.
        "origin": "???",  # Legacy card field: all_produce.json has no origin/source country.
        "local": None,  # Legacy card field: all_produce.json has no local availability flag.
        "nutrients": ["???"],  # Legacy card field: all_produce.json has no nutrient data.
        "image_src": f"/img/{item['id']}.jpg",
    }


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


def search_products(query: str, products: list[Product] | None = None) -> list[Product]:
    products_to_search = products or get_products()
    if not normalize_search_text(query):
        return products_to_search

    scored_products = [
        (score, product["name"], product)
        for product in products_to_search
        if (score := fuzzy_search_score(query, product["name"])) is not None
    ]
    scored_products.sort(key=lambda match: (match[0], match[1]))
    return [product for _, __, product in scored_products]


def get_products() -> list[Product]:
    return [product_from_produce(item) for item in ALL_PRODUCE]


def get_all_produce() -> list[ProduceItem]:
    return ALL_PRODUCE


def get_seasonal_veggies() -> list[Product]:
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
