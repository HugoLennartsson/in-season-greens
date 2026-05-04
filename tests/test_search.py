from in_season_greens.data import (
    fuzzy_search_score,
    get_search_suggestions,
    search_products,
)


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
