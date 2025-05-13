from django.forms import MultipleChoiceField, forms, ChoiceField, CheckboxSelectMultiple, RadioSelect

from dashub.widgets import DashubAdminCheckboxSelectMultiple, DashubAdminRadioSelectWidget


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
