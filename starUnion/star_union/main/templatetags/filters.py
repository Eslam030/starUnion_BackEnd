from django import template
import json


register = template.Library()


@register.filter(name='to_json')
def to_json(json_string):
    after_modified = ""
    for char in json_string:
        if char == "\'":
            after_modified += '"'
        else:
            after_modified += char
    try:
        return json.loads(after_modified[1:-1])
    except json.JSONDecodeError:
        return {}


@register.filter(name='is_list')
def is_list(value):
    return isinstance(value, list)


@register.filter(name='is_dict')
def is_dict(value):
    return isinstance(value, dict)
