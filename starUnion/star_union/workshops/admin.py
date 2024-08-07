from django.contrib import admin
from django.apps import apps
from django.conf import settings
from .models import workshopForm


class AdminCustomForms(admin.ModelAdmin):
    form = workshopForm
    change_form_template = str(
        settings.BASE_DIR / 'workshops/templates/customForm.html')


class AdminRegisterWorkshop(admin.ModelAdmin):
    change_form_template = str(
        settings.BASE_DIR / 'workshops/templates/fomRegistration.html')


models = (apps.get_app_config('workshops').get_models())
for model in models:
    if not admin.site.is_registered(model):
        if model.__name__ == 'workshops':
            admin.site.register(model, AdminCustomForms)
        elif model.__name__ == 'workshopRegister':
            admin.site.register(model, AdminRegisterWorkshop)
        else:
            admin.site.register(model)
            # Register your models here.
