from django.db import models

# Create your models here.
class user(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    created_time = models.TimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return "<user:%s>" % self.username

class JobmessageByzl(models.Model):
    GSname = models.CharField(max_length=255)
    GSlink = models.CharField(max_length=255)
    ZWname = models.CharField(max_length=255)
    ZWsalary = models.CharField(max_length=255)
    ZWtype = models.CharField(max_length=255)
    ZWexp = models.CharField(max_length=255)
    ZWadd = models.CharField(max_length=255)
    ZWnature = models.CharField(max_length=255)
    ZDedu = models.CharField(max_length=255)
    ZWnum = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    ZWinfo = models.TextField()
    created_time = models.TimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return "<Jobmessage:%s>" % self.ZWname

class JobmessageBy51(models.Model):
    GSname = models.CharField(max_length=255)
    GSlink = models.CharField(max_length=255)
    ZWname = models.CharField(max_length=255)
    ZWsalary = models.CharField(max_length=255)
    ZWtype = models.CharField(max_length=255)
    ZWexp = models.CharField(max_length=255)
    ZWadd = models.CharField(max_length=255)
    ZWnature = models.CharField(max_length=255)
    ZDedu = models.CharField(max_length=255)
    ZWnum = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    ZWinfo = models.TextField()
    created_time = models.TimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return "<Jobmessage:%s>" % self.ZWname