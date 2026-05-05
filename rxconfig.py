import reflex as rx
from reflex_base import constants
from reflex.utils import js_runtimes

# The Codex Windows environment can put an inaccessible WindowsApps node.exe on
# PATH. Run React Router through Bun and skip Reflex's Node version probe.
constants.PackageJson.Commands.DEV = "bun --bun ./node_modules/@react-router/dev/bin.js dev --host"
constants.PackageJson.Commands.EXPORT = "bun --bun ./node_modules/@react-router/dev/bin.js build"
js_runtimes.get_node_version = lambda: None
js_runtimes.is_outdated_nodejs_installed = lambda: False

config = rx.Config(
    app_name="in_season_greens",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
