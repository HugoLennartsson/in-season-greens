from in_season_greens.data import (
    ALL_PRODUCE,
    Country,
    filter_products,
    fetch_lowest_emission_origin,
    fuzzy_search_score,
    get_products,
    get_season_status,
    get_search_suggestions,
    search_products,
)
from in_season_greens.in_season_greens import State


def test_search_suggestions_use_all_produce_json():
    suggestions = get_search_suggestions("broc")

    assert suggestions[0]["name_en"] == "Broccoli"
    assert suggestions[0]["category"] == "vegetable"


def test_search_suggestions_find_misspelled_words():
    suggestions = get_search_suggestions("bluebery")

    assert suggestions[0]["name_en"] == "Blueberry"


def test_product_search_matches_misspellings():
    products = search_products("strawbery")

    assert [product["name_en"] for product in products] == ["Strawberry"]


def test_all_products_have_country_and_season_metadata():
    for product in ALL_PRODUCE:
        assert product["countries"]
        assert product["season_months"]
        assert all(code in Country.__members__ for code in product["countries"])


def test_country_filter_uses_country_enum_names():
    products = filter_products(get_products(), country_filter=Country.SE.value)

    assert products
    assert all("SE" in product["countries"] for product in products)


def test_nutrient_sort_orders_products_per_100g():
    products = filter_products(get_products(), nutrient_sort="Lowest calories")
    calories = [product["nutrients"][0]["calories"] for product in products]

    assert calories == sorted(calories)


def test_season_status_coming_soon_checks_next_two_months():
    assert get_season_status([7, 8], [], month=5) == "soon"
    assert get_season_status([8, 9], [], month=5) == "out"
    assert get_season_status([], [], month=5) == "unknown"


def test_emission_origin_prefers_nearby_country():
    code, name, carbon_kg = fetch_lowest_emission_origin(["SE", "ES"], 57.7, 12.0)

    assert code == "SE"
    assert name == "Sweden"
    assert carbon_kg > 0


def test_fuzzy_search_ignores_spaces_and_punctuation():
    assert fuzzy_search_score("sweet potato", "Sweet Potato") == 0
    assert fuzzy_search_score("sweet-potato", "Sweet Potato") == 0


def test_enter_key_closes_search_suggestions():
    state = State(_reflex_internal_init=True)

    state.set_search_query("apple")
    assert state.has_search_suggestions

    state.handle_search_key("Enter")

    assert not state.search_suggestions_open
    assert not state.has_search_suggestions


def test_selecting_suggestion_closes_search_suggestions():
    state = State(_reflex_internal_init=True)

    state.set_search_query("app")
    assert state.has_search_suggestions

    state.apply_search_suggestion("Apple")

    assert state.search_query == "Apple"
    assert not state.search_suggestions_open
    assert not state.has_search_suggestions


def test_search_submit_closes_search_suggestions():
    state = State(_reflex_internal_init=True)

    state.set_search_query("apple")
    assert state.has_search_suggestions

    state.submit_search()

    assert state.search_query == "apple"
    assert not state.search_suggestions_open
    assert not state.has_search_suggestions


def test_open_modal_selects_product_by_id():
    state = State(_reflex_internal_init=True)

    state.open_modal("apple")

    assert state.modal_open
    assert state.modal_product is not None
    assert state.modal_product["id"] == "apple"
    assert state.modal_product["name_en"] == "Apple"
