from datetime import datetime
import json
import re
from datetime import date
from enum import Enum
from pathlib import Path
from typing import TypedDict


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
    co2: float
    countries: list[str]
    country_names: list[str]
    countries_label: str
    carbon_kg: float
    carbon_label: str
    season_months: list[int]
    season_status: str
    season_label: str
    nutrients: list[NutritionFacts]


class NavItem(TypedDict):
    icon: str
    label: str
    subtitle: str


class FilterOption(TypedDict):
    value: str
    label: str


class Country(str, Enum):
    AF = "Afghanistan"
    AR = "Argentina"
    AU = "Australia"
    AZ = "Azerbaijan"
    BD = "Bangladesh"
    BE = "Belgium"
    BG = "Bulgaria"
    BR = "Brazil"
    BY = "Belarus"
    CA = "Canada"
    CH = "Switzerland"
    CI = "Cote d'Ivoire"
    CL = "Chile"
    CM = "Cameroon"
    CN = "China"
    CO = "Colombia"
    CR = "Costa Rica"
    CZ = "Czechia"
    DE = "Germany"
    DK = "Denmark"
    DO = "Dominican Republic"
    DZ = "Algeria"
    EC = "Ecuador"
    EE = "Estonia"
    EG = "Egypt"
    ES = "Spain"
    ET = "Ethiopia"
    FI = "Finland"
    FJ = "Fiji"
    FR = "France"
    GB = "United Kingdom"
    GE = "Georgia"
    GH = "Ghana"
    GR = "Greece"
    GT = "Guatemala"
    HN = "Honduras"
    ID = "Indonesia"
    IE = "Ireland"
    IL = "Israel"
    IN = "India"
    IR = "Iran"
    IT = "Italy"
    JP = "Japan"
    KE = "Kenya"
    KH = "Cambodia"
    KR = "South Korea"
    LA = "Laos"
    LK = "Sri Lanka"
    LT = "Lithuania"
    LV = "Latvia"
    MA = "Morocco"
    MG = "Madagascar"
    MW = "Malawi"
    MX = "Mexico"
    MY = "Malaysia"
    NG = "Nigeria"
    NL = "Netherlands"
    NO = "Norway"
    NP = "Nepal"
    NZ = "New Zealand"
    PA = "Panama"
    PE = "Peru"
    PH = "Philippines"
    PK = "Pakistan"
    PL = "Poland"
    PT = "Portugal"
    RO = "Romania"
    RS = "Serbia"
    RU = "Russia"
    SA = "Saudi Arabia"
    SE = "Sweden"
    TH = "Thailand"
    TR = "Turkey"
    TW = "Taiwan"
    TZ = "Tanzania"
    UA = "Ukraine"
    UG = "Uganda"
    US = "United States"
    UY = "Uruguay"
    UZ = "Uzbekistan"
    VN = "Vietnam"
    ZA = "South Africa"
    ZW = "Zimbabwe"


APP_NAME = "InSeasonGreens"
SORT_ASC = "asc"
SORT_DESC = "desc"
CATEGORY_FILTER_OPTIONS: list[FilterOption] = [
    {"value": "fruit", "label": "Fruit"},
    {"value": "vegetable", "label": "Vegetable"},
    {"value": "mushroom", "label": "Mushrooms"},
]
SEASON_FILTER_OPTIONS: list[FilterOption] = [
    {"value": "season", "label": "In season"},
    {"value": "soon", "label": "Coming soon"},
    {"value": "out", "label": "Out of season"},
    {"value": "unknown", "label": "Unknown season"},
]
SORT_FIELD_OPTIONS: list[FilterOption] = [
    {"value": "carbon_kg", "label": "CO2"},
    {"value": "serving_size_g", "label": "Serving size"},
    {"value": "calories", "label": "Calories"},
    {"value": "fat_total_g", "label": "Fat"},
    {"value": "fat_saturated_g", "label": "Sat fat"},
    {"value": "protein_g", "label": "Protein"},
    {"value": "sodium_mg", "label": "Sodium"},
    {"value": "potassium_mg", "label": "Potassium"},
    {"value": "cholesterol_mg", "label": "Cholesterol"},
    {"value": "carbohydrates_total_g", "label": "Carbs"},
    {"value": "fiber_g", "label": "Fiber"},
    {"value": "sugar_g", "label": "Sugar"},
]
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
MONTH_ABBREVIATIONS = [month[:3] for month in MONTHS]
CURRENT_MONTH = date.today().month

LOCATION = "Gothenburg"
COUNTRY = "SE"
SEARCH_SUGGESTION_LIMIT = 6
_ROOT = Path(__file__).resolve().parents[1]
_ALL_PRODUCE_PATH = _ROOT / "all_produce.json"

