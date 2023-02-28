from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def set_var(context, value):
    context["prev_cycleno"] = value
    return ""
