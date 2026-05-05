import reflex as rx


class app:
    page = "min-h-screen bg-[#f2f4ef] [font-family:Nunito,sans-serif] text-[#151915]"


class catalog:
    shell = "mx-auto w-full max-w-[1240px] bg-[#f7f7f5] px-3 py-3.5 pb-14 md:bg-transparent md:px-7 md:py-6"
    header = "mb-4 items-center justify-between gap-4"
    count = "text-[11px] font-black tracking-wider text-[#839084] md:text-[13px]"
    title = "mt-1 hidden text-[28px] font-black leading-tight text-[#151915] md:block"
    grid = "grid grid-cols-2 gap-3 md:grid-cols-[repeat(auto-fill,minmax(230px,1fr))] md:gap-[18px]"


class ui:
    hamburger_line = "h-0.5 w-[18px] rounded bg-[#273027]"
    hamburger_button = (
        "flex size-[42px] shrink-0 flex-col items-center justify-center gap-1.5 "
        "rounded-lg border border-[#d9e1d6] bg-[#f7f9f5] p-0 hover:bg-white"
    )
    filter_active = (
        "shrink-0 rounded-lg border border-[#2db34a] bg-[#2db34a] px-3 py-2 "
        "text-xs font-black text-white md:px-3.5 md:text-[13px]"
    )
    filter_inactive = (
        "shrink-0 rounded-lg border border-[#dce3d9] bg-white px-3 py-2 "
        "text-xs font-black text-[#4f5b50] hover:bg-[#f7f9f5] md:px-3.5 md:text-[13px]"
    )
    search_icon = "absolute left-3 top-1/2 size-4 -translate-y-1/2 text-[#8a948a]"
    search_input = (
        "h-10 w-full rounded-lg border border-[#d9e1d6] bg-[#f7f9f5] "
        "pl-10 pr-3 font-bold text-[#1b211b] outline-none "
        "placeholder:text-[#8a948a] md:h-[46px] md:text-[15px]"
    )
    search_shell = "relative min-w-0 flex-1"


class navigation:
    desktop_header = (
        "sticky top-0 z-20 hidden border-b border-[#e0e5dc] bg-white/95 "
        "shadow-[0_8px_28px_rgba(28,45,30,.08)] backdrop-blur md:block"
    )
    desktop_inner = (
        "grid w-full grid-cols-[max-content_minmax(0,1fr)_max-content] items-center gap-3 "
        "px-4 py-2.5 lg:grid-cols-[max-content_minmax(0,1fr)_max-content_max-content]"
    )
    desktop_logo = "whitespace-nowrap text-[23px] font-black leading-none text-[#123d1d]"
    desktop_filters = "hidden gap-2 overflow-x-auto lg:flex"
    mobile_header = "sticky top-0 z-20 md:hidden"
    mobile_inner = "h-12 items-center justify-between border-b border-[#e8e8e8] bg-white px-3.5"
    mobile_logo_row = "items-center gap-1.5"
    mobile_logo_icon = "size-[17px] text-[#1a7a30]"
    mobile_logo = "text-[15px] font-black text-[#123d1d]"
    mobile_filters = "sticky top-12 z-10 border-b border-[#e8e8e8] bg-white px-3 py-2 shadow-[0_2px_12px_rgba(0,0,0,.07)] md:hidden"
    mobile_filter_row = "mt-2 gap-1.5 overflow-x-auto"
    drawer_overlay = "fixed inset-0 z-30 bg-black/35"
    drawer_open = (
        "fixed inset-y-0 right-0 z-40 flex w-full translate-x-0 flex-col bg-white "
        "shadow-[-4px_0_24px_rgba(0,0,0,.15)] transition-transform duration-300 md:w-[360px]"
    )
    drawer_closed = (
        "fixed inset-y-0 right-0 z-40 flex w-full translate-x-full flex-col bg-white "
        "shadow-[-4px_0_24px_rgba(0,0,0,.15)] transition-transform duration-300 md:w-[360px]"
    )
    drawer_header = "bg-[#164f26] p-5 pt-7"
    drawer_brand_row = "items-center gap-1.5"
    drawer_brand_icon = "size-[18px] text-white"
    drawer_brand = "text-xl font-black text-white"
    drawer_location_row = "mt-1 gap-1"
    drawer_location_icon = "size-3 text-white/70"
    drawer_location = "text-xs text-white/70"
    drawer_list = "flex-1 gap-0 overflow-y-auto"
    drawer_item = "w-full cursor-pointer items-center gap-3.5 border-b border-[#f0f0f0] px-5 py-3.5 hover:bg-[#f7f9f5]"
    drawer_item_icon = "size-5 text-[#333]"
    drawer_item_label = "text-[15px] font-bold text-[#222]"
    drawer_item_subtitle = "text-[11px] text-[#999]"
    drawer_footer = "border-t border-[#f0f0f0] px-5 py-3.5 text-center text-[11px] text-[#bbb]"


