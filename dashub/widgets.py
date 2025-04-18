import json

from django import forms
from django.forms.widgets import Select, SelectMultiple
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.contrib.admin import widgets as admin_widgets


class DashubSelect(Select):
    template_name = "dashub/widgets/select.html"

    def build_attrs(self, base_attrs, extra_attrs=None):
        return {**base_attrs, **(extra_attrs or {})}

    @property
    def media(self):
        return forms.Media(
            css={"all": ("https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css",)},
            js=("https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js",),
        )


class DashubSelectMultiple(SelectMultiple):
    template_name = "dashub/widgets/select.html"

    def build_attrs(self, base_attrs, extra_attrs=None):
        extra_attrs["multiple"] = "multiple"
        return {**base_attrs, **(extra_attrs or {})}

    @property
    def media(self):
        return forms.Media(
            css={"all": ("https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css",)},
            js=("https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js",),
        )


class TagInputWidget(forms.Textarea):
    template_name = "dashub/widgets/tag_input.html"

    def __init__(self, attrs=None, separator=":::"):
        self.separator = separator
        final_attrs = {"data-separator": separator}
        if attrs:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)

    class Media:
        js = (
            "https://cdn.jsdelivr.net/npm/@yaireo/tagify",
            "https://cdn.jsdelivr.net/npm/@yaireo/tagify/dist/tagify.polyfills.min.js"
        )
        css = {"all": ("https://cdn.jsdelivr.net/npm/@yaireo/tagify/dist/tagify.css",)}

    def format_value(self, value):
        if value is not None:
            if isinstance(value, list):
                return self.separator.join(value)
            elif isinstance(value, str):
                return value.strip()
        return ""


class AdminTagInputWidget(TagInputWidget, admin_widgets.AdminTextareaWidget):
    pass
