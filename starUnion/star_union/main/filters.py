from django import template
import json

register = template.Library()


@register.filter(name='to_json')
def to_json(json_string):
    return json.loads(json_string)
