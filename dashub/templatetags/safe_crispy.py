from django import template
from django.conf import settings

register = template.Library()

@register.filter
def is_crispy_form(form):
    """
    Check if the form is a crispy form.
    """
    try:
        from crispy_forms.helper import FormHelper
    except ImportError:
        return False

    if not "crispy_forms" in settings.INSTALLED_APPS:
        return False

    return hasattr(form, 'helper') and isinstance(form.helper, FormHelper)

@register.simple_tag(takes_context=True)
def safe_crispy(context, form):
    """
    Render form with crispy if crispy is installed and form is crispy,
    else just render the form as HTML.
    """
    try:
        from crispy_forms.utils import render_crispy_form
        return render_crispy_form(form, None, context)
    except ImportError:
        pass
    return str(form)
