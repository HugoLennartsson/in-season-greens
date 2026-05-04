import json
import re
from pathlib import Path
from typing import TypedDict


class Product(TypedDict):
    id: int
    name: str
    emoji: str
    status: str
    months: list[int]
    co2: float
    origin: str
    local: bool
    nutrients: list[str]


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


PRODUCTS: list[Product] = [
    {
        "id": 1,
        "name": "Strawberry",
        "emoji": "🍓",
        "status": "peak",
        "months": [4, 5, 6, 7],
        "co2": 0.4,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Vitamin C", "Folate"],
    },
    {
        "id": 2,
        "name": "Tomato",
        "emoji": "🍅",
        "status": "peak",
        "months": [5, 6, 7, 8],
        "co2": 0.7,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Vitamin C", "Lycopene"],
    },
    {
        "id": 3,
        "name": "Cucumber",
        "emoji": "🥒",
        "status": "season",
        "months": [5, 6, 7],
        "co2": 0.6,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Hydration", "Vitamin K"],
    },
    {
        "id": 4,
        "name": "Pea",
        "emoji": "🫛",
        "status": "peak",
        "months": [5, 6],
        "co2": 0.1,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Protein", "Vitamin B1"],
    },
    {
        "id": 5,
        "name": "Rhubarb",
        "emoji": "🌿",
        "status": "season",
        "months": [4, 5, 6],
        "co2": 0.2,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Vitamin K", "Calcium"],
    },
    {
        "id": 6,
        "name": "Carrot",
        "emoji": "🥕",
        "status": "season",
        "months": [5, 6, 7, 8, 9],
        "co2": 0.2,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Beta-carotene", "Vitamin A"],
    },
    {
        "id": 7,
        "name": "Lettuce",
        "emoji": "🥬",
        "status": "peak",
        "months": [4, 5, 6, 7],
        "co2": 0.3,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Folate", "Vitamin K"],
    },
    {
        "id": 8,
        "name": "Blueberry",
        "emoji": "🫐",
        "status": "soon",
        "months": [6, 7, 8],
        "co2": 0.5,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Antioxidants", "Vitamin C"],
    },
    {
        "id": 9,
        "name": "Banana",
        "emoji": "🍌",
        "status": "out",
        "months": [],
        "co2": 0.9,
        "origin": "Ecuador",
        "local": False,
        "nutrients": ["Potassium", "Vitamin B6"],
    },
    {
        "id": 10,
        "name": "Avocado",
        "emoji": "🥑",
        "status": "out",
        "months": [],
        "co2": 2.5,
        "origin": "Mexico",
        "local": False,
        "nutrients": ["Healthy Fats", "Vitamin E"],
    },
    {
        "id": 11,
        "name": "Mango",
        "emoji": "🥭",
        "status": "out",
        "months": [],
        "co2": 1.9,
        "origin": "India",
        "local": False,
        "nutrients": ["Vitamin A", "Vitamin C"],
    },
    {
        "id": 12,
        "name": "Apple",
        "emoji": "🍎",
        "status": "out",
        "months": [8, 9, 10, 11],
        "co2": 0.4,
        "origin": "Poland",
        "local": False,
        "nutrients": ["Fiber", "Vitamin C"],
    },
]


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


def search_products(query: str, products: list[Product] | None = None) -> list[Product]:
    products_to_search = products or PRODUCTS
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
    return PRODUCTS


def get_all_produce() -> list[ProduceItem]:
    return ALL_PRODUCE


def get_seasonal_veggies() -> list[Product]:
    return PRODUCTS


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
