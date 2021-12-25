from django.contrib import admin
from .models import Form, FormResponse, ResponseElement


class FormAdmin(admin.ModelAdmin):
    list_display = ("id", "confirmation_message", "createdAt", "updatedAt",
                    "collect_email", "competition", "skeleton")


class ResponseElementAdmin(admin.ModelAdmin):
    list_display = ("parent", "question", "value")


class ResponseElementInline(admin.TabularInline):
    model = ResponseElement


class FormResponseAdmin(admin.ModelAdmin):
    list_display = ("form",)
    inlines = [ResponseElementInline]


admin.site.register(Form, FormAdmin)
admin.site.register(FormResponse, FormResponseAdmin)
admin.site.register(ResponseElement, ResponseElementAdmin)
