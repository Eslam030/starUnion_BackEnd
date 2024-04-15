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
    print(after_modified[1:-1])
    try:
        return json.loads(after_modified[1:-1])
    except json.JSONDecodeError:
        return {}
