
from django.contrib import admin
from .models import Todo, Profile, Teacher, Skill


class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'completed')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'age', 'gender',
                    'education', 'email', 'contact', 'handle', 'isteacher')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'Skill_set')


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'Teacher_set')


admin.site.register(Todo, TodoAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Skill, SkillAdmin)
