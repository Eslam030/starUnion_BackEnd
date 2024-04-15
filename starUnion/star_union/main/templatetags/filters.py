from django import template
import json


register = template.Library()


@register.filter(name='to_json')
def to_json(json_string):
    after_modified = ""
    for char in json_string:
        if char == "\'":
            after_modified += '"'
        elif char == "\"":
            after_modified += "'"
        else:
            after_modified += char
    return json.loads(after_modified[1:-1])
