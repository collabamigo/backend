from django.contrib import admin
from .models import Club, Competition, Announcements


# Register your models here.

class ClubAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "picture", "college", "join_date",
                    "instagram", "linkedin", "facebook", "discord", "other",
                    "memberSize", "tagline", "description")


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("id", "on_going", "name", "description",
                    "disabled")


class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = ('id', 'content')


admin.site.register(Club, ClubAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Announcements, AnnouncementsAdmin)
