import reflex as rx

from .. import styles
from ..data import APP_NAME, get_nav_items
from .ui import FILTERS, app_icon, filter_button, hamburger_button, search_input
from ..location_state import LocationState


def desktop_header(state) -> rx.Component:
    return rx.el.header(
        rx.box(
            rx.box(
                APP_NAME,
                class_name=styles.navigation.desktop_logo,
            ),
            search_input(state),
            rx.hstack(
                *[filter_button(label, key) for key, label in FILTERS],
                class_name=styles.navigation.desktop_filters,
            ),
            hamburger_button(state.open_menu),
            class_name=styles.navigation.desktop_inner,
        ),
        class_name=styles.navigation.desktop_header,
    )


def mobile_header(state) -> rx.Component:
    return rx.el.header(
        rx.hstack(
            rx.hstack(
                app_icon("leaf", styles.navigation.mobile_logo_icon, 2),
                rx.text(APP_NAME, class_name=styles.navigation.mobile_logo),
                class_name=styles.navigation.mobile_logo_row,
            ),
            hamburger_button(state.open_menu),
            class_name=styles.navigation.mobile_inner,
        ),
        class_name=styles.navigation.mobile_header,
    )


def mobile_sticky_filters(state) -> rx.Component:
    return rx.box(
        search_input(state),
        rx.hstack(
            *[filter_button(label, key) for key, label in FILTERS],
            class_name=styles.navigation.mobile_filter_row,
        ),
        class_name=styles.navigation.mobile_filters,
    )


def drawer(state) -> rx.Component:
    nav_items = get_nav_items()

    return rx.fragment(
        rx.cond(
            state.menu_open,
            rx.box(
                on_click=state.close_menu, class_name=styles.navigation.drawer_overlay
            ),
            rx.fragment(),
        ),
        rx.box(
            rx.box(
                rx.hstack(
                    app_icon("leaf", styles.navigation.drawer_brand_icon, 2),
                    rx.text(APP_NAME, class_name=styles.navigation.drawer_brand),
                    class_name=styles.navigation.drawer_brand_row,
                ),
                rx.hstack(
                    app_icon("map_pin", styles.navigation.drawer_location_icon, 2),
                    rx.text(
                        LocationState.location_display,
                        class_name=styles.navigation.drawer_location,
                    ),
                    class_name=styles.navigation.drawer_location_row,
                ),
                class_name=styles.navigation.drawer_header,
            ),
            rx.vstack(
                *[
                    rx.hstack(
                        app_icon(item["icon"], styles.navigation.drawer_item_icon, 2),
                        rx.box(
                            rx.text(
                                item["label"],
                                class_name=styles.navigation.drawer_item_label,
                            ),
                            rx.text(
                                item["subtitle"],
                                class_name=styles.navigation.drawer_item_subtitle,
                            ),
                        ),
                        on_click=state.close_menu,
                        class_name=styles.navigation.drawer_item,
                    )
                    for item in nav_items
                ],
                class_name=styles.navigation.drawer_list,
            ),
            class_name=rx.cond(
                state.menu_open,
                styles.navigation.drawer_open,
                styles.navigation.drawer_closed,
            ),
        ),
    )
