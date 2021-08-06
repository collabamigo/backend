from django.contrib import admin
from .models import Club
# Competition, Entries, Choices, Form, Question,
#       Answer, Response


# Register your models here.
class ClubAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "link", "picture", "college", "join_date",)


admin.site.register(Club, ClubAdmin)
