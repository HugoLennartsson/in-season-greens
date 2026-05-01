import reflex as rx

from .. import styles
from ..data import CURRENT_MONTH
from .ui import app_icon


def status_label(status) -> rx.Component:
    return rx.match(
        status,
        ("peak", "PEAK SEASON"),
        ("season", "IN SEASON"),
        ("soon", "COMING SOON"),
        ("OUT OF SEASON"),
    )


def carbon_label(co2) -> rx.Component:
    return rx.cond(
        co2 <= 0.7,
        "Low Carbon Footprint",
        rx.cond(co2 <= 1.5, "Medium Carbon Footprint", "Huge Carbon Footprint"),
    )


def month_name(month) -> rx.Component:
    return rx.match(
        month,
        (0, "Jan"),
        (1, "Feb"),
        (2, "Mar"),
        (3, "Apr"),
        (4, "May"),
        (5, "Jun"),
        (6, "Jul"),
        (7, "Aug"),
        (8, "Sep"),
        (9, "Oct"),
        (10, "Nov"),
        ("Dec"),
    )


def season_months(product, compact: bool = False) -> rx.Component:
    pill_class = (
        "rounded-lg px-2 py-0.5 text-[9px] font-black"
        if compact
        else "rounded-lg px-3 py-1 text-xs font-bold"
    )
    return rx.cond(
        product["local"],
        rx.flex(
            rx.foreach(
                product["months"],
                lambda month: rx.box(
                    month_name(month),
                    class_name=rx.cond(
                        month == CURRENT_MONTH,
                        f"{pill_class} {styles.product_card.month_current}",
                        f"{pill_class} {styles.product_card.month_default}",
                    ),
                ),
            ),
            class_name=styles.product_card.months,
        ),
        rx.text(
            "Can't grow locally",
            class_name=styles.product_card.month_missing,
        ),
    )


def product_card(product) -> rx.Component:
    is_in = (product["status"] == "peak") | (product["status"] == "season")
    return rx.box(
        rx.box(
            rx.text(product["emoji"], class_name=styles.product_card.emoji),
            rx.box(status_label(product["status"]), class_name=styles.product_card.badge(product["status"])),
            class_name=styles.product_card.image(product["status"]),
        ),
        rx.box(
            rx.heading(product["name"], class_name=styles.product_card.title),
            season_months(product, compact=True),
            rx.hstack(
                app_icon(
                    "map_pin",
                    rx.cond(is_in, styles.product_card.origin_icon_local, styles.product_card.origin_icon_far),
                    3,
                ),
                rx.box(
                    rx.text(
                        rx.cond(product["local"], "Grown Locally", rx.fragment("Grown in ", product["origin"])),
                        class_name=styles.product_card.origin_title,
                    ),
                    rx.text(carbon_label(product["co2"]), class_name=styles.product_card.carbon_label),
                    class_name=styles.product_card.origin_copy,
                ),
                rx.box(
                    rx.text(product["co2"], " kg CO2e"),
                    rx.text("/ kg"),
                    class_name=styles.product_card.carbon_value,
                ),
                class_name=rx.cond(
                    is_in,
                    styles.product_card.origin_box_local,
                    styles.product_card.origin_box_far,
                ),
            ),
            rx.flex(
                rx.foreach(
                    product["nutrients"],
                    lambda nutrient: rx.box(
                        nutrient,
                        class_name=styles.product_card.nutrient,
                    ),
                ),
                class_name=styles.product_card.nutrients,
            ),
            rx.hstack(
                rx.button(
                    app_icon("bookmark", "size-3 text-[#555]", 3),
                    "Save",
                    class_name=styles.product_card.save_button,
                ),
                rx.button(
                    app_icon("info", "size-3 text-white", 3),
                    "Show info",
                    class_name=styles.product_card.info_button,
                ),
                class_name=styles.product_card.actions,
            ),
            class_name=styles.product_card.body,
        ),
        class_name=styles.product_card.card,
    )
