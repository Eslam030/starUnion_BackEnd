from typing import Any
from django.contrib import admin
from django.apps import apps
from .models import partnerForm


class partnerAdmin (admin.ModelAdmin):
    form = partnerForm


models = apps.get_app_config('events').get_models()
for model in models:
    if not admin.site.is_registered(model):
        if model.__name__ != 'partnrships':
            admin.site.register(model)
        else:
            admin.site.register(model, partnerAdmin)

# Register your models here.
