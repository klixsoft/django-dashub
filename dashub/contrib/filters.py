from typing import Generator, Any

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.db.models import QuerySet, Model, Field, DateField, DateTimeField
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from dashub.contrib.forms import RadioForm, CheckboxForm, DropdownForm, AutocompleteDropdownForm, RangeDateForm, \
    RangeDateTimeForm
from dashub.contrib.mixins import ValueMixin, ChoicesMixin, MultiValueMixin, DropdownMixin, AutocompleteMixin
from dashub.utils import parse_date_str, parse_datetime_str


class RadioFilter(admin.SimpleListFilter):
    template = "dashub/filters/filters_field.html"
    form_class = RadioForm
    all_option = ["", _("All")]

    def choices(self, changelist: ChangeList) -> tuple[dict[str, Any], ...]:
        add_facets = getattr(changelist, "add_facets", False)
        facet_counts = self.get_facet_queryset(changelist) if add_facets else None
        choices = []

        if self.all_option:
            choices = [self.all_option]

        if add_facets:
            for i, (lookup, title) in enumerate(self.lookup_choices):
                if (count := facet_counts.get(f"{i}__c", -1)) != -1:
                    title = f"{title} ({count})"
                else:
                    title = f"{title} (-)"

                choices.append((lookup, title))
        else:
            choices.extend(self.lookup_choices)

        return (
            {
                "form": self.form_class(
                    label=_(" By %(filter_title)s ") % {"filter_title": self.title},
                    name=self.parameter_name,
                    choices=choices,
                    data={self.parameter_name: self.value()},
                ),
            },
        )


class CheckboxFilter(RadioFilter):
    form_class = CheckboxForm
    all_option = None

    def value(self) -> list[Any]:
        return self.request.GET.getlist(self.parameter_name)


class ChoicesRadioFilter(ValueMixin, ChoicesMixin, admin.ChoicesFieldListFilter):
    form_class = RadioForm
    all_option = ["", _("All")]


class ChoicesCheckboxFilter(
    MultiValueMixin, ChoicesMixin, admin.ChoicesFieldListFilter
):
    form_class = CheckboxForm
    all_option = None


class BooleanRadioFilter(ValueMixin, admin.BooleanFieldListFilter):
    template = "dashub/filters/filters_field.html"
    all_option = ["", _("All")]
    form_class = RadioForm

    def choices(self, changelist: ChangeList) -> Generator[dict[str, Any], None, None]:
        add_facets = getattr(changelist, "add_facets", False)
        facet_counts = self.get_facet_queryset(changelist) if add_facets else None

        if add_facets:
            choices = [
                self.all_option,
                *[
                    ("1", f"{_('Yes')} ({facet_counts['true__c']})"),
                    ("0", f"{_('No')} ({facet_counts['false__c']})"),
                ],
            ]
        else:
            choices = [
                self.all_option,
                *[
                    ("1", _("Yes")),
                    ("0", _("No")),
                ],
            ]

        yield {
            "form": self.form_class(
                label=_(" By %(filter_title)s ") % {"filter_title": self.title},
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: self.value()},
            ),
        }


class RelatedCheckboxFilter(MultiValueMixin, admin.RelatedFieldListFilter):
    template = "dashub/filters/filters_field.html"
    form_class = CheckboxForm

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        if self.value() not in EMPTY_VALUES:
            return super().queryset(request, queryset)
        return queryset

    def choices(self, changelist: ChangeList) -> Generator[dict[str, Any], None, None]:
        add_facets = getattr(changelist, "add_facets", False)
        facet_counts = self.get_facet_queryset(changelist) if add_facets else None

        if add_facets:
            choices = []

            for pk_val, val in self.lookup_choices:
                count = facet_counts[f"{pk_val}__c"]
                choice = (pk_val, f"{val} ({count})")
                choices.append(choice)
        else:
            choices = self.lookup_choices

        yield {
            "form": self.form_class(
                label=_(" By %(filter_title)s ") % {"filter_title": self.title},
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: self.value()},
            ),
        }



class DropdownFilter(admin.SimpleListFilter):
    template = "dashub/filters/filters_field.html"
    form_class = DropdownForm
    all_option = ["", _("All")]

    def choices(self, changelist: ChangeList) -> tuple[dict[str, Any], ...]:
        return (
            {
                "form": self.form_class(
                    label=_(" By %(filter_title)s ") % {"filter_title": self.title},
                    name=self.parameter_name,
                    choices=[self.all_option, *self.lookup_choices],
                    data={self.parameter_name: self.value()},
                    multiple=self.multiple if hasattr(self, "multiple") else False,
                ),
            },
        )


