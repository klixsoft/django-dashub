from django import forms
from django.forms.widgets import Select, SelectMultiple


class PractetDashboardSelect(Select):
    template_name = "practet_dashboard/widgets/select.html"

    def build_attrs(self, base_attrs, extra_attrs=None):
        return {**base_attrs, **(extra_attrs or {})}

    @property
    def media(self):
        return forms.Media(
            css={"all": ("https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css",)},
            js=("https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js",),
        )


class PractetDashboardSelectMultiple(SelectMultiple):
    template_name = "practet_dashboard/widgets/select.html"

    def build_attrs(self, base_attrs, extra_attrs=None):
        extra_attrs["multiple"] = "multiple"
        return {**base_attrs, **(extra_attrs or {})}

    @property
    def media(self):
        return forms.Media(
            css={"all": ("https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css",)},
            js=("https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js",),
        )
