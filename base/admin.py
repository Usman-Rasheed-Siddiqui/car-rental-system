from django.contrib import admin
from .models import Car, User_info, History

# Register your models here.
admin.site.register(Car)
admin.site.register(User_info)
admin.site.register(History)