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


def search_input() -> rx.Component:
    return rx.box(
        app_icon("search", styles.ui.search_icon, 2),
        rx.input(
            value="",
            read_only=True,
            placeholder="Search fruits & vegetables...",
            class_name=styles.ui.search_input,
        ),
        class_name=styles.ui.search_shell,
    )
