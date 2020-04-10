from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Bus, User, Book, PassportData



admin.site.register(Bus)
admin.site.register(User)
admin.site.register(Book)
admin.site.register(PassportData)
