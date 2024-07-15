from django.db.models.signals import post_migrate , pre_delete
from django.dispatch import receiver
from .models import user_profile_images
import os

@receiver(post_migrate)
def create_default_records(sender, **kwargs):
    if sender.name == 'main':  # Replace 'app' with the name of your app
        # Check if default records exist
        if not user_profile_images.objects.exists():
            # Create default records
            user_profile_images.objects.create(
                photo='star_union/assets/Cartoon01.png')
            user_profile_images.objects.create(
                photo='star_union/assets/Cartoon02.png')
            user_profile_images.objects.create(
                photo='star_union/assets/Cartoon03.png')
            user_profile_images.objects.create(
                photo='star_union/assets/Cartoon04.png')
            user_profile_images.objects.create(
                photo='star_union/assets/Profile Avatar.png')


@receiver(pre_delete, sender=user_profile_images)
def handle_photos_files(sender, instance, **kwargs):
    if os.path.exists(instance.photo.path):
        os.remove(instance.photo.path)