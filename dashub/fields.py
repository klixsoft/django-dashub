from django.db import models
from .widgets import TagInputWidget
from dashub import widgets as dashub_widgets
from django.contrib.admin import widgets as admin_widgets


class TagInputField(models.TextField):
    """ Custom ModelField that integrates with the Textarea input for tags separated by ::: """

    def __init__(self, *args, separator=":::", **kwargs):
        self.separator = separator
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        """ Ensures the correct form field and widget are used """
        defaults = {"widget": TagInputWidget}
        defaults.update(kwargs)

        if defaults["widget"] == admin_widgets.AdminTextareaWidget:
            defaults["widget"] = dashub_widgets.AdminTagInputWidget(separator=self.separator)

        return super().formfield(**defaults)

    def from_db_value(self, value, expression, connection):
        if value is None or value.strip() == "":
            return []
        return value.split(self.separator)

    def to_python(self, value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            value = value.strip()
            return value.split(self.separator) if value else []
        return []

    def get_prep_value(self, value):
        if value is None:
            return ""
        if isinstance(value, list):
            return self.separator.join(value)
        return value
