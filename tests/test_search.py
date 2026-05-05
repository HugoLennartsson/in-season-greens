from in_season_greens.data import (
    fuzzy_search_score,
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

    assert [product["name"] for product in products] == ["Strawberry"]


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
