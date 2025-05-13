import copy
import itertools
import json
import logging
import urllib.parse
from typing import Any, Callable, Dict, List, Optional, Union

from django.apps import apps
from django.conf import settings
from django.contrib.admin import ListFilter
from django.contrib.admin.helpers import AdminForm, Fieldset, InlineAdminFormSet
from django.contrib.admin.models import LogEntry
from django.contrib.admin.sites import all_sites
from django.contrib.admin.views.main import PAGE_VAR, ChangeList, ALL_VAR
from django.contrib.auth import get_user_model
from django.contrib.auth.context_processors import PermWrapper
from django.contrib.auth.models import AbstractUser
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import ModelBase
from django.http import HttpRequest
from django.template import Context, Library
from django.template.defaultfilters import capfirst
from django.template.loader import get_template
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import escape, format_html
from django.utils.safestring import SafeText, mark_safe
from django.utils.text import get_text_list, slugify
from django.utils.translation import gettext
from django.forms import widgets, JSONField

from .. import version
from ..settings import CHANGEFORM_TEMPLATES, get_settings
from ..utils import (
    get_admin_url,
    get_filter_id,
    get_installed_apps,
    has_fieldsets_check,
    make_menu,
    order_with_respect_to,
)

User = get_user_model()
register = Library()
logger = logging.getLogger(__name__)


def get_model_info(model_path: str):
    """
    Fetch model verbose name and admin list URL dynamically.

    :param model_path: Model path in "app_label.ModelName" format.
    :return: Dictionary with 'name' and 'url'.
    """
    try:
        app_label, model_name = model_path.split(".")
        model = apps.get_model(app_label, model_name)

        verbose_name = model._meta.verbose_name_plural or model._meta.verbose_name
        model_admin_url = reverse(f"admin:{app_label}_{model_name.lower()}_changelist")
        return {"name": str(verbose_name), "url": model_admin_url}
    except Exception as e:
        return {"name": model_path, "url": "#"}


@register.simple_tag(takes_context=True)
def get_side_menu(context: Context, using: str = "available_apps") -> List[Dict[str, Any]]:
    """
    Generate the side menu with sorting, custom submenus, and additional custom links.
    """
    user = context.get("user")
    if not user:
        return []

    options = get_settings()
    default_orders = options.get("default_orders", {})
    installed_apps = get_installed_apps()
    available_apps = copy.deepcopy(context.get(using, []))
    request = context.get("request")

    if not available_apps:
        from django.contrib import admin
        available_apps = admin.site.get_app_list(request)

    # Add custom apps if not already available
    for app_label, links in options.get("custom_links", {}).items():
        if app_label.lower() not in installed_apps:
            available_apps.append({
                "name": app_label,
                "app_label": app_label,
                "app_url": "#",
                "has_module_perms": True,
                "models": [],
                "order": links["order"] if "order" in links else default_orders.get(app_label, 0),
            })

    custom_links = {
        app_name: make_menu(user, links, options, app_name, allow_appmenus=False)
        for app_name, links in options.get("custom_links", {}).items()
    }

    submenus_models = set(options.get("submenus_models", []))
    hidden_apps = set(options.get("hide_apps", []))
    hidden_models = set(options.get("hide_models", []))
    order_menus = options.get("order_menus", [])

    menu = []

    for app in available_apps:
        app_label = app["app_label"]
        if app_label in hidden_apps:
            continue

        app["icon"] = options["icons"].get(app_label, options["default_icon_parents"])
        app["order"] = order_menus[app_label] if app_label in order_menus else default_orders.get(app_label, 0)

        menu_items = []

        app_custom_links = custom_links.get(app_label, [])
        for model in app.get("models", []):
            model_object_name = str(model['object_name']).lower()
            model_str = f"{app_label}.{model_object_name}".lower()
            if model_str in hidden_models:
                continue

            model["url"] = model["admin_url"]
            model["count"] = model.get("model", {}).objects.count() if model.get("model") else 0
            model["model_str"] = model_str
            model["icon"] = options["icons"].get(model_str, options["default_icon_children"])
            model["order"] = model.get("order", default_orders.get(model_str, 0))

            finded_menus = {}
            if app_custom_links:
                finded_menus = next((item for item in app_custom_links if item['object_name'] == model_str), None)

            if model_str in submenus_models:
                submenu = [{"name": "Add New", "url": model["add_url"], "order": 0},
                           {"name": model["name"], "url": model["url"], "order": 0}]
            else:
                submenu = []
            if finded_menus:
                custom_links_submenus = finded_menus.get("submenu", [])
                submenu.extend(custom_links_submenus)
                app_custom_links = [link for link in app_custom_links if link['name'] != model_object_name]
            model["submenu"] = sorted(submenu, key=lambda x: x.get("order", 0), reverse=True)
            menu_items.append(model)
        if app_custom_links:
            for new_link in app_custom_links:
                if not any(
                        (existing_link.get('url') == new_link.get('url')) or
                        (existing_link.get('model_str') == new_link.get('object_name'))
                        for existing_link in menu_items
                ):
                    menu_items.append(new_link)

        if menu_items:
            app["models"] = sorted(menu_items, key=lambda x: x.get("order", 0))
            menu.append(app)

    return order_menus_with_order(menu, order_menus)


