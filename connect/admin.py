
from django.contrib import admin
from .models import *


class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'fist_name', 'last_name', 'age', 'gender',
                    'education', 'email;', 'contact', 'handle', 'isvendor')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'Skill_set')


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'Teacher_set')


admin.site.register(Todo, TodoAdmin)
admin.site.register(Profile, ProfieAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Skill, SkillAdmin)
