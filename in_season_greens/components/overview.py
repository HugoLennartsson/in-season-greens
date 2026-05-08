import reflex as rx

from .. import styles
from ..location_state import LocationState
from ..data import (
    get_current_month_name,
    get_overview_signals,
    get_season_outlook,
)
from .ui import app_icon


def overview_section() -> rx.Component:
    signals = get_overview_signals()
    outlook = get_season_outlook()

    return rx.el.section(
        rx.box(
            rx.hstack(
                rx.hstack(
                    app_icon("leaf", styles.overview.title_icon, 2),
                    rx.heading(
                        "Growing Near You",
                        class_name=styles.overview.title,
                    ),
                    class_name=styles.overview.title_row,
                ),
                rx.box(
                    rx.hstack(
                        app_icon("map_pin", styles.overview.location_icon, 2),
                        rx.text(
                            LocationState.location_display,
                            class_name=styles.overview.location_text,
                        ),
                        class_name=styles.overview.location_row,
                    ),
                    rx.text(get_current_month_name(), class_name=styles.overview.month),
                    class_name=styles.overview.location_box,
                ),
                class_name=styles.overview.header,
            ),
            rx.grid(
                rx.box(
                    rx.text(
                        "REGIONAL SEASON SIGNALS",
                        class_name=styles.overview.section_label_green,
                    ),
                    rx.grid(
                        *[
                            rx.hstack(
                                app_icon(
                                    signal["icon"], styles.overview.signal_icon, 2
                                ),
                                rx.box(
                                    rx.text(
                                        signal["value"],
                                        class_name=styles.overview.signal_value,
                                    ),
                                    rx.text(
                                        signal["label"],
                                        class_name=styles.overview.signal_label,
                                    ),
                                    class_name=styles.overview.signal_copy,
                                ),
                                class_name=styles.overview.signal_row,
                            )
                            for signal in signals
                        ],
                        class_name=styles.overview.signals_grid,
                    ),
                    class_name=styles.overview.signals_panel,
                ),
                rx.box(
                    rx.text(
                        "SEASON OUTLOOK",
                        class_name=styles.overview.section_label_light,
                    ),
                    rx.grid(
                        *[
                            rx.hstack(
                                app_icon(item["icon"], styles.overview.outlook_icon, 2),
                                rx.text(
                                    item["text"],
                                    class_name=styles.overview.outlook_text,
                                ),
                                class_name=styles.overview.outlook_row,
                            )
                            for item in outlook
                        ],
                        class_name=styles.overview.outlook_grid,
                    ),
                    class_name=styles.overview.outlook_panel,
                ),
                class_name=styles.overview.content_grid,
            ),
            class_name=styles.overview.shell,
        ),
        class_name=styles.overview.section,
    )
