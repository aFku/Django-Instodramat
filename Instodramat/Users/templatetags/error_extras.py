from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='error_as_li')
def error_as_li(non_field_error, css_class=None):
    """
    Filter for returning non_field_errors as <li> tag only without <ul>
    """
    content = ''
    if css_class:
        for error in non_field_error:
            content += f'<li class={css_class}>' + error + '</li>\n'
    else:
        for error in non_field_error:
            content += f'<li>' + error + '</li>\n'
    return mark_safe(content)
