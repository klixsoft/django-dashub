from typing import Optional, Any

from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminSplitDateTime, AdminDateWidget, AdminTimeWidget
from django.forms.widgets import Select, SelectMultiple, CheckboxSelectMultiple, MultiWidget
from django.contrib.admin import widgets as admin_widgets, VERTICAL
from django.utils.translation import gettext_lazy as _


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


class DashubAdminRadioSelectWidget(AdminRadioSelect):
    template_name = "dashub/widgets/radio.html"
    option_template_name = "dashub/widgets/radio_option.html"
    RADIO_CLASSES = ["form-check-input"]

    def __init__(self, radio_style: Optional[int] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if radio_style is None:
            radio_style = VERTICAL
        self.radio_style = radio_style
        self.attrs["class"] = " ".join([*self.RADIO_CLASSES, self.attrs.get("class", "")])

    def get_context(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context(*args, **kwargs)
        context.update({"radio_style": self.radio_style})
        return context


class DashubAdminCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = "dashub/widgets/radio.html"
    option_template_name = "dashub/widgets/radio_option.html"
    CHECKBOX_CLASSES = ["form-check-input"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs["class"] = " ".join([*self.CHECKBOX_CLASSES, self.attrs.get("class", "")])


class DashubAdminDateWidget(AdminDateWidget):
    template_name = "dashub/widgets/date.html"
    DATETIME_CLASSES = ["form-control"]

    def __init__(
        self, attrs: Optional[dict[str, Any]] = None, format: Optional[str] = None
    ) -> None:
        attrs = {
            **(attrs or {}),
            "class": " ".join(
                [
                    "vDateField",
                    *self.DATETIME_CLASSES,
                    attrs.get("class", "") if attrs else "",
                ]
            ),
            "size": "10",
        }
        super().__init__(attrs=attrs, format=format)


class DashubAdminTimeWidget(AdminTimeWidget):
    template_name = "dashub/widgets/time.html"
    DATETIME_CLASSES = ["form-control"]

    def __init__(
        self, attrs: Optional[dict[str, Any]] = None, format: Optional[str] = None
    ) -> None:
        attrs = {
            **(attrs or {}),
            "class": " ".join(
                [
                    "vTimeField",
                    *self.DATETIME_CLASSES,
                    attrs.get("class", "") if attrs else "",
                ]
            ),
            "size": "8",
        }
        super().__init__(attrs=attrs, format=format)


class DashubAdminSplitDateTimeVerticalWidget(AdminSplitDateTime):
    template_name = "dashub/widgets/split_datetime_vertical.html"

    def __init__(
        self,
        attrs: Optional[dict[str, Any]] = None,
        date_attrs: Optional[dict[str, Any]] = None,
        time_attrs: Optional[dict[str, Any]] = None,
        date_label: Optional[str] = None,
        time_label: Optional[str] = None,
    ) -> None:
        self.date_label = date_label
        self.time_label = time_label

        widgets = [
            DashubAdminDateWidget(attrs=date_attrs),
            DashubAdminTimeWidget(attrs=time_attrs),
        ]
        MultiWidget.__init__(self, widgets, attrs)

    def get_context(
        self, name: str, value: Any, attrs: Optional[dict[str, Any]]
    ) -> dict[str, Any]:
        context = super().get_context(name, value, attrs)

        if self.date_label is not None:
            context["date_label"] = self.date_label
        else:
            context["date_label"] = _("Date")

        if self.time_label is not None:
            context["time_label"] = self.time_label
        else:
            context["time_label"] = _("Time")

        return context


