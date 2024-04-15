# here we will implement event database signals
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete
import shutil
import os
from .models import events


def getLast(directory):
    last = ""
    for i in range(len(directory) - 1, -1, -1):
        if directory[i] == "\\":
            break
        last = last + directory[i]
    reversed_last = last[::-1]
    return (reversed_last)


@receiver(m2m_changed, sender=events.event_photos.through)
def create_comms_group(sender, instance, action, **kwargs):
    if action == 'post_add':
        # edit the path of the photo
        for photo in instance.event_photos.all():
            print(photo)
            new_path = settings.BASE_DIR / \
                ("events/EveryEventData/" + instance.name + "/photos/")
            if not os.path.exists(new_path):
                os.mkdir(new_path)
            new_path = new_path / getLast(str(photo.photo.path))
            if not os.path.exists(new_path):
                shutil.copyfile(photo.photo.path, new_path)
            os.remove(photo.photo.path)
            photo.photo = str(new_path)
            photo.save()
    if action == 'pre_remove':
        print(instance.event_photos.all())
    if action == 'post_remove':
        # delete the deleted photo
        print(instance.event_photos.all())


@receiver(pre_delete, sender=events)
def create_comms_group(sender, instance, **kwargs):
    print(instance.name)
    print(instance.event_photos.all())
    for photo in instance.evenet_photos.all():
        print(instance.event_photos.through.objects.all().filter(photo))
