from django.contrib import admin
from .models import Order, ProjectList, Alert

# Register your models here.
admin.site.register(Order)
admin.site.register(ProjectList)
admin.site.register(Alert)