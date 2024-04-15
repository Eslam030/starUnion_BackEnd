from django.contrib import admin
from django.apps import apps
from django.conf import settings

models = apps.get_app_config('main').get_models()


class AdminForms(admin.ModelAdmin):

    change_form_template = str(
        settings.BASE_DIR / 'main/templates/customForm.html')


for model in models:
    if not admin.site.is_registered(model):
        if model != 'Forms':
            admin.site.register(model, AdminForms)
        else:
            admin.site.register(model)
