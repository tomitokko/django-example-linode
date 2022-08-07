import email
from django.db import models

# Create your models here.
class Order(models.Model):
    project_name = models.CharField(max_length=1000)
    discord_link = models.CharField(max_length=1000)
    amount_of_invites = models.IntegerField()
    verification_message = models.CharField(max_length=1000)
    current_user = models.CharField(max_length=1000)
    amount_done = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)

class Alert(models.Model):
    above_or_below = models.CharField(max_length=1000)
    price = models.FloatField()
    email = models.CharField(max_length=1000)
    current_user = models.CharField(max_length=1000)
    project_name = models.CharField(max_length=1000)
    project_image = models.CharField(max_length=1000)

class ProjectList(models.Model):
    name_of_project = models.CharField(max_length=1000)