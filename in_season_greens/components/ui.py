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
    return rx.el.button(
        rx.hstack(
            app_icon("search", styles.ui.search_suggestion_icon, 2),
            rx.box(
                rx.text(suggestion["name_en"], class_name=styles.ui.search_suggestion_name),
                rx.text(suggestion["category"], class_name=styles.ui.search_suggestion_category),
                class_name=styles.ui.search_suggestion_copy,
            ),
            class_name=styles.ui.search_suggestion_inner,
        ),
        type="button",
        on_mouse_down=state.apply_search_suggestion(suggestion["name_en"]),
        class_name=styles.ui.search_suggestion,
    )


def search_input(state) -> rx.Component:
    return rx.box(
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
        rx.button(
            app_icon("search", styles.ui.search_submit_icon, 2),
            on_mouse_down=state.submit_search,
            aria_label="Search",
            class_name=styles.ui.search_submit_button,
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


def get_category_emoji(category: str) -> str:
    """Return an emoji based on product category"""
    emoji_map = {
        "fruit": "🍎",
        "vegetable": "🥬",
        "leafy": "🥬",
        "root": "🥕",
        "berry": "🫐",
        "citrus": "🍊",
        "tropical": "🥑",
    }
    return emoji_map.get(category.lower(), "🌱")


def product_modal(state) -> rx.Component:
    """Product detail modal that appears when 'Show info' is clicked"""
    from .product_card import carbon_label, month_name, status_label
    from ..data import CURRENT_MONTH
    
    product = state.modal_product
    
    # Determine if product is in season
    is_in = rx.cond(
        product != None,
        (product["status"] == "peak") | (product["status"] == "season"),
        False
    )
    
    # Determine origin box styling
    origin_box_class = rx.cond(
        is_in,
        "mb-1.5 items-center gap-1 rounded-lg bg-[#e6f7ea] px-3 py-2",
        "mb-1.5 items-center gap-1 rounded-lg bg-[#fdecea] px-3 py-2",
    )
    
    origin_icon_class = rx.cond(
        is_in,
        "shrink-0 size-4 text-[#1a7a30]",
        "shrink-0 size-4 text-[#e03535]",
    )
    
    has_local_status = rx.cond(
        product != None,
        product["local"] != None,
        False
    )
    
    return rx.cond(
        state.modal_open & (product != None),
        # Overlay that closes modal on click
        rx.box(
            # Modal backdrop - clickable to close
            rx.box(
                on_click=state.close_modal,
                class_name="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm",
            ),
            # Modal content
            rx.box(
                rx.box(
                    # Header with close button
                    rx.hstack(
                        rx.heading(
                            product["name"],
                            class_name="text-3xl font-black text-[#151915]",
                        ),
                        rx.spacer(),
                        rx.button(
                            app_icon("x", "size-6 text-[#555]", 2),
                            on_click=state.close_modal,
                            class_name="rounded-lg hover:bg-[#f0f0f0] p-2",
                            aria_label="Close modal",
                        ),
                        class_name="w-full items-center gap-4 mb-6",
                    ),
                    # Product category icon and status
                    rx.hstack(
                        rx.text(
                            get_category_emoji(product["category"]),
                            class_name="text-6xl leading-none",
                        ),
                        rx.vstack(
                            rx.box(
                                status_label(product["status"]),
                                class_name=rx.cond(
                                    product["status"] == "peak",
                                    "rounded-lg bg-[#2db34a] px-3 py-1 text-xs font-black tracking-wide text-white inline-block",
                                    rx.cond(
                                        product["status"] == "season",
                                        "rounded-lg bg-[#5bc27a] px-3 py-1 text-xs font-black tracking-wide text-white inline-block",
                                        rx.cond(
                                            product["status"] == "soon",
                                            "rounded-lg bg-[#e8a020] px-3 py-1 text-xs font-black tracking-wide text-white inline-block",
                                            "rounded-lg bg-[#e03535] px-3 py-1 text-xs font-black tracking-wide text-white inline-block",
                                        ),
                                    ),
                                ),
                            ),
                            rx.text(
                                carbon_label(product["co2"]),
                                class_name="text-sm font-semibold text-slate-700 mt-2",
                            ),
                            rx.text(
                                rx.cond(product["co2"] == None, "???", product["co2"]),
                                " kg CO2e / kg",
                                class_name="text-xs text-slate-500",
                            ),
                            class_name="gap-1",
                        ),
                        class_name="gap-6 mb-8 items-start",
                    ),
                    # Origin and availability
                    rx.box(
                        rx.heading("Origin & Availability", class_name="text-xl font-bold mb-4 text-[#151915]"),
                        rx.hstack(
                            app_icon(
                                "map_pin",
                                rx.cond(is_in, "size-5 text-[#1a7a30]", "size-5 text-[#e03535]"),
                                3,
                            ),
                            rx.text(
                                rx.cond(
                                    has_local_status,
                                    rx.cond(product["local"], "Grown Locally", rx.fragment("Grown in ", product["origin"])),
                                    "Origin unknown",
                                ),
                                class_name="font-bold text-slate-700",
                            ),
                            class_name=origin_box_class,
                        ),
                        rx.box(
                            rx.heading("Available Months", class_name="text-sm font-bold mb-3 text-slate-600 mt-4"),
                            rx.flex(
                                rx.foreach(
                                    product["months"],
                                    lambda month: rx.box(
                                        month_name(month),
                                        class_name=rx.cond(
                                            month == CURRENT_MONTH,
                                            "rounded-full px-3 py-1 bg-[#2db34a] text-white font-bold text-sm",
                                            "rounded-full px-3 py-1 bg-[#e0e0e0] text-slate-700 font-bold text-sm",
                                        ),
                                    ),
                                ),
                                class_name="flex-wrap gap-2",
                            ),
                            class_name="rounded-2xl bg-white/50 p-4",
                        ),
                        class_name="rounded-2xl bg-white p-6 mb-6",
                    ),
                    # Nutrients
                    rx.box(
                        rx.heading("Nutrients", class_name="text-xl font-bold mb-4 text-[#151915]"),
                        rx.flex(
                            rx.foreach(
                                product["nutrients"],
                                lambda nutrient: rx.box(
                                    nutrient,
                                    class_name="rounded-full bg-[#2db34a] px-4 py-2 text-sm font-bold text-white",
                                ),
                            ),
                            class_name="flex-wrap gap-3",
                        ),
                        class_name="rounded-2xl bg-white p-6 mb-6",
                    ),
                    # Additional info
                    rx.box(
                        rx.heading("Details", class_name="text-xl font-bold mb-4 text-[#151915]"),
                        rx.vstack(
                            rx.box(
                                rx.heading("Local", class_name="text-sm font-bold text-slate-600 mb-1"),
                                rx.text(
                                    rx.cond(
                                        product["local"] == True,
                                        "Yes, grown locally",
                                        rx.cond(
                                            product["local"] == False,
                                            "No, imported",
                                            "Unknown"
                                        )
                                    ),
                                    class_name="text-slate-700",
                                ),
                            ),
                            rx.box(
                                rx.heading("Origin", class_name="text-sm font-bold text-slate-600 mb-1"),
                                rx.text(
                                    rx.cond(product["origin"] != None, product["origin"], "Unknown"),
                                    class_name="text-slate-700",
                                ),
                            ),
                            rx.box(
                                rx.heading("Carbon Footprint", class_name="text-sm font-bold text-slate-600 mb-1"),
                                rx.text(
                                    rx.cond(
                                        product["co2"] == None,
                                        "Not available",
                                        rx.fragment(product["co2"], " kg CO2e / kg")
                                    ),
                                    class_name="text-slate-700",
                                ),
                            ),
                            class_name="gap-4",
                        ),
                        class_name="rounded-2xl bg-white p-6",
                    ),
                    class_name="w-full max-h-[90vh] overflow-y-auto",
                ),
                class_name="fixed left-1/2 top-1/2 z-50 w-11/12 max-w-2xl -translate-x-1/2 -translate-y-1/2 rounded-3xl bg-[#f2f4ef] p-8 shadow-2xl",
            ),
            class_name="fixed inset-0 z-40",
        ),
        rx.fragment(),
    )
