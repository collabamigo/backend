from django.contrib import admin
from .models import Idea


# Register your models here.
class IdeaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "idea", "visibility",
                    "estimate_time", "team_size", "tags", "stage", "college",
                    "join_date")


admin.site.register(Idea, IdeaAdmin)
