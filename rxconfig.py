import reflex as rx

config = rx.Config(
    app_name="in_season_greens",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
