from django.contrib import admin

from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(News)
admin.site.register(NewsCat)
admin.site.register(Subscription)
admin.site.register(MainForm)