from django.contrib import admin

from django.contrib import admin
from .models import React

class connectAdmin(admin.ModelAdmin):
    list_display = ('_id', 'first_name', 'last_name','Age','Gender','Email','Contact','handle','isvendor')

# Register your models here.

admin.site.register(React, connectAdmin)