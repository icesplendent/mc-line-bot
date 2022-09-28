from django.contrib import admin

# Register your models here.
from MylinebotApp.models import *

class User_Info_Admin(admin.ModelAdmin):
    list_display = ('uid','name','pic_url','mtext','mdt','points','STM','Yahoo','ASML','NXP','Chunghwa','Kronos','Cathay','CTBC','Line','tsmc','a104','Pixart')
admin.site.register(User_Info,User_Info_Admin)