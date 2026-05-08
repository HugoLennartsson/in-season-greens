import reflex as rx

from .. import styles
from .ui import app_icon


def product_image_src(product_id) -> str | rx.Var:
    if isinstance(product_id, str):
        return f"/img/{product_id}.jpg"

    return rx.Var(
        _js_expr=f'("/img/" + {product_id._js_expr} + ".jpg")',
        _var_type=str,
    )


def status_label(status) -> rx.Component:
    return rx.match(
        status,
        ("peak", "PEAK SEASON"),
        ("season", "IN SEASON"),
        ("soon", "COMING SOON"),
        ("unknown", "UNKNOWN"),
        ("OUT OF SEASON"),
    )


def product_card(product) -> rx.Component:
    status = "unknown"

    return rx.box(
        rx.box(
            rx.image(
                src=product_image_src(product["id"]),
                alt=product["name_en"],
                class_name=styles.product_card.image_asset,
            ),
            rx.box(
                status_label(status),
                class_name=styles.product_card.badge(status),
            ),
            class_name=styles.product_card.image(status),
        ),
        rx.box(
            rx.heading(product["name_en"], class_name=styles.product_card.title),
            rx.text(
                "Season months unknown",
                class_name=styles.product_card.month_missing,
            ),
            rx.hstack(
                app_icon(
                    "map_pin",
                    styles.product_card.origin_icon_far,
                    3,
                ),
                rx.box(
                    rx.text(
                        "Origin unknown",
                        class_name=styles.product_card.origin_title,
                    ),
                    rx.text(
                        "Unknown Carbon Footprint",
                        class_name=styles.product_card.carbon_label,
                    ),
                    class_name=styles.product_card.origin_copy,
                ),
                rx.box(
                    rx.text("??? kg CO2e"),
                    rx.text("/ kg"),
                    class_name=styles.product_card.carbon_value,
                ),
                class_name=styles.product_card.origin_box_far,
            ),
            rx.flex(
                rx.box(
                    "???",
                    class_name=styles.product_card.nutrient,
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