class overview:
    section = "bg-[#164f26] md:block"
    shell = "w-full"
    header = "items-start justify-between gap-6 px-[18px] py-5 md:py-6"
    title_row = "items-center gap-2.5"
    title_icon = "size-5 text-white md:size-[30px]"
    title = "text-[22px] font-black leading-tight text-white md:text-4xl"
    location_box = "text-right"
    location_row = "justify-end gap-1"
    location_icon = "size-3 text-white/85 md:size-3.5"
    location_text = "text-[11px] font-extrabold text-white/85 md:text-[13px]"
    month = "text-right text-xs font-black text-[#a8e6ba] md:text-[15px]"
    content_grid = "grid-cols-1 border-white/20 md:grid-cols-2 md:border-t"
    signals_panel = (
        "mx-4 mb-5 rounded-2xl border border-white/20 bg-white/10 p-3.5 "
        "md:m-0 md:rounded-none md:border-0 md:border-r md:border-white/20 md:p-[18px]"
    )
    section_label_green = "mb-3 text-[11px] font-black tracking-wider text-[#a8e6ba] md:text-xs"
    section_label_light = "mb-3 text-[11px] font-black tracking-wider text-white/65 md:text-xs"
    signals_grid = "grid-cols-2 gap-2 md:gap-3.5"
    signal_row = "min-w-0 items-center gap-2.5"
    signal_icon = "size-[18px] text-white/90 md:size-[22px]"
    signal_copy = "min-w-0"
    signal_value = "text-[11px] font-black leading-tight text-white md:text-[17px]"
    signal_label = "text-[9px] font-extrabold leading-tight text-white/65 md:text-[11px]"
    outlook_panel = "px-4 pb-5 md:p-[18px]"
    outlook_grid = "grid-cols-1 gap-3 md:grid-cols-2"
    outlook_row = "items-start gap-2.5"
    outlook_icon = "mt-0.5 size-4 text-white/85"
    outlook_text = "text-[13px] font-bold leading-snug text-white/90"


class product_card:
    card = (
        "flex flex-col overflow-hidden rounded-lg border border-[#e1e1dc] bg-white "
        "shadow-[0_8px_22px_rgba(35,45,35,.16)]"
    )
    image_asset = "h-full w-full object-cover"
    body = "border-t border-[#eeeeea] px-2.5 pb-2.5 pt-2"
    title = "mb-1 text-[17px] font-black leading-tight text-[#141414]"
    months = "mb-1.5 flex-wrap gap-1"
    month_current = "bg-[#2db34a] text-white"
    month_default = "bg-[#e0e0e0] text-[#666]"
    month_missing = "mb-1.5 text-[10px] font-bold italic text-[#999]"
    origin_icon_local = "shrink-0 size-3.5 text-[#1a7a30]"
    origin_icon_far = "shrink-0 size-3.5 text-[#e03535]"
    origin_box_local = "mb-1.5 items-center gap-1 rounded-lg bg-[#e6f7ea] px-1.5 py-1.5"
    origin_box_far = "mb-1.5 items-center gap-1 rounded-lg bg-[#fdecea] px-1.5 py-1.5"
    origin_copy = "min-w-0 flex-1"
    origin_title = "break-words text-[8.5px] font-black leading-tight text-[#111]"
    carbon_label = "text-[7.5px] leading-tight text-[#777]"
    carbon_value = "shrink-0 text-right text-[7.5px] font-black leading-tight text-[#111]"
    nutrients = "mb-2 flex-wrap gap-1"
    nutrient = "rounded-full bg-[#2db34a] px-2 py-0.5 text-[9px] font-black text-white"
    actions = "gap-1.5"
    save_button = (
        "flex flex-1 items-center justify-center gap-1 rounded-lg border-2 border-[#ccc] "
        "bg-white py-1.5 text-[11px] font-black text-[#222] hover:bg-[#f7f9f5]"
    )
    info_button = "flex-[1.4] rounded-lg bg-[#2db34a] py-1.5 text-[11px] font-black text-white hover:bg-[#1a7a30]"

    @staticmethod
    def image(status) -> rx.Component:
        return rx.match(
            status,
            ("peak", "relative m-2 flex h-[120px] items-center justify-center overflow-hidden rounded-lg bg-[#3dcc56]"),
            ("season", "relative m-2 flex h-[120px] items-center justify-center overflow-hidden rounded-lg bg-[#7dd89a]"),
            ("soon", "relative m-2 flex h-[120px] items-center justify-center overflow-hidden rounded-lg bg-[#f0bc50]"),
            ("relative m-2 flex h-[120px] items-center justify-center overflow-hidden rounded-lg bg-[#d0cdc8]"),
        )

    @staticmethod
    def badge(status) -> rx.Component:
        return rx.match(
            status,
            ("peak", "absolute left-2 top-2 rounded-lg bg-[#2db34a] px-2 py-1 text-[9px] font-black tracking-wide text-white"),
            ("season", "absolute left-2 top-2 rounded-lg bg-[#5bc27a] px-2 py-1 text-[9px] font-black tracking-wide text-white"),
            ("soon", "absolute left-2 top-2 rounded-lg bg-[#e8a020] px-2 py-1 text-[9px] font-black tracking-wide text-white"),
            ("absolute left-2 top-2 rounded-lg bg-[#e03535] px-2 py-1 text-[9px] font-black tracking-wide text-white"),
        )
