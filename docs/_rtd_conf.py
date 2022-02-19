import typing

# rtd theme configuration
# # https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
html_theme_options: typing.Dict[str, typing.Union[str, bool, int]] = {
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}
