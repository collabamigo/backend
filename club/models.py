from django.db import models


class Club(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True,
                                max_length=50)
    name = models.CharField(max_length=50)
    picture = models.CharField(max_length=100)  # url
    college = models.CharField(max_length=100, default="IIIT-D")
    join_date = models.DateField(auto_now_add=True)
    admins = models.ManyToManyField(to="auth.User", related_name="clubs")
    instagram = models.URLField(max_length=100, blank=True)
    linkedin = models.URLField(max_length=100, blank=True)
    facebook = models.URLField(max_length=100, blank=True)
    discord = models.URLField(max_length=100, blank=True)
    other = models.URLField(max_length=100, blank=True)
    memberSize = models.IntegerField(blank=False, default=1)
    tagline = models.CharField(max_length=100)
    description = models.TextField(max_length=100)

    def __str__(self):
        return self.username


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    club = models.ForeignKey(Club, related_name="announcements",
                             on_delete=models.CASCADE)


class Competition(models.Model):
    id = models.AutoField(primary_key=True)
    clubs = models.ManyToManyField(Club, related_name="competitions")
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=280, blank=True)
    disabled = models.BooleanField(default=False)
    event_start = models.DateTimeField()
    event_end = models.DateTimeField(blank=True, null=True)
    image_links = models.TextField(max_length=250, blank=True)
    faq = models.TextField(max_length=3000, blank=True)
    link = models.TextField(max_length=100, blank=True)
    location = models.TextField(max_length=100, blank=True)
