from django import template

register = template.Library()


@register.filter(name='detect_type')
def detect_type(input_html, type_html=''):
    """
    Check if given input has given type or check if tag has any type
    """
    if len(type_html) == 0:
        return 'type' in str(input_html).lower()
    else:
        return f'type="{type_html}"' in str(input_html).lower()