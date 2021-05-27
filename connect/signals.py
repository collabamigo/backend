from django.db.models.signals import post_save
from django.dispatch import receiver
from connect.models import Profile, Teacher


@receiver(post_save, sender=Teacher)
def profile_isteacher_true(sender, instance, created, **kwargs):
    if created:
        print(instance.id, flush=True)
        Profile.objects.get(str(instance.id)).update(IsTeacher=True)


@receiver(post_save, sender=Teacher)
def profile_isteacher_false(sender, instance, **kwargs):
    print(instance.id, flush=True)
    Profile.objects.get(str(instance.id)).update(IsTeacher=False)


def varia():
    print("leave ")
