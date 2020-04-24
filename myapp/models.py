from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email

class PassportData(models.Model):
    MALE = 'm'
    FEMALE = 'f'
    GENDER_STATUSES = ((MALE, 'Male'),
                       (FEMALE, 'Female'),)

    name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=30)
    passport_number = models.CharField(max_length = 30)
    date_of_end = models.DateField()
    #gender = models.CharField(choices=GENDER_STATUSES, default=MALE, max_length=2)
    userid = models.DecimalField(decimal_places=0, max_digits=2)

class Bus(models.Model):
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()


    def __str__(self):
        return self.bus_name





class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)

    email = models.EmailField()
    name = models.CharField(max_length=30)
    userid =models.DecimalField(decimal_places=0, max_digits=2)
    busid=models.DecimalField(decimal_places=0, max_digits=2)
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    uniccode = models.CharField(max_length=50)
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=2)
    child = models.DecimalField(decimal_places=0, max_digits=2, blank=True)
    adult = models.DecimalField(decimal_places=0, max_digits=2, blank=True)
    senior = models.DecimalField(decimal_places=0, max_digits=2, blank=True)
    isic = models.DecimalField(decimal_places=0, max_digits=2, blank=True)


    def __str__(self):
        return self.email
