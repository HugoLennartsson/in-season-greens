import json
from pathlib import Path
from typing import TypedDict


class Product(TypedDict):
    id: str
    name: str
    status: str
    months: list[int]
    co2: float
    origin: str
    local: bool
    nutrients: list[str]
    image_src: str


class OverviewSignal(TypedDict):
    icon: str
    value: str
    label: str


class OverviewOutlook(TypedDict):
    icon: str
    text: str


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

ROOT_DIR = Path(__file__).resolve().parents[1]
ALL_PRODUCE_FILE = ROOT_DIR / "all_produce.json"


OVERVIEW_PRODUCTS: list[Product] = [
    {
        "id": "strawberry",
        "name": "Strawberry",
        "status": "peak",
        "months": [4, 5, 6, 7],
        "co2": 0.4,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Vitamin C", "Folate"],
        "image_src": "",
    },
    {
        "id": "tomato",
        "name": "Tomato",
        "status": "peak",
        "months": [5, 6, 7, 8],
        "co2": 0.7,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Vitamin C", "Lycopene"],
        "image_src": "",
    },
    {
        "id": "cucumber",
        "name": "Cucumber",
        "status": "season",
        "months": [5, 6, 7],
        "co2": 0.6,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Hydration", "Vitamin K"],
        "image_src": "",
    },
    {
        "id": "peas",
        "name": "Pea",
        "status": "peak",
        "months": [5, 6],
        "co2": 0.1,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Protein", "Vitamin B1"],
        "image_src": "",
    },
    {
        "id": "rhubarb",
        "name": "Rhubarb",
        "status": "season",
        "months": [4, 5, 6],
        "co2": 0.2,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Vitamin K", "Calcium"],
        "image_src": "",
    },
    {
        "id": "carrot",
        "name": "Carrot",
        "status": "season",
        "months": [5, 6, 7, 8, 9],
        "co2": 0.2,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Beta-carotene", "Vitamin A"],
        "image_src": "",
    },
    {
        "id": "lettuce",
        "name": "Lettuce",
        "status": "peak",
        "months": [4, 5, 6, 7],
        "co2": 0.3,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Folate", "Vitamin K"],
        "image_src": "",
    },
    {
        "id": "blueberry",
        "name": "Blueberry",
        "status": "soon",
        "months": [6, 7, 8],
        "co2": 0.5,
        "origin": "Sweden",
        "local": True,
        "nutrients": ["Antioxidants", "Vitamin C"],
        "image_src": "",
    },
    {
        "id": "banana",
        "name": "Banana",
        "status": "out",
        "months": [],
        "co2": 0.9,
        "origin": "Ecuador",
        "local": False,
        "nutrients": ["Potassium", "Vitamin B6"],
        "image_src": "",
    },
    {
        "id": "avocado",
        "name": "Avocado",
        "status": "out",
        "months": [],
        "co2": 2.5,
        "origin": "Mexico",
        "local": False,
        "nutrients": ["Healthy Fats", "Vitamin E"],
        "image_src": "",
    },
    {
        "id": "mango",
        "name": "Mango",
        "status": "out",
        "months": [],
        "co2": 1.9,
        "origin": "India",
        "local": False,
        "nutrients": ["Vitamin A", "Vitamin C"],
        "image_src": "",
    },
    {
        "id": "apple",
        "name": "Apple",
        "status": "out",
        "months": [8, 9, 10, 11],
        "co2": 0.4,
        "origin": "Poland",
        "local": False,
        "nutrients": ["Fiber", "Vitamin C"],
        "image_src": "",
    },
]


def get_all_produce_ids() -> set[str]:
    with ALL_PRODUCE_FILE.open() as produce_file:
        return {item["id"] for item in json.load(produce_file)}


def get_products() -> list[Product]:
    produce_ids = get_all_produce_ids()
    return [
        {
            **product,
            "image_src": f"/img/{product['id']}.jpg",
        }
        for product in OVERVIEW_PRODUCTS
        if product["id"] in produce_ids
    ]


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
