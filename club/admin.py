from django.contrib import admin
from .models import Club, Competition


# Register your models here.

class ClubAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "link", "picture", "college", "join_date",)


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("id", "club", "on_going",)


admin.site.register(Club, ClubAdmin)
admin.site.register(Competition, CompetitionAdmin)
