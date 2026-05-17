from in_season_greens.data import (
    fuzzy_search_score,
    get_search_suggestions,
    order_products,
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


def test_product_order_can_sort_by_name_ascending_and_descending():
    products = [
        {"id": "pear", "name_en": "Pear", "category": "fruit", "nutrients": []},
        {"id": "apple", "name_en": "Apple", "category": "fruit", "nutrients": []},
        {"id": "banana", "name_en": "Banana", "category": "fruit", "nutrients": []},
    ]

    assert [product["name_en"] for product in order_products(products, "name_asc")] == [
        "Apple",
        "Banana",
        "Pear",
    ]
    assert [product["name_en"] for product in order_products(products, "name_desc")] == [
        "Pear",
        "Banana",
        "Apple",
    ]


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


def test_state_orders_filtered_products_by_selected_order():
    state = State(_reflex_internal_init=True)

    state.set_product_order("Name Z-A")

    assert state.product_order_key == "name_desc"
    assert state.product_order_label == "Name Z-A"
    assert state.filtered_products[0]["name_en"] == "Zucchini"


def test_open_modal_selects_product_by_id():
    state = State(_reflex_internal_init=True)

    state.open_modal("apple")

    assert state.modal_open
    assert state.modal_product is not None
    assert state.modal_product["id"] == "apple"
    assert state.modal_product["name_en"] == "Apple"