class MultipleDropdownFilter(DropdownFilter):
    multiple = True

    def __init__(
        self,
        request: HttpRequest,
        params: dict[str, Any],
        model: type[Model],
        model_admin: ModelAdmin,
    ) -> None:
        self.request = request
        super().__init__(request, params, model, model_admin)

    def value(self) -> list[Any]:
        return self.request.GET.getlist(self.parameter_name)


class ChoicesDropdownFilter(ValueMixin, DropdownMixin, admin.ChoicesFieldListFilter):
    def choices(self, changelist: ChangeList) -> Generator[dict[str, Any], None, None]:
        choices = [self.all_option, *self.field.flatchoices]

        yield {
            "form": self.form_class(
                label=_(" By %(filter_title)s ") % {"filter_title": self.title},
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: self.value()},
                multiple=self.multiple if hasattr(self, "multiple") else False,
            ),
        }


class ChoicesMultipleDropdownFilter(MultiValueMixin, ChoicesDropdownFilter):
    multiple = True


class RelatedDropdownFilter(ValueMixin, DropdownMixin, admin.RelatedFieldListFilter):
    def __init__(
        self,
        field: Field,
        request: HttpRequest,
        params: dict[str, str],
        model: type[Model],
        model_admin: ModelAdmin,
        field_path: str,
    ) -> None:
        super().__init__(field, request, params, model, model_admin, field_path)
        self.model_admin = model_admin
        self.request = request

    def choices(self, changelist: ChangeList) -> Generator[dict[str, Any], None, None]:
        add_facets = getattr(changelist, "add_facets", False)
        facet_counts = self.get_facet_queryset(changelist) if add_facets else None

        if add_facets:
            choices = [self.all_option]

            for pk_val, val in self.lookup_choices:
                if add_facets:
                    count = facet_counts[f"{pk_val}__c"]
                    choice = (pk_val, f"{val} ({count})")
                    choices.append(choice)
        else:
            choices = [self.all_option, *self.lookup_choices]

        yield {
            "form": self.form_class(
                label=_(" By %(filter_title)s ") % {"filter_title": self.title},
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: self.value()},
                multiple=self.multiple if hasattr(self, "multiple") else False,
            ),
        }


class MultipleRelatedDropdownFilter(MultiValueMixin, RelatedDropdownFilter):
    multiple = True


class AutocompleteSelectFilter(AutocompleteMixin, RelatedDropdownFilter):
    form_class = AutocompleteDropdownForm


class AutocompleteSelectMultipleFilter(
    AutocompleteMixin, MultipleRelatedDropdownFilter
):
    form_class = AutocompleteDropdownForm



class RangeDateFilter(admin.FieldListFilter):
    request = None
    parameter_name = None
    form_class = RangeDateForm
    template = "dashub/filters/filters_date_range.html"

    def __init__(
        self,
        field: Field,
        request: HttpRequest,
        params: dict[str, str],
        model: type[Model],
        model_admin: ModelAdmin,
        field_path: str,
    ) -> None:
        super().__init__(field, request, params, model, model_admin, field_path)
        if not isinstance(field, DateField):
            raise TypeError(
                f"Class {type(self.field)} is not supported for {self.__class__.__name__}."
            )

        self.request = request
        if self.parameter_name is None:
            self.parameter_name = self.field_path

        if self.parameter_name + "_from" in params:
            value = params.pop(self.field_path + "_from")
            value = value[0] if isinstance(value, list) else value

            if value not in EMPTY_VALUES:
                self.used_parameters[self.field_path + "_from"] = value

        if self.parameter_name + "_to" in params:
            value = params.pop(self.field_path + "_to")
            value = value[0] if isinstance(value, list) else value

            if value not in EMPTY_VALUES:
                self.used_parameters[self.field_path + "_to"] = value

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        filters = {}

        value_from = self.used_parameters.get(self.parameter_name + "_from")
        if value_from not in EMPTY_VALUES:
            filters.update({self.parameter_name + "__gte": parse_date_str(value_from)})

        value_to = self.used_parameters.get(self.parameter_name + "_to")
        if value_to not in EMPTY_VALUES:
            filters.update({self.parameter_name + "__lte": parse_date_str(value_to)})

        try:
            return queryset.filter(**filters)
        except (ValueError, ValidationError):
            return None

    def expected_parameters(self) -> list[str]:
        return [
            f"{self.parameter_name}_from",
            f"{self.parameter_name}_to",
        ]

    def choices(self, changelist: ChangeList) -> tuple[dict[str, Any], ...]:
        return (
            {
                "request": self.request,
                "parameter_name": self.parameter_name,
                "form": self.form_class(
                    name=self.parameter_name,
                    data={
                        self.parameter_name + "_from": self.used_parameters.get(
                            self.parameter_name + "_from", None
                        ),
                        self.parameter_name + "_to": self.used_parameters.get(
                            self.parameter_name + "_to", None
                        ),
                    },
                ),
            },
        )


