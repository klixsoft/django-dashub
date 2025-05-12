from django.db import models
from .widgets import TagInputWidget
from dashub import widgets as dashub_widgets
from django.contrib.admin import widgets as admin_widgets


class TagInputField(models.TextField):
    """
    Custom ModelField that stores a string of tags separated by a custom separator,
    but presents and accepts data as a list in Python.
    """

    def __init__(self, *args, separator=":::", **kwargs):
        self.separator = separator
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        """Use custom widget for both regular and admin forms"""
        widget = kwargs.get("widget", TagInputWidget)

        if widget == admin_widgets.AdminTextareaWidget:
            widget = dashub_widgets.AdminTagInputWidget(separator=self.separator)

        kwargs["widget"] = widget
        return super().formfield(**kwargs)

    def from_db_value(self, value, expression, connection):
        if not value:
            return []
        return value.split(self.separator)

    def to_python(self, value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        value = value.strip()
        return value.split(self.separator) if value else []

    def get_prep_value(self, value):
        if value is None:
            return ""
        if isinstance(value, list):
            return self.separator.join(value)
        return value

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['separator'] = self.separator
        return name, path, args, kwargs
