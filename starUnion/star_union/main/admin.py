from django.contrib import admin
from django.apps import apps

models = []
models.append(apps.get_app_config('events').get_models())
models.append(apps.get_app_config('workshops').get_models())
models.append(apps.get_app_config('main').get_models())

for app_models in models:
    for model in app_models:
        if not admin.site.is_registered(model):
            admin.site.register(model)
