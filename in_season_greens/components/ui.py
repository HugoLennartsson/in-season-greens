import reflex as rx

from .. import styles
from ..data import (
    COUNTRY_FILTER_OPTIONS,
    NUTRIENT_SORT_OPTIONS,
    SEASON_FILTER_OPTIONS,
)


def app_icon(tag: str, class_name: str = "size-4", stroke_width: int = 2) -> rx.Component:
    return rx.icon(tag=tag, stroke_width=stroke_width, class_name=class_name)


def hamburger_button(on_click) -> rx.Component:
    return rx.button(
        rx.box(class_name=styles.ui.hamburger_line),
        rx.box(class_name=styles.ui.hamburger_line),
        rx.box(class_name=styles.ui.hamburger_line),
        on_click=on_click,
        aria_label="Open menu",
        class_name=styles.ui.hamburger_button,
    )


def filter_toggle_button(state) -> rx.Component:
    return rx.button(
        app_icon("sliders-horizontal", styles.ui.filter_button_icon, 2),
        "Filter",
        rx.cond(
            state.has_active_filters,
            rx.box(class_name=styles.ui.filter_active_dot),
            rx.fragment(),
        ),
        on_click=state.toggle_filters,
        aria_label="Open filters",
        class_name=styles.ui.filter_button,
    )


def filter_field(label: str, items: list[str], value, on_change) -> rx.Component:
    return rx.box(
        rx.text(label, class_name=styles.ui.filter_field_label),
        rx.select(
            items,
            value=value,
            on_change=on_change,
            class_name=styles.ui.filter_select,
        ),
        class_name=styles.ui.filter_field,
    )


def filter_drawer(state) -> rx.Component:
    return rx.fragment(
        rx.cond(
            state.filters_open,
            rx.box(
                on_click=state.close_filters,
                class_name=styles.ui.filter_overlay,
            ),
            rx.fragment(),
        ),
        rx.box(
            rx.hstack(
                rx.hstack(
                    app_icon("sliders-horizontal", styles.ui.filter_drawer_icon, 2),
                    rx.heading("Filters", class_name=styles.ui.filter_drawer_title),
                    class_name=styles.ui.filter_drawer_title_row,
                ),
                rx.button(
                    app_icon("x", styles.ui.filter_close_icon, 2),
                    on_click=state.close_filters,
                    aria_label="Close filters",
                    class_name=styles.ui.filter_close_button,
                ),
                class_name=styles.ui.filter_drawer_header,
            ),
            rx.vstack(
                filter_field(
                    "Country",
                    COUNTRY_FILTER_OPTIONS,
                    state.country_filter,
                    state.set_country_filter,
                ),
                filter_field(
                    "Season",
                    SEASON_FILTER_OPTIONS,
                    state.season_filter,
                    state.set_season_filter,
                ),
                filter_field(
                    "Nutrition",
                    NUTRIENT_SORT_OPTIONS,
                    state.nutrient_sort,
                    state.set_nutrient_sort,
                ),
                class_name=styles.ui.filter_drawer_fields,
            ),
            rx.cond(
                state.has_active_filters,
                rx.button(
                    app_icon("rotate-ccw", styles.ui.filter_reset_icon, 2),
                    "Reset filters",
                    on_click=state.clear_filters,
                    class_name=styles.ui.filter_reset_button,
                ),
                rx.fragment(),
            ),
            class_name=rx.cond(
                state.filters_open,
                styles.ui.filter_drawer_open,
                styles.ui.filter_drawer_closed,
            ),
        ),
    )


def search_suggestion_button(state, suggestion) -> rx.Component:
    return rx.el.button(
        rx.hstack(
            app_icon("search", styles.ui.search_suggestion_icon, 2),
            rx.box(
                rx.text(suggestion["name_en"], class_name=styles.ui.search_suggestion_name),
                rx.text(suggestion["category"], class_name=styles.ui.search_suggestion_category),
                class_name=styles.ui.search_suggestion_copy,
            ),
            class_name=styles.ui.search_suggestion_inner,
        ),
        type="button",
        on_mouse_down=state.apply_search_suggestion(suggestion["name_en"]),
        class_name=styles.ui.search_suggestion,
    )


def search_input(state) -> rx.Component:
    return rx.box(
        rx.input(
            value=state.search_query,
            on_change=state.set_search_query,
            on_focus=state.open_search_suggestions,
            on_blur=state.close_search_suggestions,
            on_key_down=state.handle_search_key,
            placeholder="Search fruits & vegetables...",
            class_name=styles.ui.search_input,
        ),
        rx.cond(
            state.has_search_query,
            rx.button(
                app_icon("x", styles.ui.search_clear_icon, 2),
                on_click=state.clear_search,
                aria_label="Clear search",
                class_name=styles.ui.search_clear_button,
            ),
            rx.fragment(),
        ),
        rx.button(
            app_icon("search", styles.ui.search_submit_icon, 2),
            on_mouse_down=state.submit_search,
            aria_label="Search",
            class_name=styles.ui.search_submit_button,
        ),
        rx.cond(
            state.has_search_suggestions,
            rx.box(
                rx.foreach(
                    state.search_suggestions,
                    lambda suggestion: search_suggestion_button(state, suggestion),
                ),
                class_name=styles.ui.search_suggestions,
            ),
            rx.fragment(),
        ),
        class_name=styles.ui.search_shell,
    )


