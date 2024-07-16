from django.db.models.signals import post_migrate, pre_delete, pre_save, post_save
from django.dispatch import receiver
from .models import user_profile_images
import os
from django.conf import settings
import shutil


logo = []


def check_path(path):
    return os.path.exists(settings.BASE_DIR / path)


def make_photo_record(path):
    if check_path(path):
        user_profile_images.objects.create(
            photo=path)


@receiver(post_migrate)
def create_default_records(sender, **kwargs):
    if sender.name == 'main':
        # Check if default records exist
        # Create default records
        make_photo_record('star_union/assets/Male.png')
        make_photo_record('star_union/assets/Female.png')
        make_photo_record('star_union/assets/Baby_Male.png')
        make_photo_record('star_union/assets/Baby_Female.png')
        make_photo_record('star_union/assets/Profile Avatar.png')


@receiver(pre_delete, sender=user_profile_images)
def handle_photos_files(sender, instance, **kwargs):
    if os.path.exists(instance.photo.path):
        os.remove(instance.photo.path)


@receiver(pre_save, sender=user_profile_images)
def handle_logo_routing(sender, instance, **kwargs):
    # print(user_profile_images.objects.all().values())
    # wanted_path = settings.BASE_DIR / "main/user_profile_images" / \
    #     str(instance.photo.path).split("\\")[-1]

    # print(str(instance.photo.path).split("\\")[-1])
    # wanted_path = str(wanted_path).replace("\\", "\\\\")
    # print(wanted_path)
    log = user_profile_images.objects.filter(
        photo__contains=instance.photo.name).first()
    if log != None and log.photo.name != "":
        if log.id != instance.id:
            raise Exception("This photo is already exist")
        logo.append(log.photo.path)


@receiver(post_save, sender=user_profile_images)
def handle_photo_routing(sender, instance, **kwargs):
    if instance.photo.name != None and instance.photo.name != "":
        if len(logo) > 0:
            if logo[0] != instance.photo.path:
                if os.path.exists(logo[0]):
                    os.remove(logo[0])
        name_for_path = sender.__name__[0].upper() + sender.__name__[1:]
        new_path = settings.BASE_DIR / \
            ("main/" + name_for_path)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        logo_path = str(instance.photo.path).replace("/", "\\")
        new_path = new_path / logo_path.split("\\")[-1]
        if not os.path.exists(new_path):
            shutil.copyfile(instance.photo.path, new_path)
        if not os.path.samefile(instance.photo.path, new_path):
            os.remove(instance.photo.path)
            instance.photo = str(new_path)
            instance.save()
    else:
        if len(logo) > 0:
            for logo_name in logo:
                if os.path.exists(logo_name):
                    os.remove(logo_name)
    logo.clear()
