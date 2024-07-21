# here we will implement event database signals
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete, post_save, pre_save
import shutil
import os
from .models import *
from threading import local
from pathlib import Path
from django import forms


# This is a set to store the photos before they are removed
before = set()
logo = []

# handle the event_photos m2m_changed signal
# specficly the post_add and pre_remove signals


@receiver(m2m_changed, sender=events.event_photos.through)
def post_add_signal(sender, instance, action, **kwargs):
    if action == 'post_add':
        # edit the path of the photo
        for photo in instance.event_photos.all():
            # create the new path
            new_path = settings.BASE_DIR / \
                ("events/EveryEventData/" + instance.name + "/photos/")
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            new_path = new_path / str(photo.photo.path).split("\\")[-1]
            # copy the photo to the new path
            if not os.path.exists(new_path):
                shutil.copyfile(photo.photo.path, new_path)
            # remove the old photo if it is not the same as the new one
            if not os.path.samefile(photo.photo.path, new_path):
                os.remove(photo.photo.path)
                photo.photo = str(new_path)
                photo.save()

# handle the pre_remove signal to handle the photos that are removed


@receiver(m2m_changed, sender=events.event_photos.through)
def pre_remove_signal(sender, instance, action, **kwargs):
    if action == 'pre_remove':
        for photo in instance.event_photos.all():
            before.add(photo.id)

# handle the post_remove signal to remove the photos that are removed


@receiver(m2m_changed, sender=events.event_photos.through)
def post_remove_signal(sender, instance, action, **kwargs):
    if action == 'post_remove':
        after = set()
        for photo in instance.event_photos.all():
            after.add(photo.id)

        diff = before.difference(after)
        for photo_id in diff:
            photo = photos.objects.get(id=photo_id)
            if photo is not None:
                photo.delete()

# delete event path after it is removed


@receiver(pre_delete, sender=events)
def handle_events_files(sender, instance, **kwargs):
    if os.path.exists(settings.BASE_DIR / "events/EveryEventData/" / instance.name):
        shutil.rmtree(settings.BASE_DIR /
                      "events/EveryEventData/" / instance.name)

# delete photo path after it is removed


@receiver(pre_delete, sender=photos)
def handle_photos_files(sender, instance, **kwargs):
    if os.path.exists(instance.photo.path):
        os.remove(instance.photo.path)


@receiver(pre_save)
def handle_logo_routing(sender, instance, **kwargs):
    if sender == events or sender == company:
        log = events.objects.filter(name=instance.name).first()
        if log != None and log.logo.name != "":
            logo.append(log.logo.path)


models_with_logos = [events, sponsors, partnrships, company, special_events]


@receiver(post_save)
def handle_logo_routing(sender, instance, **kwargs):
    if sender in models_with_logos:
        if instance.logo.name != None and instance.logo.name != "":
            if len(logo) > 0:
                if logo[0] != instance.logo.path:
                    if os.path.exists(logo[0]):
                        os.remove(logo[0])
            name_for_path = sender.__name__[0].upper() + sender.__name__[1:-1]
            if sender == company:
                name_for_path = "Company"
            if sender == special_events:
                name_for_path = "Event"

            new_path = settings.BASE_DIR / \
                ("events/Every" + name_for_path +
                 "Data/" + instance.name + "/logos/")
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            logo_path = str(instance.logo.path).replace("/", "\\")
            new_path = new_path / logo_path.split("\\")[-1]
            if not os.path.exists(new_path):
                shutil.copyfile(instance.logo.path, new_path)
            if not os.path.samefile(instance.logo.path, new_path):
                os.remove(instance.logo.path)
                instance.logo = str(new_path)
                instance.save()
        else:
            if len(logo) > 0:
                for logo_name in logo:
                    if os.path.exists(logo_name):
                        os.remove(logo_name)
        logo.clear()


@receiver(post_save)
def handle_logo_routing(sender, instance, **kwargs):
    if sender == special_events:
        if instance.form_photo.name != None and instance.form_photo.name != "":
            if len(logo) > 0:
                if logo[0] != instance.form_photo.path:
                    if os.path.exists(logo[0]):
                        os.remove(logo[0])

            name_for_path = "Event"

            new_path = settings.BASE_DIR / \
                ("events/Every" + name_for_path +
                 "Data/" + instance.name + "/form_logo/")
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            logo_path = str(instance.form_photo.path).replace("/", "\\")
            new_path = new_path / logo_path.split("\\")[-1]
            if not os.path.exists(new_path):
                shutil.copyfile(instance.form_photo.path, new_path)
            if not os.path.samefile(instance.form_photo.path, new_path):
                os.remove(instance.form_photo.path)
                instance.form_photo = str(new_path)
                instance.save()
        else:
            if len(logo) > 0:
                for logo_name in logo:
                    if os.path.exists(logo_name):
                        os.remove(logo_name)
        logo.clear()
