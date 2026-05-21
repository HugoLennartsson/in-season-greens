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
                on_click=state.close_menu,
                class_name=styles.navigation.drawer_overlay,
            ),
            rx.fragment(),
        ),
        rx.box(
            rx.box(
                rx.hstack(
                    rx.hstack(
                        app_icon("leaf", styles.navigation.drawer_brand_icon, 2),
                        rx.text(APP_NAME, class_name=styles.navigation.drawer_brand),
                        class_name=styles.navigation.drawer_brand_row,
                    ),
                    rx.icon(
                        tag="x",
                        on_click=state.close_menu,
                        cursor="pointer",
                        size=22,
                        color="var(--gray-11)",
                        _hover={"color": "var(--gray-12)"},
                    ),
                    justify="between",
                    align="center",
                    width="100%",
                    margin_bottom="15px",
                ),
                rx.vstack(
                    rx.box(
                        rx.hstack(
                            app_icon(
                                "map_pin",
                                styles.navigation.drawer_location_icon,
                                2,
                            ),
                            rx.input(
                                value=LocationState.typed_city,
                                placeholder="Type city...",
                                on_change=LocationState.set_typed_city,
                                on_key_down=LocationState.handle_key_down,
                                variant="soft",
                                size="1",
                                width="100%",
                                color_scheme="gray",
                                style={
                                    "color": "#FFFFFF",
                                    "background_color": "rgba(255,255,255,0.1)",
                                },
                            ),
                            rx.icon(
                                tag="locate-fixed",
                                on_click=LocationState.get_location,
                                cursor="pointer",
                                size=18,
                            ),
                            align="center",
                            width="100%",
                        ),
                        # Suggestions Dropdown
                        rx.cond(
                            LocationState.suggestions != [],
                            rx.vstack(
                                rx.foreach(
                                    LocationState.suggestions,
                                    lambda city: rx.box(
                                        rx.text(
                                            city,
                                            color="#1C2024",
                                            font_weight="500",
                                            font_size="13px",
                                        ),
                                        on_click=LocationState.select_suggestion(city),
                                        padding="10px 14px",
                                        cursor="pointer",
                                        width="100%",
                                        _hover={"background_color": "#F1F3F5"},
                                    ),
                                ),
                                position="absolute",
                                top="100%",
                                left="0",
                                width="100%",
                                background_color="#FFFFFF",
                                border="1px solid #E6E8EA",
                                border_radius="8px",
                                box_shadow="0px 4px 20px rgba(0,0,0,0.08)",
                                z_index=9999,
                                spacing="0",
                                align_items="start",
                                margin_top="6px",
                            ),
                        ),
                        position="relative",
                        width="100%",
                    ),
                    rx.cond(
                        LocationState.error != "",
                        rx.text(
                            LocationState.error,
                            color="red",
                            font_size="10px",
                        ),
                    ),
                    class_name=styles.navigation.drawer_location_row,
                    overflow="visible",
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
