from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import user_profile_images


@receiver(post_migrate)
def create_default_records(sender, **kwargs):
    print('test')
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