class RangeDateTimeFilter(admin.FieldListFilter):
    request = None
    parameter_name = None
    template = "dashub/filters/filters_datetime_range.html"
    form_class = RangeDateTimeForm

    def __init__(
        self,
        field: Field,
        request: HttpRequest,
        params: dict[str, str],
        model: type[Model],
        model_admin: ModelAdmin,
        field_path: str,
    ) -> None:
        super().__init__(field, request, params, model, model_admin, field_path)
        if not isinstance(field, DateTimeField):
            raise TypeError(
                f"Class {type(self.field)} is not supported for {self.__class__.__name__}."
            )

        self.request = request
        if self.parameter_name is None:
            self.parameter_name = self.field_path

        if self.parameter_name + "_from_0" in params:
            value = params.pop(self.field_path + "_from_0")
            value = value[0] if isinstance(value, list) else value
            self.used_parameters[self.field_path + "_from_0"] = value

        if self.parameter_name + "_from_1" in params:
            value = params.pop(self.field_path + "_from_1")
            value = value[0] if isinstance(value, list) else value
            self.used_parameters[self.field_path + "_from_1"] = value

        if self.parameter_name + "_to_0" in params:
            value = params.pop(self.field_path + "_to_0")
            value = value[0] if isinstance(value, list) else value
            self.used_parameters[self.field_path + "_to_0"] = value

        if self.parameter_name + "_to_1" in params:
            value = params.pop(self.field_path + "_to_1")
            value = value[0] if isinstance(value, list) else value
            self.used_parameters[self.field_path + "_to_1"] = value

    def expected_parameters(self) -> list[str]:
        return [
            f"{self.parameter_name}_from_0",
            f"{self.parameter_name}_from_1",
            f"{self.parameter_name}_to_0",
            f"{self.parameter_name}_to_1",
        ]

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None:
        filters = {}

        date_value_from = self.used_parameters.get(self.parameter_name + "_from_0")
        time_value_from = self.used_parameters.get(self.parameter_name + "_from_1")

        date_value_to = self.used_parameters.get(self.parameter_name + "_to_0")
        time_value_to = self.used_parameters.get(self.parameter_name + "_to_1")

        if date_value_from not in EMPTY_VALUES and time_value_from not in EMPTY_VALUES:
            filters.update(
                {
                    f"{self.parameter_name}__gte": parse_datetime_str(
                        f"{date_value_from} {time_value_from}"
                    ),
                }
            )

        if date_value_to not in EMPTY_VALUES and time_value_to not in EMPTY_VALUES:
            filters.update(
                {
                    f"{self.parameter_name}__lte": parse_datetime_str(
                        f"{date_value_to} {time_value_to}"
                    ),
                }
            )

        try:
            return queryset.filter(**filters)
        except (ValueError, ValidationError):
            return None

    def choices(self, changelist: ChangeList) -> tuple[dict[str, Any], ...]:
        return (
            {
                "request": self.request,
                "parameter_name": self.parameter_name,
                "form": self.form_class(
                    name=self.parameter_name,
                    data={
                        self.parameter_name + "_from_0": self.used_parameters.get(
                            self.parameter_name + "_from_0"
                        ),
                        self.parameter_name + "_from_1": self.used_parameters.get(
                            self.parameter_name + "_from_1"
                        ),
                        self.parameter_name + "_to_0": self.used_parameters.get(
                            self.parameter_name + "_to_0"
                        ),
                        self.parameter_name + "_to_1": self.used_parameters.get(
                            self.parameter_name + "_to_1"
                        ),
                    },
                ),
            },
        )








