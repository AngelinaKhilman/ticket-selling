import decimal
import uuid

from decimal import Decimal

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Bus, Book, PassportData
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal


number_of_seats = 0
child = 0
adult = 0
senior = 0
isic = 0

def home(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/home.html')
    else:
        return render(request, 'myapp/signin.html')

def contacts(request):
    return render(request, 'myapp/contacts.html')

def aboutus(request):
    return render(request, 'myapp/aboutus.html')

def info(request):
    return render(request, 'myapp/info.html')

def gallery(request):
    return render(request, 'myapp/gallery.html')

def mediacenter(request):
    return render(request, 'myapp/mediacenter.html')

def service_on_board(request):
    return render(request, 'myapp/service_on_board.html')


def show_my_bus(request):
    context = {}
    if request.method == "POST":
        uniccode_r = request.POST.get('uniccode')
        ticket = Book.objects.filter(uniccode=uniccode_r)
        if ticket:
            return render(request, 'myapp/show_my_bus.html', locals())
        else:
            context["error"] = "Sorry no bookings available"
            return render(request, 'myapp/show_my_bus.html', context)
    else:
        return render(request, 'myapp/show_my_bus.html')

def null_validation(value):
    if value != '':
        return int(value)
    else:
        return 0

@login_required(login_url='signin')
def findbus(request):
    context = {}
    if request.method == 'POST':
        global number_of_seats, adult, senior, isic, child
        radio = request.POST.get("returning", None)
        if radio in ['0']:
            source_r = request.POST.get('source')
            dest_r = request.POST.get('destination')
            date_r = request.POST.get('date')
            adult_r = request.POST.get('adult')
            adult_r = null_validation(adult_r)
            senior_r = request.POST.get('senior')
            senior_r = null_validation(senior_r)
            child_r = request.POST.get('child')
            child_r = null_validation(child_r)
            isic_r = request.POST.get('isic')
            isic_r = null_validation(isic_r)
            adult = adult_r
            senior = senior_r
            isic = isic_r
            child = child_r
            bus_list = []
            number_of_seats = adult_r + senior_r + child_r + isic_r
            bus_list1 = Bus.objects.filter(source=source_r, dest=dest_r, date=date_r, rem__gte=number_of_seats)
            if bus_list1:
                return render(request, 'myapp/list.html', locals())
            else:
                context["error"] = "Sorry no buses availiable"
                return render(request, 'myapp/home.html', context)

        if radio in ['1']:
            source_r = request.POST.get('source')
            dest_r = request.POST.get('destination')
            date_r = request.POST.get('date')
            adult_r = request.POST.get('adult')
            adult_r = null_validation(adult_r)
            senior_r = request.POST.get('senior')
            senior_r = null_validation(senior_r)
            child_r = request.POST.get('child')
            child_r = null_validation(child_r)
            isic_r = request.POST.get('isic')
            isic_r = null_validation(isic_r)
            adult = adult_r
            senior = senior_r
            isic = isic_r
            child = child_r
            date_return_r = request.POST.get('date_return')
            bus_list = []
            number_of_seats = adult_r + senior_r + child_r + isic_r
            bus_list1 = Bus.objects.filter(source=source_r, dest=dest_r, date=date_r, rem__gte=number_of_seats)
            bus_list2 = Bus.objects.filter(source=dest_r, dest=source_r, date=date_return_r, rem__gte=number_of_seats)
            if bus_list1 and bus_list2:
                return render(request, 'myapp/list.html', locals())
            else:
                context["error"] = "Sorry no buses availiable"
                return render(request, 'myapp/home.html', context)
    else:
        return render(request, 'myapp/home.html')

#@login_required(login_url='signin')
#def get_passport_data(request):
    #data_list = PassportData.objects.all()
    #return render(request, '/myapp/passportdata.html', {'data': data_list})


@login_required(login_url='signin')
def passportdata(request, new={}):
    id_r = request.user.id
    context = {}
    data_list = PassportData.objects.filter(userid=id_r)
    if data_list:
        render(request, 'myapp/passportdata.html', locals())
    else:
        render(request, 'myapp/passportdata.html', context)
    if request.method == 'POST':
        data = PassportData()
        data.name = request.POST.get("name")
        data.second_name = request.POST.get("second_name")
        data.date_of_birth = request.POST.get("date_of_birth")
        data.nationality = request.POST.get("nationality")
        data.passport_number = request.POST.get("passport_number")
        data.date_of_end = request.POST.get("date_of_end")
        data.userid = request.user.id
        #data.gender = request.POST.get("gender")
        data.save()
        userid_r = request.user.id
        data_list = PassportData.objects.filter(userid=userid_r)
        if data_list:
            return render(request, 'myapp/passportdata.html', locals())
        else:
            return render(request, 'myapp/passportdata.html', context)
    return render(request, "myapp/passportdata.html")


@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        seats_r = number_of_seats
        adult_r = adult
        senior_r = senior
        isic_r = isic
        child_r = child
        bus = Bus.objects.get(id=id_r)
        if bus:
            if bus.rem > int(seats_r):
                name_r = bus.bus_name
                cost = adult_r * bus.price + senior_r * Decimal('0.9') * bus.price + isic_r * Decimal('0.9') * bus.price + child_r * Decimal('0.8') * bus.price
                source_r = bus.source
                dest_r = bus.dest
                nos_r = Decimal(bus.nos)
                price_r = bus.price
                date_r = bus.date
                time_r = bus.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                uniccode_r = uuid.uuid1()
                rem_r = bus.rem - seats_r
                Bus.objects.filter(id=id_r).update(rem=rem_r)
                book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, bus_name=name_r,
                                           source=source_r, busid=id_r,
                                           dest=dest_r, price=cost, nos=seats_r, date=date_r, time=time_r,
                                           uniccode=uniccode_r, status='BOOKED', adult=adult_r, child=child_r, senior=senior_r, isic=isic_r)
                print('------------book id-----------', book.id)
                # book.save()

                return render(request, 'myapp/bookings.html', locals())
            else:
                context["error"] = "Sorry select fewer number of seats"
                return render(request, 'myapp/findbus.html', context)

    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        #seats_r = int(request.POST.get('no_seats'))

        try:
            book = Book.objects.get(id=id_r)
            bus = Bus.objects.get(id=book.busid)
            rem_r = bus.rem + book.nos
            Bus.objects.filter(id=book.busid).update(rem=rem_r)
            #nos_r = book.nos - seats_r
            Book.objects.filter(id=id_r).update(status='CANCELLED')
            Book.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that bus"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no buses booked"
        return render(request, 'myapp/findbus.html', context)




def signup(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r, )
        if user:
            login(request, user)
            return render(request, 'myapp/thank.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signup.html', context)
    else:
        return render(request, 'myapp/signup.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            # username = request.session['username']
            context["user"] = name_r
            context["id"] = request.user.id
            return render(request, 'myapp/home.html', context)
            # return HttpResponseRedirect('success')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)