def get_category_emoji(category) -> str | rx.Component:
    """Return an emoji based on product category"""
    if isinstance(category, str):
        emoji_map = {
            "fruit": "🍎",
            "vegetable": "🥬",
            "leafy": "🥬",
            "root": "🥕",
            "berry": "🫐",
            "citrus": "🍊",
            "tropical": "🥑",
        }
        return emoji_map.get(category.lower(), "🌱")

    return rx.match(
        category,
        ("fruit", "🍎"),
        ("vegetable", "🥬"),
        ("leafy", "🥬"),
        ("root", "🥕"),
        ("berry", "🫐"),
        ("citrus", "🍊"),
        ("tropical", "🥑"),
        ("🌱"),
    )


def product_modal(state) -> rx.Component:
    """Product detail modal that appears when 'Show info' is clicked"""
    product = state.modal_product

    def nutrition_fact(label: str, value, unit: str = "") -> rx.Component:
        return rx.box(
            rx.text(label, class_name="text-[11px] font-black uppercase tracking-wide text-[#728072]"),
            rx.text(
                value,
                rx.cond(unit != "", f" {unit}", ""),
                class_name="text-lg font-black text-[#151915]",
            ),
            class_name="rounded-lg border border-[#e0e5dc] bg-[#f7f9f5] px-3 py-2",
        )

    def product_fact(label: str, value) -> rx.Component:
        return rx.box(
            rx.text(label, class_name="text-[10px] font-black uppercase tracking-wide text-[#728072]"),
            rx.text(
                value,
                class_name="break-words text-sm font-black leading-snug text-[#151915]",
            ),
            class_name="rounded-lg border border-[#e0e5dc] bg-white px-3 py-2",
        )

    def nutrient_panel(nutrient) -> rx.Component:
        return rx.grid(
            nutrition_fact("Calories", nutrient["calories"], "kcal"),
            nutrition_fact("Protein", nutrient["protein_g"], "g"),
            nutrition_fact("Carbs", nutrient["carbohydrates_total_g"], "g"),
            nutrition_fact("Fiber", nutrient["fiber_g"], "g"),
            nutrition_fact("Sugar", nutrient["sugar_g"], "g"),
            nutrition_fact("Fat", nutrient["fat_total_g"], "g"),
            nutrition_fact("Sodium", nutrient["sodium_mg"], "mg"),
            nutrition_fact("Potassium", nutrient["potassium_mg"], "mg"),
            class_name="grid grid-cols-2 gap-2 md:grid-cols-4",
        )

    return rx.cond(
        state.modal_open & (product != None),
        rx.box(
            rx.box(
                on_click=state.close_modal,
                class_name="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm",
            ),
            rx.box(
                rx.box(
                    rx.hstack(
                        rx.hstack(
                            rx.text(
                                get_category_emoji(product["category"]),
                                class_name="text-4xl leading-none",
                            ),
                            rx.box(
                                rx.heading(
                                    product["name_en"],
                                    class_name="text-3xl font-black leading-tight text-[#151915]",
                                ),
                                rx.text(
                                    product["category"],
                                    class_name="text-xs font-black uppercase tracking-wide text-[#728072]",
                                ),
                                class_name="min-w-0",
                            ),
                            class_name="min-w-0 flex-1 items-center gap-3",
                        ),
                        rx.button(
                            app_icon("x", "size-6 text-[#555]", 2),
                            on_click=state.close_modal,
                            class_name="rounded-lg p-2 hover:bg-[#e7ede4]",
                            aria_label="Close modal",
                        ),
                        class_name="w-full items-start gap-4",
                    ),
                    rx.box(
                        rx.image(
                            src=rx.Var(
                                _js_expr=f'("/img/" + {product["id"]._js_expr} + ".jpg")',
                                _var_type=str,
                            ),
                            alt=product["name_en"],
                            class_name="h-full w-full object-cover",
                        ),
                        class_name="mt-6 aspect-[16/9] overflow-hidden rounded-lg bg-[#dfe8dc]",
                    ),
                    rx.box(
                        rx.heading("Season and sourcing", class_name="mb-3 text-lg font-black text-[#151915]"),
                        rx.grid(
                            product_fact("Season", product["season_label"]),
                            product_fact("Peak", product["peak_label"]),
                            product_fact("Lowest emissions", product["best_country_name"]),
                            product_fact("Countries", product["countries_label"]),
                            class_name="grid grid-cols-1 gap-2 md:grid-cols-2",
                        ),
                        class_name="mt-6",
                    ),
                    rx.box(
                        rx.heading("Nutrition per 100g", class_name="mb-3 text-lg font-black text-[#151915]"),
                        rx.foreach(product["nutrients"], nutrient_panel),
                        class_name="mt-6",
                    ),
                    class_name="w-full max-h-[90vh] overflow-y-auto",
                ),
                class_name="fixed left-1/2 top-1/2 z-50 w-11/12 max-w-3xl -translate-x-1/2 -translate-y-1/2 rounded-2xl bg-white p-5 shadow-2xl md:p-6",
            ),
            class_name="fixed inset-0 z-40",
        ),
        rx.fragment(),
    )
