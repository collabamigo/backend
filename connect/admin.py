from django.contrib import admin
from .models import *
class connectCredentials(admin.ModelAdmin):
    list_display = ('_id', 'first_name', 'last_name','Age','Gender','Education','Email','Contact','handle','isvendor')


class connectTeacher(admin.ModelAdmin):
    list_display = ('Skill_set','helo')

# Register your models here.

admin.register(Credentials, connectCredentials)
admin.register(Teacher, connectTeacher)

# admin.site.register(Credentials, connectCredentials)
# admin.site.register(Teacher, connectTeacher)