def order_menus_with_order(menu: List[Dict[str, Any]], order_menus: List[str]) -> List[Dict[str, Any]]:
    """
    Sorts menu items based on `order_menus` list. Items not in the list will retain their original order.
    This function ensures sorting in the following hierarchy: submenus → models → apps.
    """
    order_map = {label.lower(): index for index, label in enumerate(order_menus)}

    def get_order_index(item: Dict[str, Any]) -> int:
        """Returns the order index of an app."""
        return order_map.get(item["app_label"].lower(), item.get("order", 0))

    def sort_models(models: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort models inside apps based on 'order' key."""
        for model in models:
            if "submenu" in model:
                model["submenu"].sort(key=lambda x: x.get("order", 0), reverse=True)
        return sorted(models, key=lambda x: x.get("order", 0), reverse=True)

    for app in menu:
        if "models" in app:
            app["models"] = sort_models(app["models"])

    return sorted(menu, key=get_order_index, reverse=True)


@register.simple_tag
def get_top_menu(user: AbstractUser, admin_site: str = "admin") -> List[Dict]:
    """
    Produce the menu for the top nav bar
    """
    options = get_settings()
    return make_menu(user, options.get("topmenu_links", []), options, None, allow_appmenus=True, admin_site=admin_site)


@register.simple_tag
def get_user_menu(user: AbstractUser, admin_site: str = "admin") -> List[Dict]:
    """
    Produce the menu for the user dropdown
    """
    options = get_settings()
    return make_menu(
        user,
        options.get("usermenu_links", []),
        options,
        None,
        allow_appmenus=False,
        admin_site=admin_site,
    )


@register.simple_tag
def get_dashub_settings(request: WSGIRequest) -> Dict:
    """
    Get Practet Dashboard settings, update any defaults from the request, and return
    """
    settings = get_settings()

    admin_site = {x.name: x for x in all_sites}.get("admin", {})
    if not settings["site_title"]:
        settings["site_title"] = getattr(admin_site, "site_title", None)

    if not settings["site_header"]:
        settings["site_header"] = getattr(admin_site, "site_header", None)

    if not settings["site_brand"]:
        settings["site_brand"] = getattr(admin_site, "site_header", None)

    return settings


@register.simple_tag
def get_dashub_version() -> str:
    """
    Get the version for this package
    """
    return version


@register.simple_tag
def get_user_avatar(user: AbstractUser) -> str:
    """
    For the given user, try to get the avatar image, which can be one of:

        - ImageField on the user model
        - URLField/Charfield on the model
        - A callable that receives the user instance e.g lambda u: u.profile.image.url
    """
    no_avatar = static("assets/img/user.svg")
    options = get_settings()
    avatar_field_name: Optional[Union[str, Callable]] = options.get("user_avatar")

    if not avatar_field_name:
        return no_avatar

    if callable(avatar_field_name):
        return avatar_field_name(user)

    # If we find the property directly on the user model (imagefield or URLfield)
    avatar_field = getattr(user, avatar_field_name, None)
    if avatar_field is not None:
        if not avatar_field:
            return no_avatar
        if isinstance(avatar_field, str):
            return avatar_field
        elif hasattr(avatar_field, "url"):
            return avatar_field.url
        elif callable(avatar_field):
            return avatar_field()

    logger.warning("Avatar field must be an ImageField/URLField on the user model, or a callable")

    return no_avatar


@register.simple_tag
def dashub_paginator_number(change_list: ChangeList, i: int) -> SafeText:
    """
    Generate an individual page index link in a paginated list.
    """
    html_str = ""
    start = i == 1
    end = i == change_list.paginator.num_pages
    spacer = i in (".", "…")
    current_page = i == change_list.page_num

    if start:
        link = change_list.get_query_string({PAGE_VAR: change_list.page_num - 1}) if change_list.page_num > 1 else "#"
        html_str += """
        <li class="page-item previous {disabled}">
            <a class="page-link" href="{link}" data-dt-idx="0" tabindex="0">Previous</a>
        </li>
        """.format(link=link, disabled="disabled" if link == "#" else "")

    if current_page:
        html_str += """
        <li class="page-item active">
            <a class="page-link" href="javascript:void(0);" data-dt-idx="3" tabindex="0">{num}</a>
        </li>
        """.format(num=i)
    elif spacer:
        html_str += """
        <li class="page-item">
            <a class="page-link" href="javascript:void(0);" data-dt-idx="3" tabindex="0">… </a>
        </li>
        """
    else:
        query_string = change_list.get_query_string({PAGE_VAR: i})
        end = "end" if end else ""
        html_str += """
            <li class="page-item">
            <a href="{query_string}" class="page-link {end}" data-dt-idx="3" tabindex="0">{num}</a>
            </li>
        """.format(num=i, query_string=query_string, end=end)

    if end:
        link = change_list.get_query_string({PAGE_VAR: change_list.page_num + 1}) if change_list.page_num < i else "#"
        html_str += """
        <li class="page-item next {disabled}">
            <a class="page-link" href="{link}" data-dt-idx="7" tabindex="0">Next</a>
        </li>
        """.format(link=link, disabled="disabled" if link == "#" else "")

    return format_html(html_str)


@register.simple_tag
def admin_extra_filters(cl: ChangeList) -> Dict:
    """
    Return the dict of used filters which is not included in list_filters form
    """
    used_parameters = list(itertools.chain(*(s.used_parameters.keys() for s in cl.filter_specs)))
    return {k: v for k, v in cl.params.items() if k not in used_parameters}


@register.simple_tag
def dashub_list_filter(cl: ChangeList, spec: ListFilter):
    """
    Render out our list filter in a dropdown friendly format, for use by filter.html, see original implementation here

    django.contrib.admin.templatetags.admin_list.admin_list_filter

    """
    tpl = get_template(spec.template)
    choices = list(spec.choices(cl))
    field_key = get_filter_id(spec)
    field_name = ""

    for choice in choices:
        qs = choice.get("query_string")
        if not qs:
            continue

        matches = {}
        query_parts = urllib.parse.parse_qs(qs[1:])
        if f"{field_key}__exact" in query_parts:
            matches[f"{field_key}__exact"] = query_parts[f"{field_key}__exact"][0]
        elif field_key in query_parts:
            matches[field_key] = query_parts[field_key][0]
        else:
            for key in query_parts:
                if key.startswith(field_key + "__") or f"__{field_key}__" in key:
                    matches[key] = query_parts[key][0]

        # Iterate matches, use original as actual values, additional for hidden
        for i, (key, value) in enumerate(matches.items()):
            if i == 0:
                choice["name"] = key
                choice["value"] = value
                field_name = key

    return tpl.render({
        "field_name": field_name,
        "title": spec.title,
        "choices": choices,
        "spec": spec
    })


@register.simple_tag
def jazzy_admin_url(value: Union[str, ModelBase], admin_site: str = "admin") -> str:
    """
    Get the admin url for a given object
    """
    return get_admin_url(value, admin_site=admin_site)


@register.filter
def has_dashub_setting(settings: Dict[str, Any], key: str) -> bool:
    return key in settings and settings[key] is not None


@register.filter
def has_fieldsets(adminform: AdminForm) -> bool:
    """
    Do we have fieldsets
    """
    return has_fieldsets_check(adminform)


@register.simple_tag
def get_sections(
        admin_form: AdminForm, inline_admin_formsets: List[InlineAdminFormSet]
) -> List[Union[Fieldset, InlineAdminFormSet]]:
    """
    Get and sort all of the sections that need rendering out in a change form
    """
    fieldsets = list(admin_form)

    # Make inlines behave like formsets
    for fieldset in inline_admin_formsets:
        fieldset.name = capfirst(fieldset.opts.verbose_name_plural)
        fieldset.is_inline = True
        fieldsets.append(fieldset)

    if hasattr(admin_form.model_admin, "dashub_section_order"):
        fieldsets = order_with_respect_to(
            fieldsets, admin_form.model_admin.dashub_section_order, getter=lambda x: x.name
        )

    return fieldsets


@register.filter
def debug(value: Any) -> Any:
    """
    Add in a breakpoint() here and use filter in templates for debugging ;)
    """
    return type(value)


@register.filter
def as_json(value: Union[List, Dict]) -> str:
    """
    Take the given item and dump it out as JSON
    """
    return json.dumps(value)


@register.simple_tag
def get_changeform_template(adminform: AdminForm) -> str:
    """
    Go get the correct change form template based on the modeladmin being used,
    the default template, or the overridden one for this modeladmin
    """
    options = get_settings()
    has_fieldsets = has_fieldsets_check(adminform)
    inlines = adminform.model_admin.inlines
    has_inlines = inlines and len(inlines) > 0
    model = adminform.model_admin.model
    model_name = "{}.{}".format(model._meta.app_label, model._meta.model_name).lower()

    changeform_format = options.get("changeform_format", "")
    if model_name in options.get("changeform_format_overrides", {}):
        changeform_format = options["changeform_format_overrides"][model_name]

    if not has_fieldsets and not has_inlines:
        return CHANGEFORM_TEMPLATES["single"]

    if not changeform_format or changeform_format not in CHANGEFORM_TEMPLATES.keys():
        return CHANGEFORM_TEMPLATES["horizontal_tabs"]

    return CHANGEFORM_TEMPLATES[changeform_format]


@register.simple_tag
def get_changeform_template_class(adminform: AdminForm) -> str:
    """
    Go get the correct change form template based on the modeladmin being used,
    the default template, or the overridden one for this modeladmin
    """
    options = get_settings()
    has_fieldsets = has_fieldsets_check(adminform)
    inlines = adminform.model_admin.inlines
    has_inlines = inlines and len(inlines) > 0
    model = adminform.model_admin.model
    model_name = "{}.{}".format(model._meta.app_label, model._meta.model_name).lower()

    changeform_format = options.get("changeform_format", "")
    if model_name in options.get("changeform_format_overrides", {}):
        changeform_format = options["changeform_format_overrides"][model_name]

    if not has_fieldsets and not has_inlines:
        return "single"

    if not changeform_format or changeform_format not in CHANGEFORM_TEMPLATES.keys():
        return "horizontal_tabs"

    return changeform_format


@register.filter
def can_view_self(perms: PermWrapper) -> bool:
    """
    Determines whether a user has sufficient permissions to view its own profile
    """
    view_perm = "view_{}".format(User._meta.model_name)
    return perms[User._meta.app_label][view_perm]


@register.simple_tag
def header_class(header: Dict, forloop: Dict) -> str:
    """
    Adds CSS classes to header HTML element depending on its attributes
    """
    classes = []
    sorted, asc, desc = (
        header.get("sorted"),
        header.get("ascending"),
        header.get("descending"),
    )

    is_checkbox_column_conditions = (
        forloop["counter0"] == 0,
        header.get("class_attrib") == ' class="action-checkbox-column"',
    )
    if all(is_checkbox_column_conditions):
        classes.append("djn-checkbox-select-all")

    if not header["sortable"]:
        return " ".join(classes)

    if sorted and asc:
        classes.append("sorting_asc")
    elif sorted and desc:
        classes.append("sorting_desc")
    else:
        classes.append("sorting")

    return " ".join(classes)


@register.filter
def app_is_installed(app: str) -> bool:
    """
    Checks if an app has been installed under INSTALLED_APPS on the project settings
    """
    return app in settings.INSTALLED_APPS


@register.simple_tag
def action_message_to_list(action: LogEntry) -> List[Dict]:  # noqa: C901
    """
    Retrieves a formatted list with all actions taken by a user given a log entry object
    """
    messages = []

    def added(x: str) -> Dict:
        return {
            "msg": x,
            "icon": "plus-circle",
            "colour": "success",
        }

    def changed(x: str) -> Dict:
        return {
            "msg": x,
            "icon": "edit",
            "colour": "blue",
        }

    def deleted(x: str) -> Dict:
        return {
            "msg": x,
            "icon": "trash",
            "colour": "danger",
        }

    if action.change_message and action.change_message[0] == "[":
        try:
            change_message = json.loads(action.change_message)
        except json.JSONDecodeError:
            return [action.change_message]

        for sub_message in change_message:
            if "added" in sub_message:
                if sub_message["added"]:
                    sub_message["added"]["name"] = gettext(sub_message["added"]["name"])
                    messages.append(added(gettext("Added {name} “{object}”.").format(**sub_message["added"])))
                else:
                    messages.append(added(gettext("Added.")))

            elif "changed" in sub_message:
                sub_message["changed"]["fields"] = get_text_list(
                    [gettext(field_name) for field_name in sub_message["changed"]["fields"]],
                    gettext("and"),
                )
                if "name" in sub_message["changed"]:
                    sub_message["changed"]["name"] = gettext(sub_message["changed"]["name"])
                    messages.append(changed(gettext("Changed {fields}.").format(**sub_message["changed"])))
                else:
                    messages.append(changed(gettext("Changed {fields}.").format(**sub_message["changed"])))

            elif "deleted" in sub_message:
                sub_message["deleted"]["name"] = gettext(sub_message["deleted"]["name"])
                messages.append(deleted(gettext("Deleted “{object}”.").format(**sub_message["deleted"])))

    return messages if len(messages) else [changed(gettext(action.change_message))]


@register.filter
def style_bold_first_word(message: str) -> str | Any:
    """
    Wraps first word in a message with <strong> HTML element
    """
    message_words = escape(message).split()

    if not len(message_words):
        return ""

    message_words[0] = "<strong>{}</strong>".format(message_words[0])

    message = " ".join(list(message_words))

    return mark_safe(message)


@register.filter
def unicode_slugify(message: str) -> str:
    return slugify(message, allow_unicode=True)


@register.filter
def render_form_field_class(field, css_class=None):
    widget = field.field.widget
    existing_classes = widget.attrs.get("class", "")
    class_list = existing_classes.split()

    if isinstance(field.field, JSONField):
        default_class = "form-control jsoneditor"
    elif isinstance(widget, (
            widgets.Select,
            widgets.SelectMultiple
    )):
        default_class = "form-select"
    elif isinstance(widget, (
            widgets.CheckboxInput,
            widgets.CheckboxSelectMultiple,
            widgets.RadioSelect
    )):
        default_class = None
    else:
        default_class = "form-control"

    if css_class is None:
        css_class = default_class

    if css_class and css_class not in class_list:
        class_list.append(css_class)

    if field.errors and "is-invalid" not in class_list:
        class_list.append("is-invalid")

    widget.attrs["class"] = " ".join(class_list)
    return field


@register.filter
def is_path_image(path: str) -> bool:
    """
    Check if the given path is an image
    """
    return path.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".avif", ".svg", ".webp"))


@register.filter
def class_name(value: Any) -> str:
    return value.__class__.__name__


@register.filter
def pagination_show_all_url(cl) -> bool:
    need_show_all_link = cl.can_show_all and not cl.show_all and cl.multi_page
    return need_show_all_link and cl.get_query_string({ALL_VAR: ""})


@register.inclusion_tag(
    "dashub/templatetags/preserve_changelist_filters.html",
    takes_context=True,
    name="preserve_filters",
)
def preserve_changelist_filters(context: Context) -> dict[str, dict[str, str]]:
    """
    Generate hidden input fields to preserve filters for POST forms.
    """
    request: Optional[HttpRequest] = context.get("request")
    changelist: Optional[ChangeList] = context.get("cl")

    if not request or not changelist:
        return {"params": {}}

    used_params: set[str] = {
        param for spec in changelist.filter_specs for param in spec.used_parameters
    }
    preserved_params: dict[str, str] = {
        param: value for param, value in request.GET.items() if param not in used_params
    }

    return {"params": preserved_params}





