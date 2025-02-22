from django import template

register = template.Library()

@register.filter
def format_large_number(value):
    try:
        value = float(value)
        if value >= 1_000_000_000_000:
            return f"{value / 1_000_000_000_000:.2f} trillion"
        elif value >= 1_000_000_000:
            return f"{value / 1_000_000_000:.2f} billion"
        elif value >= 1_000_000:
            return f"{value / 1_000_000:.2f} million"
        elif value >= 1_000:
            return f"{value / 1_000:.2f} thousand"
        else:
            return str(value)
    except (ValueError, TypeError):
        return value