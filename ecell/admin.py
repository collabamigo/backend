from django.contrib import admin
from .models import Idea


class IdeaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "hidden", "team_size", "stage", "startedOn")


admin.site.register(Idea, IdeaAdmin)
