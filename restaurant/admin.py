from django.contrib import admin

# Register your models here.
from restaurant import models

admin.site.register(models.Restaurant)
admin.site.register(models.MenuCategory)
admin.site.register(models.MenuSubCategory)
admin.site.register(models.MenuItem)
