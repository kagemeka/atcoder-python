from __future__ import annotations

# rtd theme configuration
# # https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
html_theme_options: dict[str, str | bool | int] = {
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}
