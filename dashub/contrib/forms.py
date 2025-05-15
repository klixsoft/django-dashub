from django.contrib.admin.widgets import AutocompleteSelect, AutocompleteSelectMultiple
from django.forms import MultipleChoiceField, ChoiceField, CheckboxSelectMultiple, RadioSelect, ModelMultipleChoiceField
from django import forms
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from dashub.widgets import DashubAdminCheckboxSelectMultiple, DashubAdminRadioSelectWidget, DashubSelect, \
    DashubSelectMultiple, DashubAdminSplitDateTimeVerticalWidget


class CheckboxForm(forms.Form):
    field = MultipleChoiceField
    widget = DashubAdminCheckboxSelectMultiple

    def __init__(
        self,
        name: str,
        label: str,
        choices: tuple,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.fields[name] = self.field(
            label=label,
            required=False,
            choices=choices,
            widget=self.widget,
        )


class RadioForm(CheckboxForm):
    field = ChoiceField
    widget = DashubAdminRadioSelectWidget


class DropdownForm(forms.Form):
    widget = DashubSelect()
    field = ChoiceField

    def __init__(
        self,
        name: str,
        label: str,
        choices: tuple,
        multiple: bool = False,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        if multiple:
            self.widget = DashubSelectMultiple()
            self.field = MultipleChoiceField

        self.fields[name] = self.field(
            label=label,
            required=False,
            choices=choices,
            widget=self.widget,
        )



class AutocompleteDropdownForm(forms.Form):
    field = forms.ModelChoiceField
    widget = AutocompleteSelect

    def __init__(
        self,
        request: HttpRequest,
        name: str,
        label: str,
        choices: tuple,
        field,
        model_admin,
        multiple: bool = False,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        if multiple:
            self.field = ModelMultipleChoiceField
            self.widget = AutocompleteSelectMultiple

        self.fields[name] = self.field(
            label=label,
            required=False,
            queryset=field.remote_field.model.objects,
            widget=self.widget(field, model_admin.admin_site),
        )


class RangeDateForm(forms.Form):
    INPUT_CLASSES = ["form-control"]

    def __init__(self, name: str, *args, **kwargs) -> None:
        self.name = name
        super().__init__(*args, **kwargs)

        self.fields[self.name + "_from"] = forms.DateField(
            label="",
            required=False,
            widget=forms.DateInput(
                attrs={
                    "placeholder": _("From"),
                    "class": "vDateField vCustomDateField " + " ".join(self.INPUT_CLASSES),
                }
            ),
        )
        self.fields[self.name + "_to"] = forms.DateField(
            label="",
            required=False,
            widget=forms.DateInput(
                attrs={
                    "placeholder": _("To"),
                    "class": "vDateField vCustomDateField " + " ".join(self.INPUT_CLASSES),
                }
            ),
        )


class RangeDateTimeForm(forms.Form):
    INPUT_CLASSES = ["form-control"]
    def __init__(self, name: str, *args, **kwargs) -> None:
        self.name = name
        super().__init__(*args, **kwargs)

        self.fields[self.name + "_from"] = forms.SplitDateTimeField(
            label="",
            required=False,
            widget=DashubAdminSplitDateTimeVerticalWidget(
                date_label="",
                date_attrs={
                    "placeholder": _("Date from"),
                    "class": "vCustomDateField " + " ".join(self.INPUT_CLASSES),
                },
                time_label="",
                time_attrs={
                    "placeholder": _("Time"),
                    "class": "vCustomTimeField " + " ".join(self.INPUT_CLASSES),
                },
            ),
        )
        self.fields[self.name + "_to"] = forms.SplitDateTimeField(
            label="",
            required=False,
            widget=DashubAdminSplitDateTimeVerticalWidget(
                date_label="",
                date_attrs={
                    "placeholder": _("Date to"),
                    "class": "vCustomDateField " + " ".join(self.INPUT_CLASSES),
                },
                time_label="",
                time_attrs={
                    "placeholder": _("Time"),
                    "class": "vCustomTimeField " + " ".join(self.INPUT_CLASSES),
                },
            ),
        )


