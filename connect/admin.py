
from django.contrib import admin
from .models import Todo, Profile, Teacher


class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'First_Name', 'Last_Name', 'Gender',
                    'Degree', 'Course', 'Email', 'Handle',
                    'IsTeacher')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'First_Name', 'Last_Name', 'Gender',
                    'Degree', 'Course', 'email', 'Handle',
                    'IsTeacher', 'Created')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'Contact', 'UpVotes', 'DownVotes')


admin.site.register(Todo, TodoAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Teacher, TeacherAdmin)
