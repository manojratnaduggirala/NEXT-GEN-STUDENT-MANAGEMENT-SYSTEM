from django import template

register = template.Library()

@register.filter
def split_lines(value):
    """Split text by newlines and return list of non-empty lines"""
    if not value:
        return []
    return [line.strip() for line in value.split('\n') if line.strip()]

@register.filter
def add_class(field, css_class):
    """Add CSS class to form field"""
    return field.as_widget(attrs={"class": css_class})
