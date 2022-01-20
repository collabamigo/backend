from django.db import models

from backend import settings


class Club(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True,
                                max_length=50)
    name = models.CharField(max_length=50)
    image_links = models.TextField(default="[]", blank=False, null=False)
    college = models.CharField(max_length=100, default="IIIT-D")
    join_date = models.DateField(auto_now_add=True)
    admins = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name="clubs")
    instagram = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    github = models.CharField(max_length=100, blank=True)
    mail = models.EmailField(max_length=50, blank=True)
    telegram = models.CharField(max_length=100, blank=True)
    discord = models.CharField(max_length=100, blank=True)
    other = models.CharField(max_length=100, blank=True)
    medium = models.CharField(max_length=100, blank=True)
    memberSize = models.IntegerField(blank=False, default=0)
    tagline = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.username


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    club = models.ForeignKey(Club, related_name="announcements",
                             on_delete=models.CASCADE)

    class Meta:
        ordering = [
            '-timestamp',
            ]


class Competition(models.Model):
    id = models.AutoField(primary_key=True)
    clubs = models.ManyToManyField(Club, related_name="competitions")
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    disabled = models.BooleanField(default=False)
    event_start = models.DateTimeField()
    event_end = models.DateTimeField(blank=True, null=True)
    image_links = models.TextField(default="[]", blank=False, null=False)
    faq = models.TextField(max_length=3000, default="[]", blank=False, null=False)
    link = models.TextField(max_length=300, default="", blank=True)
    promotional_message = models.TextField()
    location = models.TextField(max_length=100, blank=True)
    winners = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name="competitionsWon",
                                     through="CompetitionWinner")
    graph_link = models.CharField(max_length=100, blank=True)
    priority = models.IntegerField(blank=False, default=0)

    class Meta:
        ordering = [
            "-priority",
            "event_start",
            "form__closes_at",
            "form__opens_at"
        ]


class CompetitionWinner(models.Model):
    id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    winner = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name="positionsWon",
                               on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    index = models.IntegerField(blank=False)
    position = models.CharField(max_length=100)

    class Meta:
        ordering = [
            'index',
            ]