PRECIPITATION = "Normal"
AVG_TEMP = (16, 18)
HARVEST = "Favorable"


def get_nav_items() -> list[NavItem]:
    from in_season_greens.location_state import LocationState

    return [
        {"icon": "home", "label": "Home", "subtitle": "Browse all products"},
        {
            "icon": "map_pin",
            "label": "Local",
            "subtitle": f"Grown near {LocationState.city}",
        },
        {"icon": "wind", "label": "CO2 Tracker", "subtitle": "Compare CO2 per kg"},
        {
            "icon": "droplets",
            "label": "Water Usage",
            "subtitle": "Water per kg ratings",
        },
        {"icon": "bookmark", "label": "Saved", "subtitle": "Your saved products"},
        {"icon": "info", "label": "About", "subtitle": "Sources and methodology"},
    ]


def _country_name(code: str) -> str:
    try:
        return Country[code].value
    except KeyError:
        return code


def is_supported_country_code(code: str | None) -> bool:
    if not code:
        return False
    normalized_code = code.strip().upper()
    return normalized_code in Country.__members__


def normalize_country_code(code: str | None, fallback: str = COUNTRY) -> str:
    if is_supported_country_code(code):
        return code.strip().upper()
    return fallback


def get_country_name(code: str | None) -> str:
    return _country_name(normalize_country_code(code))


def _next_months(month: int, count: int = 2) -> set[int]:
    return {((month - 1 + offset) % 12) + 1 for offset in range(1, count + 1)}


def get_season_status(
    season_months: list[int],
    month: int = CURRENT_MONTH,
) -> str:
    if not season_months:
        return "unknown"
    if month in season_months:
        return "season"
    if _next_months(month) & set(season_months):
        return "soon"
    return "out"


def _format_month_range(start_month: int, end_month: int) -> str:
    if start_month == end_month:
        return MONTH_ABBREVIATIONS[start_month - 1]
    return (
        f"{MONTH_ABBREVIATIONS[start_month - 1]}-{MONTH_ABBREVIATIONS[end_month - 1]}"
    )


def format_month_window(months: list[int]) -> str:
    unique_months = sorted(set(months))
    if not unique_months:
        return "Unknown"
    if len(unique_months) == 12:
        return "Year-round"

    segments: list[tuple[int, int]] = []
    start = previous = unique_months[0]
    for month in unique_months[1:]:
        if month == previous + 1:
            previous = month
            continue
        segments.append((start, previous))
        start = previous = month
    segments.append((start, previous))

    if len(segments) > 1 and segments[0][0] == 1 and segments[-1][1] == 12:
        segments = [(segments[-1][0], segments[0][1]), *segments[1:-1]]

    return ", ".join(_format_month_range(start, end) for start, end in segments)


def _with_derived_fields(item: dict) -> ProduceItem:
    countries = item.get("countries", [])
    season_months = item.get("month", [])
    carbon_kg = float(item.get("co2") or 0.0)
    product = dict(item)
    product["countries"] = countries
    product["country_names"] = [_country_name(code) for code in countries]
    product["countries_label"] = ", ".join(product["country_names"]) or "Unknown"
    product["carbon_kg"] = carbon_kg
    product["carbon_label"] = (
        f"{carbon_kg:.2f} kg CO2e/kg" if carbon_kg else "CO2 unavailable"
    )
    product["season_months"] = season_months
    product["season_status"] = get_season_status(season_months)
    product["season_label"] = format_month_window(season_months)
    return product


def _load_all_produce() -> list[ProduceItem]:
    with _ALL_PRODUCE_PATH.open(encoding="utf-8") as produce_file:
        return [_with_derived_fields(item) for item in json.load(produce_file)]


ALL_PRODUCE: list[ProduceItem] = _load_all_produce()
COUNTRY_FILTER_OPTIONS: list[FilterOption] = [
    {"value": country.name, "label": country.value}
    for country in sorted(Country, key=lambda item: item.value)
]
COUNTRY_CODE_BY_NAME = {country.value: country.name for country in Country}


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


def _best_search_score(query: str, item: ProduceItem) -> int | None:
    searchable_values = [
        item["name_en"],
        item["category"],
        item["countries_label"],
    ]
    scores = [
        score + index * 15
        for index, value in enumerate(searchable_values)
        if (score := fuzzy_search_score(query, value)) is not None
    ]
    return min(scores) if scores else None


def get_search_suggestions(
    query: str, limit: int = SEARCH_SUGGESTION_LIMIT
) -> list[ProduceItem]:
    scored_items = [
        (score, item["name_en"], item)
        for item in ALL_PRODUCE
        if (score := _best_search_score(query, item)) is not None
    ]
    scored_items.sort(key=lambda match: (match[0], match[1]))
    return [item for _, __, item in scored_items[:limit]]


