from django.contrib import admin
from .models import Form, Response, TextResponse, FileResponse


class FormAdmin(admin.ModelAdmin):
    list_display = ("id", "confirmation_message", "createdAt", "updatedAt",
                    "collect_email", "competition", "skeleton")


class ResponseAdmin(admin.ModelAdmin):
    list_display = ("form", "responders")


class TextResponseAdmin(admin.ModelAdmin):
    list_display = ("parent", "question_id", "value")


class FileResponseAdmin(admin.ModelAdmin):
    list_display = ("parent", "question_id", "value")


admin.site.register(Form, FormAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(TextResponse, TextResponseAdmin)
