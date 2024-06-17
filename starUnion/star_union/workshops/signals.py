from django.db.models.signals import pre_save, post_save, pre_delete, m2m_changed
from django.dispatch import receiver
from .models import workshops, photos
from django.dispatch import receiver
import os
import shutil
from django.conf import settings
logo = []
before = set()


# handle the workshops_photos m2m_changed signal
# specficly the post_add and pre_remove signals


@receiver(m2m_changed, sender=workshops.workshop_photos.through)
def post_add_signal(sender, instance, action, **kwargs):
    if action == 'post_add':
        # edit the path of the photo
        for photo in instance.workshop_photos.all():
            # create the new path
            new_path = settings.BASE_DIR / \
                ("workshops/EveryWorkshopData/" + instance.name + "/photos/")
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


@receiver(m2m_changed, sender=workshops.workshop_photos.through)
def pre_remove_signal(sender, instance, action, **kwargs):
    if action == 'pre_remove':
        for photo in instance.workshop_photos.all():
            before.add(photo.id)

# handle the post_remove signal to remove the photos that are removed


@receiver(m2m_changed, sender=workshops.workshop_photos.through)
def post_remove_signal(sender, instance, action, **kwargs):
    if action == 'post_remove':
        after = set()
        for photo in instance.workshop_photos.all():
            after.add(photo.id)

        diff = before.difference(after)
        for photo_id in diff:
            photo = photos.objects.get(id=photo_id)
            if photo is not None:
                photo.delete()


@receiver(pre_save, sender=workshops)
def handle_logo_routing(sender, instance, **kwargs):
    log = workshops.objects.filter(name=instance.name).first()
    if log != None and log.logo.name != "":
        logo.append(log.logo.path)


@receiver(post_save,  sender=workshops)
def handle_logo_routing(sender, instance, **kwargs):
    if instance.logo.name != "" and instance.logo.path != None:
        if len(logo) > 0:
            if logo[0] != instance.logo.path:
                if os.path.exists(logo[0]):
                    os.remove(logo[0])
        name_for_path = sender.__name__[0].upper() + sender.__name__[1:-1]
        new_path = settings.BASE_DIR / \
            ("workshops/Every" + name_for_path +
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


# delete workshop path after it is removed


@receiver(pre_delete, sender=workshops)
def handle_workshops_files(sender, instance, **kwargs):
    if os.path.exists(settings.BASE_DIR / "workshops/EveryWorkshopData/" / instance.name):
        shutil.rmtree(settings.BASE_DIR /
                      "workshops/EveryWorkshopData/" / instance.name)


# delete photo path after it is removed
@receiver(pre_delete, sender=photos)
def handle_photos_files(sender, instance, **kwargs):
    if os.path.exists(instance.photo.path):
        os.remove(instance.photo.path)
