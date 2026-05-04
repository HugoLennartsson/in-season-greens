import reflex as rx

from .. import styles


FILTERS = [
    ("all", "All"),
    ("peak", "Peak"),
    ("season", "In Season"),
    ("out", "Out of Season"),
]


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


def filter_button(label: str, key: str) -> rx.Component:
    return rx.button(
        label,
        class_name=styles.ui.filter_active if key == "all" else styles.ui.filter_inactive,
    )


def search_suggestion_button(state, suggestion) -> rx.Component:
    return rx.button(
        rx.hstack(
            app_icon("search", styles.ui.search_suggestion_icon, 2),
            rx.box(
                rx.text(suggestion["name_en"], class_name=styles.ui.search_suggestion_name),
                rx.text(suggestion["category"], class_name=styles.ui.search_suggestion_category),
                class_name=styles.ui.search_suggestion_copy,
            ),
            class_name=styles.ui.search_suggestion_inner,
        ),
        on_mouse_down=state.apply_search_suggestion(suggestion["name_en"]),
        class_name=styles.ui.search_suggestion,
    )


def search_input(state) -> rx.Component:
    return rx.box(
        app_icon("search", styles.ui.search_icon, 2),
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
