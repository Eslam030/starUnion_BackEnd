from django.db.models.signals import pre_save
from .models import workshops
from django.dispatch import receiver


@receiver(pre_save, sender=workshops)
def workshop_pre_save(sender, instance, **kwargs):
    if instance.start_date > instance.end_date:
        raise ValueError("End date must be after start date")
    else:
        pass
        # instance.save()
