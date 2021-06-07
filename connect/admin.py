from django.contrib import admin
from .models import Profile, Teacher


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'First_Name', 'Last_Name', 'gender',
                    'degree', 'course', 'email', 'handle', )


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'Contact', 'UpVotes', 'DownVotes', 'Gitname',
                    'Linkedin', 'Created', )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Teacher, TeacherAdmin)
