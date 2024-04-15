# here we will implement event database signals
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete
import shutil
import os
from .models import *
from threading import local


# This is a set to store the photos before they are removed
before = set()

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
                os.mkdir(new_path)
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
def create_comms_group(sender, instance, **kwargs):
    shutil.rmtree(settings.BASE_DIR / "events/EveryEventData/" / instance.name)

# delete photo path after it is removed


@receiver(pre_delete, sender=photos)
def create_comms_group(sender, instance, **kwargs):
    print(instance.photo.path)
    if os.path.exists(instance.photo.path):
        os.remove(instance.photo.path)
