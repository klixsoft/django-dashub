from typing import Optional, Generator, Any

from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.core.validators import EMPTY_VALUES
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.db.models.fields import BLANK_CHOICE_DASH, Field
from dashub.contrib.forms import DropdownForm, AutocompleteDropdownForm


class ValueMixin:
    def value(self) -> Optional[str]:
        return (
            self.lookup_val[0]
            if self.lookup_val not in EMPTY_VALUES
               and isinstance(self.lookup_val, list)
               and len(self.lookup_val) > 0
            else self.lookup_val
        )


class MultiValueMixin:
    def value(self) -> Optional[list[str]]:
        return (
            self.lookup_val
            if self.lookup_val not in EMPTY_VALUES
            and isinstance(self.lookup_val, list)
            and len(self.lookup_val) > 0
            else self.lookup_val
        )


class ChoicesMixin:
    template = "dashub/filters/filters_field.html"

    def choices(self, changelist: ChangeList) -> Generator[dict[str, Any], None, None]:
        add_facets = getattr(changelist, "add_facets", False)
        facet_counts = self.get_facet_queryset(changelist) if add_facets else None
        choices = [self.all_option] if self.all_option else []

        for i, choice in enumerate(self.field.flatchoices):
            if add_facets:
                count = facet_counts[f"{i}__c"]
                choice = (choice[0], f"{choice[1]} ({count})")

            choices.append(choice)

        yield {
            "form": self.form_class(
                label=_(" By %(filter_title)s ") % {"filter_title": self.title},
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: self.value()},
            ),
        }


class DropdownMixin:
    template = "dashub/filters/filters_field.html"
    form_class = DropdownForm
    all_option = ["", _("All")]

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        if self.value() not in EMPTY_VALUES:
            return super().queryset(request, queryset)

        return queryset



class AutocompleteMixin:
    def has_output(self) -> bool:
        return True

    def field_choices(
        self, field: Field, request: HttpRequest, model_admin: ModelAdmin
    ) -> list[tuple[str, list[tuple[str, str]]]]:
        return [
            ("", BLANK_CHOICE_DASH),
        ]

    def choices(
        self, changelist: ChangeList
    ) -> Generator[dict[str, AutocompleteDropdownForm], None, None]:
        yield {
            "form": self.form_class(
                request=self.request,
                label=_(" By %(filter_title)s ") % {"filter_title": self.title},
                name=self.lookup_kwarg,
                choices=(),
                field=self.field,
                model_admin=self.model_admin,
                data={self.lookup_kwarg: self.value()},
                multiple=self.multiple if hasattr(self, "multiple") else False,
            ),
        }


