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


def origin_icon_class(country_code, local_country_code="SE"):
    return rx.cond(
        country_code == local_country_code,
        styles.product_card.origin_icon_local,
        styles.product_card.origin_icon_far,
    )


def origin_box_class(country_code, local_country_code="SE"):
    return rx.cond(
        country_code == local_country_code,
        styles.product_card.origin_box_local,
        styles.product_card.origin_box_far,
    )


def product_card(product, state=None) -> rx.Component:
    status = product["season_status"]
    nutrient = product["nutrients"][0]
    local_country_code = state.user_country_code if state else "SE"

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
            rx.button(
                rx.cond(
                    state.saved_product_ids.contains(product["id"]) if state else False,
                    app_icon("bookmark", "size-4 text-white fill-white", 3),
                    app_icon("bookmark", "size-4 text-[#555]", 3),
                ),
                on_click=state.toggle_saved_product(product["id"]) if state else rx.fragment(),
                aria_label="Save product",
                class_name=rx.cond(
                    state.saved_product_ids.contains(product["id"]) if state else False,
                    styles.product_card.save_button_overlay_active,
                    styles.product_card.save_button_overlay,
                ) if state else styles.product_card.save_button_overlay,
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
                    "map_pin",
                    origin_icon_class(product["best_country_code"], local_country_code),
                    3,
                ),
                rx.box(
                    rx.text(
                        product["best_country_name"],
                        class_name=styles.product_card.origin_title,
                    ),
                    rx.text(
                        "Lowest emissions origin",
                        class_name=styles.product_card.carbon_label,
                    ),
                    class_name=styles.product_card.origin_copy,
                ),
                rx.box(
                    rx.text(product["carbon_label"]),
                    rx.text("/ kg"),
                    class_name=styles.product_card.carbon_value,
                ),
                class_name=origin_box_class(
                    product["best_country_code"],
                    local_country_code,
                ),
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
