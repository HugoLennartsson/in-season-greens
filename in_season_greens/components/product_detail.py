import reflex as rx

from .. import styles
from ..data import CURRENT_MONTH, APP_NAME, get_full_location, get_nav_items
from .ui import app_icon, FILTERS, filter_button, hamburger_button, search_input, get_category_emoji
from .product_card import carbon_label, month_name, status_label


def desktop_header_detail() -> rx.Component:
    return rx.el.header(
        rx.box(
            rx.box(
                APP_NAME,
                class_name=styles.navigation.desktop_logo,
            ),
            search_input(),
            rx.hstack(
                *[filter_button(label, key) for key, label in FILTERS],
                class_name=styles.navigation.desktop_filters,
            ),
            class_name=styles.navigation.desktop_inner,
        ),
        class_name=styles.navigation.desktop_header,
    )


def mobile_header_detail() -> rx.Component:
    return rx.el.header(
        rx.hstack(
            rx.hstack(
                app_icon("leaf", styles.navigation.mobile_logo_icon, 2),
                rx.text(APP_NAME, class_name=styles.navigation.mobile_logo),
                class_name=styles.navigation.mobile_logo_row,
            ),
            class_name=styles.navigation.mobile_inner,
        ),
        class_name=styles.navigation.mobile_header,
    )


def product_detail_view(product, go_back) -> rx.Component:
    if product is None:
        return rx.fragment(
            desktop_header_detail(),
            mobile_header_detail(),
            rx.box(
                rx.heading("Product not found", class_name="text-3xl font-bold mb-6 text-[#1f3d1f]"),
                rx.button(
                    "Back to catalog",
                    on_click=go_back,
                    class_name="px-6 py-3 rounded-full bg-[#2db34a] text-white font-black hover:bg-[#1f6f36]",
                ),
                class_name="min-h-[calc(100vh-72px)] flex flex-col items-center justify-center bg-[#eef6e8] px-4",
            ),
        )

    is_in = (product["status"] == "peak") | (product["status"] == "season")

    return rx.fragment(
        desktop_header_detail(),
        mobile_header_detail(),
        rx.box(
        rx.box(
            rx.button(
                rx.hstack(app_icon("arrow_back", "size-4", 3), rx.text("Back")),
                on_click=go_back,
                class_name="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#1f5f2f] text-white hover:bg-[#163f1e]",
            ),
            rx.heading(product["name"], class_name="text-5xl font-extrabold mt-6"),
            rx.text(
                rx.cond(
                    product["local"],
                    "A locally sourced seasonal product.",
                    rx.fragment("Imported from ", product["origin"], "."),
                ),
                class_name="text-lg text-slate-600 mt-2",
            ),
            class_name="max-w-5xl mx-auto py-8 px-4",
        ),
        rx.grid(
            rx.box(
                rx.text(get_category_emoji(product["category"]), class_name="text-[6rem] leading-none mb-4"),
                rx.box(status_label(product["status"]), class_name=styles.product_card.badge(product["status"])),
                rx.text(
                    carbon_label(product["co2"]),
                    class_name="mt-6 text-xl font-semibold text-slate-800",
                ),
                rx.text(f"{product['co2']} kg CO2e per kg", class_name="text-sm text-slate-500 mt-2"),
                rx.box(
                    rx.heading("Origin", class_name="text-xl font-semibold mt-8 mb-3"),
                    rx.text(product["origin"], class_name="text-base text-slate-700"),
                    rx.heading("Availability", class_name="text-xl font-semibold mt-8 mb-3"),
                    rx.flex(
                        rx.foreach(
                            product["months"],
                            lambda month: rx.box(
                                month_name(month),
                                class_name=rx.cond(
                                    month == CURRENT_MONTH,
                                    "rounded-full px-4 py-2 bg-emerald-100 text-emerald-800 font-bold",
                                    "rounded-full px-4 py-2 bg-slate-100 text-slate-700",
                                ),
                            ),
                        ),
                        class_name="flex flex-wrap gap-2",
                    ),
                    class_name="rounded-3xl bg-white p-6 shadow-sm",
                ),
                class_name="rounded-3xl bg-white p-8 shadow-lg",
            ),
            rx.box(
                rx.heading("Details", class_name="text-2xl font-bold mb-4"),
                rx.text(
                    "This page highlights the product's season, carbon impact and nutrient profile in a broader layout.",
                    class_name="text-slate-600 leading-relaxed mb-6",
                ),
                rx.box(
                    rx.heading("Nutrients", class_name="text-xl font-semibold mb-4"),
                    rx.flex(
                        rx.foreach(
                            product["nutrients"],
                            lambda nutrient: rx.box(
                                nutrient,
                                class_name="rounded-2xl bg-emerald-50 px-4 py-2 text-emerald-900 font-medium",
                            ),
                        ),
                        class_name="flex flex-wrap gap-3",
                    ),
                    class_name="rounded-3xl bg-white p-6 shadow-sm mb-6",
                ),
                rx.box(
                    rx.heading("How to use it", class_name="text-xl font-semibold mb-4"),
                    rx.text(
                        "Perfect for salads, smoothies, and seasonal meals when it is freshest.",
                        class_name="text-slate-600 leading-relaxed",
                    ),
                    class_name="rounded-3xl bg-white p-6 shadow-sm",
                ),
                class_name="rounded-3xl bg-white p-8 shadow-lg",
            ),
            class_name="grid-cols-1 gap-8 lg:grid-cols-[0.9fr_1.1fr] max-w-6xl mx-auto px-4 pb-12",
        ),
            class_name="min-h-[calc(100vh-72px)] bg-[#eef6e8] pb-12 pt-6",
        ),
    )
