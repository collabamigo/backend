
from django.contrib import admin
from .models import Todo, Profile, Teacher, Skill


class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'First_Name', 'Last_Name', 'Gender',
                    'Degree', 'Course', 'Email', 'Handle',
                    'IsTeacher')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'First_Name', 'Last_Name', 'Gender',
                    'Degree', 'Course', 'email', 'Handle',
                    'IsTeacher', 'Created')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'Skill_set', 'Contact')


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'Teacher_set')


admin.site.register(Todo, TodoAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Skill, SkillAdmin)
