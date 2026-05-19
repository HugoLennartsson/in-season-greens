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
        ("season", "IN SEASON"),
        ("soon", "COMING SOON"),
        ("unknown", "UNKNOWN"),
        ("OUT OF SEASON"),
    )


def product_card(product, state=None) -> rx.Component:
    status = product["season_status"]
    nutrient = product["nutrients"][0]

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
                product["season_label"],
                class_name=styles.product_card.season_label,
            ),
            rx.hstack(
                app_icon(
                    "wind",
                    styles.product_card.emissions_icon,
                    3,
                ),
                rx.box(
                    rx.text(
                        "Lowest emissions",
                        class_name=styles.product_card.emissions_title,
                    ),
                    class_name=styles.product_card.emissions_copy,
                ),
                rx.box(
                    rx.text(product["carbon_label"]),
                    class_name=styles.product_card.emissions_value,
                ),
                class_name=styles.product_card.emissions_box,
            ),
            rx.flex(
                rx.box(
                    "100g",
                    class_name=styles.product_card.nutrient,
                ),
                rx.box(
                    nutrient["calories"],
                    " kcal",
                    class_name=styles.product_card.nutrient,
                ),
                rx.box(
                    nutrient["fiber_g"],
                    "g fiber",
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
                    on_click=state.open_modal(product["id"]) if state else rx.fragment(),
                    class_name=styles.product_card.info_button,
                ),
                class_name=styles.product_card.actions,
            ),
            class_name=styles.product_card.body,
        ),
        class_name=styles.product_card.card,
    )
