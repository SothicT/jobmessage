from django.contrib import admin
from .import models
# Register your models here.

class Jobmessageadmin(admin.ModelAdmin):    # 用于定制admin
    list_display = ("id", "GSname", "ZWname", "ZWadd")
    ordering = ("id",)

class useradmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")
    ordering = ("id",)

admin.site.register(models.JobmessageBy51, Jobmessageadmin)
admin.site.register(models.JobmessageByzl, Jobmessageadmin)
admin.site.register(models.user, useradmin)