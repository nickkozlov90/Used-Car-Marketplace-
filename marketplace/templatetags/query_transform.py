from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            updated[key] = value
        else:
            updated.pop(key, 0)
    return updated.urlencode()


@register.filter
def space_separate(value):
    try:
        value = int(value)
        return "{:,}".format(value).replace(",", " ")
    except (ValueError, TypeError):
        return value


@register.filter(name="add_units")
def add_measurement_units(value, units):
    try:
        formatted_value = space_separate(value)
        return f"{formatted_value} {units}"
    except (ValueError, TypeError):
        return value
