from django.contrib import admin
from .models import Idea


# Register your models here.
class IdeaAdmin(admin.ModelAdmin):
    list_display = ("id", "role", "name", "profile", "idea", "visibility",
                    "stage", "college", "join_date")


admin.site.register(Idea, IdeaAdmin)
