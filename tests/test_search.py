from in_season_greens.data import (
    ALL_PRODUCE,
    Country,
    filter_products,
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
        assert product["co2"]
        assert all(code in Country.__members__ for code in product["countries"])


def test_country_filter_uses_country_enum_names():
    products = filter_products(get_products(), country_filters=[Country.SE.name])

    assert products
    assert all("SE" in product["countries"] for product in products)


def test_local_only_filter_uses_location_country():
    products = filter_products(
        get_products(),
        local_only=True,
        local_country_code=Country.ES.name,
    )

    assert products
    assert all("ES" in product["countries"] for product in products)


def test_local_only_filter_falls_back_to_sweden_for_unknown_country():
    products = filter_products(
        get_products(),
        local_only=True,
        local_country_code="XX",
    )

    assert products
    assert all("SE" in product["countries"] for product in products)


def test_nutrient_sort_orders_products_per_100g():
    products = filter_products(get_products(), sort_key="calories", sort_direction="asc")
    calories = [product["nutrients"][0]["calories"] for product in products]

    assert calories == sorted(calories)


def test_carbon_sort_orders_products_by_emissions():
    products = filter_products(get_products(), sort_key="carbon_kg", sort_direction="asc")
    carbon_values = [product["carbon_kg"] for product in products]

    assert carbon_values == sorted(carbon_values)


def test_multi_filters_combine_categories_countries_and_seasons():
    products = filter_products(
        get_products(),
        country_filters=["SE"],
        category_filters=["vegetable"],
        season_filters=["season"],
    )

    assert products
    assert all("SE" in product["countries"] for product in products)
    assert all(product["category"] == "vegetable" for product in products)
    assert all(product["season_status"] == "season" for product in products)


def test_mushroom_category_filter_is_supported():
    products = filter_products(get_products(), category_filters=["mushroom"])

    assert [product["id"] for product in products] == [
        "chanterelle",
        "funnel_chanterelle",
    ]


def test_season_status_coming_soon_checks_next_two_months():
    assert get_season_status([7, 8], month=5) == "soon"
    assert get_season_status([8, 9], month=5) == "out"
    assert get_season_status([], month=5) == "unknown"


def test_products_use_hardcoded_co2_from_json():
    products = {product["id"]: product for product in get_products()}

    assert products["apple"]["carbon_kg"] == 0.2
    assert products["apple"]["carbon_label"] == "0.20 kg CO2e/kg"
    assert products["apricot"]["carbon_kg"] == 0.48


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


def test_state_local_only_uses_detected_country():
    state = State(_reflex_internal_init=True)

    state.toggle_local_only()
    state.set_user_location(40.4168, -3.7038, "es")

    assert state.user_country_code == "ES"
    assert not state.user_country_is_fallback
    assert state.local_country_label == "Spain"
    assert state.has_active_filters
    assert state.filtered_products
    assert all("ES" in product["countries"] for product in state.filtered_products)


def test_state_local_country_label_shows_sweden_fallback():
    state = State(_reflex_internal_init=True)

    assert state.user_country_code == "SE"
    assert state.user_country_is_fallback
    assert state.local_country_label == "Sweden (fallback)"

    state.set_user_location(59.3293, 18.0686, "se")

    assert state.user_country_code == "SE"
    assert not state.user_country_is_fallback
    assert state.local_country_label == "Sweden"


def test_open_modal_selects_product_by_id():
    state = State(_reflex_internal_init=True)

    state.open_modal("apple")

    assert state.modal_open
    assert state.modal_product is not None
    assert state.modal_product["id"] == "apple"
    assert state.modal_product["name_en"] == "Apple"
