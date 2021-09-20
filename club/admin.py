from django.contrib import admin
from .models import Club, Competition


# Register your models here.

class ClubAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "picture", "college", "join_date", "admins",
                    "instagram", "linkedin", "facebook", "discord", "other")


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("id", "club", "on_going", "name", "description",
                    "disabled")


admin.site.register(Club, ClubAdmin)
admin.site.register(Competition, CompetitionAdmin)
