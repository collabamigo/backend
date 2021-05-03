from django.contrib import admin

from django.contrib import admin
from .models import React

class connectCredentials(admin.ModelAdmin):
    list_display = ('_id', 'first_name', 'last_name','Age','Gender','Education','Email','Contact','handle','isvendor')


class connectTeacher(admin.ModelAdmin):
    list_display = ('_id','Skill_set')
    
# Register your models here.

admin.site.register(React, connectAdmin)