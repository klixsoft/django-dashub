import copy
import logging
from typing import Any, Dict

from django.conf import settings

from .utils import hex_to_rgb

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS: Dict[str, Any] = {
    # title of the window (Will default to current_admin_site.site_title)
    "site_title": "Admin Dashboard",
    # Title on the login screen (19 chars max) (will default to current_admin_site.site_header)
    "site_header": None,
    # Title on the brand (19 chars max) (will default to current_admin_site.site_header)
    "site_brand": None,
    # URL of the logo for your site, used for brand on top left
    "site_logo": "https://cdn.practet.com/static/logo-new.webp",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    ############
    # Top Menu #
    ############
    # Links to put along the nav bar
    "topmenu_links": [],
    #############
    # User Menu #
    #############
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps to base side menu ordering off of
    "order_menus": [],
    # Custom links to append to side menu app groups, keyed on lower case app label
    # or makes a new group if the given app label doesnt exist in installed apps
    "custom_links": {},
    # Custom icons for side menu apps/models See the link below
    "icons": {"auth": "fas fa-users-cog", "auth.user": "fas fa-user", "auth.Group": "fas fa-users"},
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": [],
    "custom_js": [],
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {},
    # Add a language dropdown into the admin
    "language_chooser": False,
    "model_submenus": {},
    "related_modal_active": True,
    "use_compressed_assets": False,

    # Styles
    "theme_color": "#e31837",
    "border_radius": "4px"
}

CHANGEFORM_TEMPLATES = {
    "single": "dashub/includes/single.html",
    "horizontal_tabs": "dashub/includes/horizontal_tabs.html",
    "vertical_tabs": "dashub/includes/vertical_tabs.html",
}


def get_settings() -> Dict:
    dashub_settings = copy.deepcopy(DEFAULT_SETTINGS)
    user_settings = {x: y for x, y in getattr(settings, "DASHUB_SETTINGS", {}).items() if y is not None}
    dashub_settings.update(user_settings)

    # Deal with single strings in hide_apps/hide_models and make sure we lower case 'em
    if isinstance(dashub_settings["hide_apps"], str):
        dashub_settings["hide_apps"] = [dashub_settings["hide_apps"]]
    dashub_settings["hide_apps"] = [x.lower() for x in dashub_settings["hide_apps"]]

    if isinstance(dashub_settings["hide_models"], str):
        dashub_settings["hide_models"] = [dashub_settings["hide_models"]]
    dashub_settings["hide_models"] = [x.lower() for x in dashub_settings["hide_models"]]

    # Ensure icon model names and classes are lower case
    dashub_settings["icons"] = {x.lower(): y.lower() for x, y in dashub_settings.get("icons", {}).items()}

    # Default the site icon using the site logo
    dashub_settings["site_icon"] = dashub_settings["site_icon"] or dashub_settings["site_logo"]

    # ensure all model names are lower cased
    dashub_settings["changeform_format_overrides"] = {
        x.lower(): y.lower() for x, y in dashub_settings.get("changeform_format_overrides", {}).items()
    }

    dashub_settings["theme_color_rgb"] = hex_to_rgb(dashub_settings.get("theme_color", "#30AA99"))
    return dashub_settings
