from django.db.models.signals import post_save
from django.dispatch import receiver
from connect.models import Profile, Teacher
from connect.emailhandler import new_teacher_email


@receiver(post_save, sender=Teacher)
def profile_isteacher_true(sender, instance, created, **kwargs):
    if created:
        print(instance.id, flush=True)
        b = Profile.objects.get(id=str(instance.id))
        person = {
            "Id": b.id,
            "Name": b.First_Name + " " + b.Last_Name,
            "Email": str((b.email).email)
            }
        new_teacher_email(person)


@receiver(post_save, sender=Teacher)
def profile_isteacher_false(sender, instance, **kwargs):
    print(instance.id, flush=True)