def search_products(
    query: str, products: list[ProduceItem] | None = None
) -> list[ProduceItem]:
    products_to_search = products if products is not None else get_products()
    if not normalize_search_text(query):
        return products_to_search

    scored_products = [
        (score, product["name_en"], product)
        for product in products_to_search
        if (score := _best_search_score(query, product)) is not None
    ]
    scored_products.sort(key=lambda match: (match[0], match[1]))
    return [product for _, __, product in scored_products]


def _nutrient_value(product: ProduceItem, nutrient_key: str) -> float:
    nutrient = product["nutrients"][0]
    return float(nutrient[nutrient_key])


def _sort_value(product: ProduceItem, sort_key: str) -> float:
    if sort_key == "carbon_kg":
        return float(product["carbon_kg"])
    return _nutrient_value(product, sort_key)


def _sort_products(
    products: list[ProduceItem],
    sort_key: str = "",
    sort_direction: str = "",
) -> list[ProduceItem]:
    if not sort_key or sort_direction not in {SORT_ASC, SORT_DESC}:
        return products
    reverse = sort_direction == SORT_DESC
    return sorted(
        products, key=lambda product: _sort_value(product, sort_key), reverse=reverse
    )


def filter_products(
    products: list[ProduceItem],
    query: str = "",
    country_filters: list[str] | None = None,
    season_filters: list[str] | None = None,
    category_filters: list[str] | None = None,
    local_only: bool = False,
    local_country_code: str | None = COUNTRY,
    sort_key: str = "",
    sort_direction: str = "",
) -> list[ProduceItem]:
    selected_countries = set(country_filters or [])
    selected_seasons = set(season_filters or [])
    selected_categories = set(category_filters or [])
    local_country = normalize_country_code(local_country_code)
    filtered_products = [
        _with_derived_fields(product)
        for product in products
        if not selected_countries or selected_countries & set(product["countries"])
    ]

    if local_only:
        filtered_products = [
            product
            for product in filtered_products
            if local_country in product["countries"]
        ]

    if selected_categories:
        filtered_products = [
            product
            for product in filtered_products
            if product["category"] in selected_categories
        ]

    if selected_seasons:
        filtered_products = [
            product
            for product in filtered_products
            if product["season_status"] in selected_seasons
        ]

    filtered_products = search_products(query, filtered_products)
    return _sort_products(filtered_products, sort_key, sort_direction)


def get_products() -> list[ProduceItem]:
    return ALL_PRODUCE


def get_all_produce() -> list[ProduceItem]:
    return ALL_PRODUCE


def get_seasonal_veggies() -> list[ProduceItem]:
    return get_products()


def get_current_month_name() -> str:
    return MONTHS[CURRENT_MONTH - 1]


def get_short_location() -> str:
    return f"{LOCATION}, {COUNTRY}"


def get_full_location() -> str:
    return f"{LOCATION}, {COUNTRY} · {get_current_month_name()}"


def get_temperature_range() -> str:
    from in_season_greens.location_state import LocationState

    return LocationState.avg_temp


def get_rain_outlook() -> str:
    from in_season_greens.location_state import LocationState

    return LocationState.rain_outlook


def get_harvest_outlook() -> str:
    from in_season_greens.location_state import LocationState

    return LocationState.harvest_outlook


def get_overview_signals() -> list[OverviewSignal]:
    from in_season_greens.location_state import LocationState

    return [
        {"icon": "info", "value": get_current_month_name(), "label": "Current month"},
        {
            "icon": "thermometer",
            "value": get_temperature_range(),
            "label": "Avg temp normal",
        },
        {"icon": "cloud_rain", "value": get_rain_outlook(), "label": "Rain outlook"},
        {
            "icon": "sprout",
            "value": get_harvest_outlook(),
            "label": "Harvest outlook",
        },  # ← was HARVEST
    ]


def get_season_outlook() -> list[OverviewOutlook]:
    from in_season_greens.location_state import LocationState

    return [
        {
            "icon": "thermometer",
            "text": f"Average temperature is within {LocationState.location_display}'s normal {get_current_month_name()} range.",
        },
        {
            "icon": "cloud_rain",
            "text": f"Rain outlook is {get_rain_outlook()} for outdoor leafy greens and field crops.",
        },
        {
            "icon": "sprout",
            "text": f"Harvest outlook is {get_harvest_outlook().lower()} for local seasonal produce.",
        },
        {
            "icon": "leaf",
            "text": "Season status is based on product season windows and the current month.",
        },
    ]


def get_catalog_label(count: int) -> str:
    if count == 1:
        return "1 product"
    return f"{count} products"
