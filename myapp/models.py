import django
from django.db import models

# Create your models here.
from django.db import models

from django.contrib.auth.models import User

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
    source_code = models.CharField(max_length=4)
    dest = models.CharField(max_length=30)
    dest_code = models.CharField(max_length=4)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    time_travel = models.TimeField()

    def __str__(self):
        return self.bus_name



class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)

    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE, default="")
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, default="")
    price = models.DecimalField(decimal_places=2, max_digits=6)
    uniccode = models.CharField(max_length=50)
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=2)
    child = models.DecimalField(decimal_places=0, max_digits=2, blank=True)
    adult = models.DecimalField(decimal_places=0, max_digits=2, blank=True)
    senior = models.DecimalField(decimal_places=0, max_digits=2, blank=True)
    isic = models.DecimalField(decimal_places=0, max_digits=2, blank=True)


    def __str__(self):
        return str(self.user.id)


class Passenger(models.Model):
    ADULT = 'A'
    ISIC = 'I'
    CHILD = 'CH'
    SENIOR = 'S'
    STATUS = ((ADULT, 'Adult'), (ISIC, 'Isic'), (CHILD, 'Child'), (SENIOR, 'Senior'),)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50)
    status = models.CharField(choices=STATUS, default=ADULT, max_length=2)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default="")

#class Order(models.Model):
    #books = models.ForeignKey(Book, verbose_name='Бронирование')
    #count = models.PositiveIntegerField('Кол-во', default=1)
    #payment = models.ForeignKey('yandex_money.Payment',
                                #verbose_name='Платеж')
    #amount = models.PositiveIntegerField('Сумма заказа')

    #class Meta:
        #verbose_name = 'Заказ'
        #verbose_name_plural = 'Заказы'

