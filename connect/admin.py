from django.contrib import admin

class connectCredentials(admin.ModelAdmin):
    list_display = ('_id', 'first_name', 'last_name','Age','Gender','Education','Email','Contact','handle','isvendor')


class connectTeacher(admin.ModelAdmin):
    list_display = ('_id','Skill_set')

# Register your models here.

admin.site.register(Credentials, connectCredentials)
admin.site.register(Teacher, connectTeacher)