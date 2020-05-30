from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Bus, Book, PassportData, Passenger



admin.site.register(Bus)
admin.site.register(Book)
admin.site.register(PassportData)
admin.site.register(Passenger)

