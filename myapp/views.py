import datetime
import uuid
from io import BytesIO
from random import randint

from django.core import mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from reportlab.graphics import barcode
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import barcode


from .models import Bus, Book, PassportData, Passenger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from barcode.writer import ImageWriter
from django.core.mail import send_mail
import smtplib
from email.mime.text import MIMEText

number_of_seats = 0
child = 0
adult = 0
senior = 0
isic = 0
round_or_one_flag = 0
base_list = []


def home(request):
    # if request.user.is_authenticated:
    return render(request, 'myapp/home.html')


def contacts(request):
    return render(request, 'myapp/contacts.html')


def home_minsk_moscow(request):
    return render(request, 'myapp/home_minsk_moscow.html')


def home_minsk_warsaw(request):
    return render(request, 'myapp/home_minsk_warsaw.html')


def home_minsk_saint_petersburg(request):
    return render(request, 'myapp/home_minsk_saint_petersburg.html')


def home_minsk_vilnius(request):
    return render(request, 'myapp/home_minsk_vilnius.html')


def home_minsk_kiev(request):
    return render(request, 'myapp/home_minsk_kiev.html')


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
        ticket_tmp = Book.objects.filter(uniccode=uniccode_r)
        time_end = []
        for i in ticket_tmp:
            time_end.append(datetime.datetime(year=i.bus.date.year, month=i.bus.date.month, day=i.bus.date.day,
                                              hour=i.bus.time.hour, minute=i.bus.time.minute)
                            + datetime.timedelta(minutes=i.bus.time_travel.minute + int(i.bus.time_travel.hour) * 60))
            print(time_end)
        print(ticket_tmp[0].passenger_set.all())
        ticket = dict(pairs=zip(ticket_tmp, time_end))

        if ticket_tmp:
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

def dijkstra_price(bus_list_from=[], source_r=0, dest_r=0, date_r=datetime.datetime(2020, 7, 1), number_of_seats=0):
    qwery = []
    cost = 0
    list_of_buses = Bus.objects.all()
    set_of_cities = set()
    for i in range(len(list_of_buses)):
        if list_of_buses[i].source == source_r:
            s = int(list_of_buses[i].source_code)
        if list_of_buses[i].dest == dest_r:
            f = int(list_of_buses[i].dest_code)
        set_of_cities.add((int(list_of_buses[i].source_code), list_of_buses[i].source))
        set_of_cities.add((int(list_of_buses[i].dest_code), list_of_buses[i].dest))
    n = 200

    list_of_name_source = []
    for i in range(len(list_of_buses)):
        list_of_name_source.append(
            (int(list_of_buses[i].source_code), int(list_of_buses[i].dest_code), int(list_of_buses[i].rem),
             int(list_of_buses[i].price),
             datetime.datetime(int(list_of_buses[i].date.year), int(list_of_buses[i].date.month),
                               int(list_of_buses[i].date.day), int(list_of_buses[i].time.hour),
                               int(list_of_buses[i].time.minute)),
             int(int(list_of_buses[i].time_travel.hour) * 60 + int(list_of_buses[i].time_travel.minute)),
             int(list_of_buses[i].id), int(list_of_buses[i].rem)))

    graph = []
    for i in range(n):
        graph.append([])

    for i in range(len(list_of_name_source)):
        date_end = list_of_name_source[i][4] + datetime.timedelta(minutes=list_of_name_source[i][5])
        graph[list_of_name_source[i][0]].append((list_of_name_source[i][1], list_of_name_source[i][5],
                                                 list_of_name_source[i][4], date_end, list_of_name_source[i][6],
                                                 list_of_name_source[i][7], list_of_name_source[i][3]))

    visited = []
    distances = []
    p = []
    price = []

    for i in range(n):
        distances.append(datetime.datetime(5000, 2, 7, 10, 10))
        price.append(10 ** 9)
        visited.append(0)
        p.append(-1)
        qwery.append(-1)

    date_split = date_r.split('-')
    distances[s] = datetime.datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
    price[s] = 0

    for t in range(n):

        qwe = 10 ** 9
        k = -1

        for i in range(n):
            if price[i] < qwe and visited[i] < 1:
                qwe = price[i]
                k = i

        if price[k] == 10 ** 9:
            break

        visited[k] = 1

        for j in range(len(graph[k])):
            to = graph[k][j][0]
            length = graph[k][j][1]
            if graph[k][j][2] >= distances[k]:
                qqq = distances[k] + (graph[k][j][2] - distances[k])
                if price[k] + graph[k][j][6] < price[to] and graph[k][j][5] >= number_of_seats:
                    distances[to] = datetime.timedelta(minutes=length) + qqq
                    price[to] = price[k] + graph[k][j][6]
                    p[to] = k
                    qwery[to] = graph[k][j][4]

    predki = []
    while f != -1:
        predki.append(f)
        f = p[f]

    predki.reverse()
    print(predki)
    for i in range(1, len(predki)):
        bus_list_from.append(Bus.objects.get(id=qwery[predki[i]]))
        cost += Bus.objects.get(id=qwery[predki[i]]).price
    return cost * number_of_seats

def dijkstra(bus_list_from=[], source_r=0, dest_r=0, date_r=datetime.datetime(2020, 7, 1), number_of_seats=0):
    qwery = []
    cost = 0
    list_of_buses = Bus.objects.all()
    set_of_cities = set()
    for i in range(len(list_of_buses)):
        if list_of_buses[i].source == source_r:
            s = int(list_of_buses[i].source_code)
        if list_of_buses[i].dest == dest_r:
            f = int(list_of_buses[i].dest_code)
        set_of_cities.add((int(list_of_buses[i].source_code), list_of_buses[i].source))
        set_of_cities.add((int(list_of_buses[i].dest_code), list_of_buses[i].dest))
    n = 200

    list_of_name_source = []
    for i in range(len(list_of_buses)):
        list_of_name_source.append(
            (int(list_of_buses[i].source_code), int(list_of_buses[i].dest_code), int(list_of_buses[i].rem),
             int(list_of_buses[i].price),
             datetime.datetime(int(list_of_buses[i].date.year), int(list_of_buses[i].date.month),
                               int(list_of_buses[i].date.day), int(list_of_buses[i].time.hour),
                               int(list_of_buses[i].time.minute)),
             int(int(list_of_buses[i].time_travel.hour) * 60 + int(list_of_buses[i].time_travel.minute)),
             int(list_of_buses[i].id), int(list_of_buses[i].rem)))

    graph = []
    for i in range(n):
        graph.append([])

    for i in range(len(list_of_name_source)):
        date_end = list_of_name_source[i][4] + datetime.timedelta(minutes=list_of_name_source[i][5])
        graph[list_of_name_source[i][0]].append((list_of_name_source[i][1], list_of_name_source[i][5],
                                                 list_of_name_source[i][4], date_end, list_of_name_source[i][6],
                                                 list_of_name_source[i][7]))

    visited = []
    distances = []
    p = []

    for i in range(n):
        distances.append(datetime.datetime(5000, 2, 7, 10, 10))

    for i in range(n):
        visited.append(0)
        p.append(-1)
        qwery.append(-1)
    date_split = date_r.split('-')
    distances[s] = datetime.datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))

    for t in range(n):

        qwe = datetime.datetime(5000, 2, 7, 10, 10)
        k = -1

        for i in range(n):
            if distances[i] < qwe and visited[i] < 1:
                qwe = distances[i]
                k = i

        if distances[k] == datetime.datetime(5000, 2, 7, 10, 10):
            break

        visited[k] = 1

        for j in range(len(graph[k])):
            to = graph[k][j][0]
            length = graph[k][j][1]
            if graph[k][j][2] >= distances[k]:
                qqq = distances[k] + (graph[k][j][2] - distances[k])
                if datetime.timedelta(minutes=length) + qqq < distances[to] and graph[k][j][5] >= number_of_seats:
                    distances[to] = datetime.timedelta(minutes=length) + qqq
                    p[to] = k
                    qwery[to] = graph[k][j][4]

    predki = []
    while f != -1:
        predki.append(f)
        f = p[f]
    predki.reverse()
    for i in range(1, len(predki)):
        bus_list_from.append(Bus.objects.get(id=qwery[predki[i]]))
        cost += Bus.objects.get(id=qwery[predki[i]]).price
    return cost * number_of_seats

def fixed_length_path(pr=[], c1=[], pr2 = [], d2 = []):
    n = 10
    a = []
    b = []
    f4 = []
    list_of_buses = Bus.objects.all()
    for i in range(n):
        qwe = []
        for j in range(n):
            qwe.append(10 ** 9)
        a.append(qwe)
    for i in range(n):
        qwe = []
        for j in range(n):
            qwe.append(10 ** 9)
        b.append(qwe)
    for i in range(n):
        qwe = []
        for j in range(n):
            qwe.append(10 ** 9)
        c1.append(qwe)

    for i in range(n):
        qwe = []
        for j in range(n):
            qwe.append(10 ** 9)
        d2.append(qwe)
    for i in range(len(list_of_buses)):
        #print('list_of_buses[i].price')
        #print(int(list_of_buses[i].price))
        #print(a[int(list_of_buses[i].source_code)][int(list_of_buses[i].dest_code)])
        #if int(list_of_buses[i].price) < a[int(list_of_buses[i].source_code)][int(list_of_buses[i].dest_code)]:
        a[int(list_of_buses[i].source_code)][int(list_of_buses[i].dest_code)] = int(list_of_buses[i].price)
    for i in range(len(list_of_buses)):
        #if int(list_of_buses[i].price) < a[int(list_of_buses[i].source_code)][int(list_of_buses[i].dest_code)]:
        b[int(list_of_buses[i].source_code)][int(list_of_buses[i].dest_code)] = int(list_of_buses[i].price)

    for i in range(n):
        rty = []
        for j in range(n):
            rty.append([i])
        pr.append(rty)

    for i in range(n):
        for j in range(n):
            for p in range(n):
                if b[i][p] + a[p][j] < c1[i][j]:
                    c1[i][j] = b[i][p] + a[p][j]
                    pr[i][j].append(p)

    for i in range(n):
        rty = []
        for j in range(n):
            rty.append([i])
        pr2.append(rty)

    for i in range(n):
        for j in range(n):
            pr2[i][j] = pr[i][j][:]

    for i in range(n):
        for j in range(n):
            pr[i][j].append(j)


    for i in range(n):
        for j in range(n):
            for p in range(n):
                if c1[i][p] + a[p][j] < d2[i][j]:
                    d2[i][j] = c1[i][p] + a[p][j]
                    for k in range(1, len(pr2[i][p])-1):
                        if pr[i][p][k] not in pr2[i][j]:
                            pr2[i][j].append(pr[i][p][k])
                    pr2[i][j].append(p)

    for i in range(n):
        for j in range(n):
            pr2[i][j].append(j)

    for i in range(n):
        print(pr2[i])


def findbus(request):
    context = {}
    predki_for_fix_length = []

    predki_for_fix_length_2 = []
    cost_for_fix_length_2 = []
    cost_for_fix_length = []
    fixed_length_path(predki_for_fix_length, cost_for_fix_length, predki_for_fix_length_2, cost_for_fix_length_2)
    print('predki_for_fix_lengt')
    print(predki_for_fix_length)
    buses_length_one = []
    buses_length_two = []
    for i in range(10):
        qwe = []
        for j in range(10):
            qwe.append([])
        buses_length_one.append(qwe)
    for i in range(10):
        qwe = []
        for j in range(10):
            qwe.append([])
        buses_length_two.append(qwe)
    buses_length_all = Bus.objects.all()
    for i in range(len(predki_for_fix_length)):
        for j in range(len(predki_for_fix_length)):
            if len(predki_for_fix_length[i][j]) == 3:
                for k in buses_length_all:
                    if k.source_code == str(predki_for_fix_length[i][j][0]) and k.dest_code == str(predki_for_fix_length[i][j][1]):
                        buses_length_one[predki_for_fix_length[i][j][0]][predki_for_fix_length[i][j][-1]].append(k)
                    if k.source_code == str(predki_for_fix_length[i][j][1]) and k.dest_code == str(predki_for_fix_length[i][j][2]):
                        buses_length_one[predki_for_fix_length[i][j][0]][predki_for_fix_length[i][j][-1]].append(k)
                        break



    for i in range(len(predki_for_fix_length_2)):
        for j in range(len(predki_for_fix_length_2)):
            if len(predki_for_fix_length_2[i][j]) == 4:
                for k in buses_length_all:
                    if k.source_code == str(predki_for_fix_length_2[i][j][0]) and k.dest_code == str(predki_for_fix_length_2[i][j][1]):
                        buses_length_two[predki_for_fix_length_2[i][j][0]][predki_for_fix_length_2[i][j][-1]].append(k)
                    if k.source_code == str(predki_for_fix_length_2[i][j][1]) and k.dest_code == str(predki_for_fix_length_2[i][j][2]):
                        buses_length_two[predki_for_fix_length_2[i][j][0]][predki_for_fix_length_2[i][j][-1]].append(k)
                    if k.source_code == str(predki_for_fix_length_2[i][j][2]) and k.dest_code == str(predki_for_fix_length_2[i][j][3]):
                        buses_length_two[predki_for_fix_length_2[i][j][0]][predki_for_fix_length_2[i][j][-1]].append(k)

    #for i in range(10):
        #print(predki_for_fix_length_2)

    if request.method == 'POST':
        global number_of_seats, adult, senior, isic, child, round_or_one_flag, base_list
        radio = request.POST.get("trip_type", None)
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
        number_of_seats = adult_r + senior_r + child_r + isic_r
        print(number_of_seats)
        bus_list_from = []
        bus_list_from_price = []
        bus_list_to = []
        bus_list_to_price = []
        cost_r = dijkstra(bus_list_from, source_r, dest_r, date_r, number_of_seats)
        cost_r = cost_r // number_of_seats
        cost = Decimal('0.8') * cost_r * child_r + Decimal('0.9') * cost_r * senior_r + Decimal('0.9') * cost_r * isic + cost_r * adult_r
        cost_price_r = dijkstra_price(bus_list_from_price, source_r, dest_r, date_r, number_of_seats)
        cost_price_r = cost_price_r // number_of_seats
        cost_price = Decimal('0.8') * cost_price_r * child_r + Decimal('0.9') * cost_price_r * senior_r + Decimal('0.9') * cost_price_r * isic + cost_price_r * adult_r
        array_of_date = []
        array_of_time = []
        array_of_date_one_stop = []
        array_of_time_one_stop = []
        array_of_date_two_stop = []
        array_of_time_two_stop = []
        array_of_date_price = []
        array_of_time_price = []
        array_of_date2 = []
        array_of_time2 = []
        array_of_date2_price = []
        array_of_time2_price = []
        iter = len(bus_list_from) // 2 + 1
        if radio in ['0']:
            if bus_list_from:
                for i in buses_length_all:
                    if i.source == source_r:
                        fr = int(i.source_code)
                    if i.dest == dest_r:
                        too = int(i.dest_code)
                one_stop = buses_length_one[fr][too][:]
                cost_one_stop = Decimal('1.00') * cost_for_fix_length[fr][too] * adult_r + Decimal('0.8') * cost_for_fix_length[fr][too] * child_r + Decimal('0.9') * cost_for_fix_length[fr][too] * senior_r +  Decimal('0.9') * cost_for_fix_length[fr][too] * isic_r
                two_stop = buses_length_two[fr][too][:]
                cost_two_stop = Decimal('1.00') * cost_for_fix_length_2[fr][too] * adult_r + Decimal('0.8') * cost_for_fix_length_2[fr][too] * child_r + Decimal('0.9') * cost_for_fix_length_2[fr][too] * senior_r + Decimal('0.9') * cost_for_fix_length_2[fr][too] * isic_r
                if one_stop:
                    duration_one_stop = datetime.datetime(year=int(one_stop[-1].date.year),
                                                 month=int(one_stop[-1].date.month),
                                                 day=int(one_stop[-1].date.day), hour=int(one_stop[-1].time.hour),
                                                 minute=int(one_stop[-1].time.minute)) + datetime.timedelta(
                        minutes=int(one_stop[-1].time_travel.hour) * 60 + int(
                            one_stop[-1].time_travel.minute)) - datetime.datetime(year=int(one_stop[0].date.year),
                                                                                       month=int(
                                                                                           one_stop[0].date.month),
                                                                                       day=int(one_stop[0].date.day),
                                                                                       hour=int(one_stop[0].time.hour),
                                                                                       minute=int(
                                                                                           one_stop[0].time.minute))
                    for i in range(len(one_stop)):
                        date_end = datetime.datetime(year=int(one_stop[i].date.year),
                                                     month=int(one_stop[i].date.month),
                                                     day=int(one_stop[i].date.day),
                                                     hour=int(one_stop[i].time.hour),
                                                     minute=int(one_stop[i].time.minute)) + datetime.timedelta(
                            minutes=int(one_stop[i].time_travel.hour) * 60 + int(one_stop[i].time_travel.minute))
                        array_of_date_one_stop.append(datetime.date(year=date_end.year, month=date_end.month, day=date_end.day))
                        array_of_time_one_stop.append(datetime.time(hour=date_end.hour, minute=date_end.minute))
                    combined_list_one_stop = zip(one_stop, array_of_date_one_stop, array_of_time_one_stop)

                if two_stop:

                    duration_two_stop = datetime.datetime(year=int(two_stop[-1].date.year),
                                                 month=int(two_stop[-1].date.month),
                                                 day=int(two_stop[-1].date.day), hour=int(two_stop[-1].time.hour),
                                                 minute=int(two_stop[-1].time.minute)) + datetime.timedelta(
                        minutes=int(two_stop[-1].time_travel.hour) * 60 + int(
                            two_stop[-1].time_travel.minute)) - datetime.datetime(year=int(two_stop[0].date.year),
                                                                                       month=int(
                                                                                           two_stop[0].date.month),
                                                                                       day=int(two_stop[0].date.day),
                                                                                       hour=int(two_stop[0].time.hour),
                                                                                       minute=int(
                                                                                           two_stop[0].time.minute))
                    for i in range(len(two_stop)):
                        date_end = datetime.datetime(year=int(two_stop[i].date.year),
                                                     month=int(two_stop[i].date.month),
                                                     day=int(two_stop[i].date.day),
                                                     hour=int(two_stop[i].time.hour),
                                                     minute=int(two_stop[i].time.minute)) + datetime.timedelta(
                            minutes=int(two_stop[i].time_travel.hour) * 60 + int(two_stop[i].time_travel.minute))
                        array_of_date_two_stop.append(datetime.date(year=date_end.year, month=date_end.month, day=date_end.day))
                        array_of_time_two_stop.append(datetime.time(hour=date_end.hour, minute=date_end.minute))
                    combined_list_two_stop = zip(two_stop, array_of_date_two_stop, array_of_time_two_stop)

                duration = datetime.datetime(year=int(bus_list_from[-1].date.year),
                                             month=int(bus_list_from[-1].date.month),
                                             day=int(bus_list_from[-1].date.day), hour=int(bus_list_from[-1].time.hour),
                                             minute=int(bus_list_from[-1].time.minute)) + datetime.timedelta(
                    minutes=int(bus_list_from[-1].time_travel.hour) * 60 + int(
                        bus_list_from[-1].time_travel.minute)) - datetime.datetime(year=int(bus_list_from[0].date.year),
                                                                                   month=int(
                                                                                       bus_list_from[0].date.month),
                                                                                   day=int(bus_list_from[0].date.day),
                                                                                   hour=int(bus_list_from[0].time.hour),
                                                                                   minute=int(
                                                                                       bus_list_from[0].time.minute))
                for i in range(len(bus_list_from)):
                    date_end = datetime.datetime(year=int(bus_list_from[i].date.year),
                                                 month=int(bus_list_from[i].date.month),
                                                 day=int(bus_list_from[i].date.day),
                                                 hour=int(bus_list_from[i].time.hour),
                                                 minute=int(bus_list_from[i].time.minute)) + datetime.timedelta(
                        minutes=int(bus_list_from[i].time_travel.hour) * 60 + int(bus_list_from[i].time_travel.minute))
                    array_of_date.append(datetime.date(year=date_end.year, month=date_end.month, day=date_end.day))
                    array_of_time.append(datetime.time(hour=date_end.hour, minute=date_end.minute))
                combined_list = zip(bus_list_from, array_of_date, array_of_time)
                base_list.append(bus_list_from)
                print(base_list)
                duration_price = datetime.datetime(year=int(bus_list_from_price[-1].date.year),
                                                   month=int(bus_list_from_price[-1].date.month),
                                                   day=int(bus_list_from_price[-1].date.day),
                                                   hour=int(bus_list_from_price[-1].time.hour),
                                                   minute=int(
                                                       bus_list_from_price[-1].time.minute)) + datetime.timedelta(
                    minutes=int(bus_list_from_price[-1].time_travel.hour) * 60 + int(
                        bus_list_from_price[-1].time_travel.minute)) - datetime.datetime(
                    year=int(bus_list_from_price[0].date.year),
                    month=int(
                        bus_list_from_price[0].date.month),
                    day=int(bus_list_from_price[0].date.day),
                    hour=int(bus_list_from_price[0].time.hour),
                    minute=int(
                        bus_list_from_price[0].time.minute))
                for i in range(len(bus_list_from_price)):
                    date_end = datetime.datetime(year=int(bus_list_from_price[i].date.year),
                                                 month=int(bus_list_from_price[i].date.month),
                                                 day=int(bus_list_from_price[i].date.day),
                                                 hour=int(bus_list_from_price[i].time.hour),
                                                 minute=int(bus_list_from_price[i].time.minute)) + datetime.timedelta(
                        minutes=int(bus_list_from_price[i].time_travel.hour) * 60 + int(
                            bus_list_from_price[i].time_travel.minute))
                    array_of_date_price.append(
                        datetime.date(year=date_end.year, month=date_end.month, day=date_end.day))
                    array_of_time_price.append(datetime.time(hour=date_end.hour, minute=date_end.minute))
                combined_list_price = zip(bus_list_from_price, array_of_date_price, array_of_time_price)
                base_list.append(bus_list_from_price)
                base_list.append(one_stop)
                base_list.append(two_stop)
                return render(request, 'myapp/list.html', locals())
            else:
                context["error"] = "Sorry no buses availiable"
                return render(request, 'myapp/home.html', context)

        if radio in ['1']:
            round_or_one_flag = 1
            date_return_r = request.POST.get('date_return')
            if date_return_r < date_r:
                context["error"] = "Return date earlier than arrival date"
                return render(request, 'myapp/home.html', context)
            cost2_r = dijkstra(bus_list_to, dest_r, source_r, date_return_r, number_of_seats)
            cost2_r = cost2_r / number_of_seats
            cost2 = Decimal('0.8') * cost2_r * child_r + Decimal('0.9') * cost2_r * senior_r + Decimal('0.9') * cost2_r * isic + cost2_r * adult_r + cost
            cost2_price_r = dijkstra_price(bus_list_to_price, dest_r, source_r, date_return_r,
                                         number_of_seats)
            cost2_price_r = cost2_price_r / number_of_seats
            cost2_price = Decimal('0.8') * cost2_price_r * child_r + Decimal('0.9') * cost2_price_r * senior_r + Decimal('0.9') * cost2_price_r * isic + cost2_price_r * adult_r + cost_price
            if bus_list_from and bus_list_to:
                iter2 = len(bus_list_to) // 2 + 1
                duration = datetime.datetime(year=int(bus_list_from[-1].date.year),
                                             month=int(bus_list_from[-1].date.month),
                                             day=int(bus_list_from[-1].date.day), hour=int(bus_list_from[-1].time.hour),
                                             minute=int(bus_list_from[-1].time.minute)) + datetime.timedelta(
                    minutes=int(bus_list_from[-1].time_travel.hour) * 60 + int(
                        bus_list_from[-1].time_travel.minute)) - datetime.datetime(year=int(bus_list_from[0].date.year),
                                                                                   month=int(
                                                                                       bus_list_from[0].date.month),
                                                                                   day=int(bus_list_from[0].date.day),
                                                                                   hour=int(bus_list_from[0].time.hour),
                                                                                   minute=int(
                                                                                       bus_list_from[0].time.minute))
                for i in range(len(bus_list_from)):
                    date_end = datetime.datetime(year=int(bus_list_from[i].date.year),
                                                 month=int(bus_list_from[i].date.month),
                                                 day=int(bus_list_from[i].date.day),
                                                 hour=int(bus_list_from[i].time.hour),
                                                 minute=int(bus_list_from[i].time.minute)) + datetime.timedelta(
                        minutes=int(bus_list_from[i].time_travel.hour) * 60 + int(bus_list_from[i].time_travel.minute))
                    array_of_date.append(datetime.date(year=date_end.year, month=date_end.month, day=date_end.day))
                    array_of_time.append(datetime.time(hour=date_end.hour, minute=date_end.minute))
                combined_list = zip(bus_list_from, array_of_date, array_of_time)
                base_list[:].append(bus_list_from)

                duration_price = datetime.datetime(year=int(bus_list_from_price[-1].date.year),
                                                   month=int(bus_list_from_price[-1].date.month),
                                                   day=int(bus_list_from_price[-1].date.day),
                                                   hour=int(bus_list_from_price[-1].time.hour),
                                                   minute=int(
                                                       bus_list_from_price[-1].time.minute)) + datetime.timedelta(
                    minutes=int(bus_list_from_price[-1].time_travel.hour) * 60 + int(
                        bus_list_from_price[-1].time_travel.minute)) - datetime.datetime(
                    year=int(bus_list_from_price[0].date.year),
                    month=int(
                        bus_list_from_price[0].date.month),
                    day=int(bus_list_from_price[0].date.day),
                    hour=int(bus_list_from_price[0].time.hour),
                    minute=int(
                        bus_list_from_price[0].time.minute))
                for i in range(len(bus_list_from_price)):
                    date_end = datetime.datetime(year=int(bus_list_from_price[i].date.year),
                                                 month=int(bus_list_from_price[i].date.month),
                                                 day=int(bus_list_from_price[i].date.day),
                                                 hour=int(bus_list_from_price[i].time.hour),
                                                 minute=int(bus_list_from_price[i].time.minute)) + datetime.timedelta(
                        minutes=int(bus_list_from_price[i].time_travel.hour) * 60 + int(
                            bus_list_from_price[i].time_travel.minute))
                    array_of_date_price.append(
                        datetime.date(year=date_end.year, month=date_end.month, day=date_end.day))
                    array_of_time_price.append(datetime.time(hour=date_end.hour, minute=date_end.minute))
                combined_list_price = zip(bus_list_from_price, array_of_date_price, array_of_time_price)
                base_list.append(bus_list_from_price)
                duration2 = datetime.datetime(year=int(bus_list_to[-1].date.year),
                                              month=int(bus_list_to[-1].date.month),
                                              day=int(bus_list_to[-1].date.day), hour=int(bus_list_to[-1].time.hour),
                                              minute=int(bus_list_to[-1].time.minute)) + datetime.timedelta(
                    minutes=int(bus_list_to[-1].time_travel.hour) * 60 + int(
                        bus_list_to[-1].time_travel.minute)) - datetime.datetime(year=int(bus_list_to[0].date.year),
                                                                                 month=int(
                                                                                     bus_list_to[0].date.month),
                                                                                 day=int(bus_list_to[0].date.day),
                                                                                 hour=int(bus_list_to[0].time.hour),
                                                                                 minute=int(
                                                                                     bus_list_to[0].time.minute))
                for i in range(len(bus_list_to)):
                    date_end2 = datetime.datetime(year=int(bus_list_to[i].date.year),
                                                  month=int(bus_list_to[i].date.month),
                                                  day=int(bus_list_to[i].date.day),
                                                  hour=int(bus_list_to[i].time.hour),
                                                  minute=int(bus_list_to[i].time.minute)) + datetime.timedelta(
                        minutes=int(bus_list_to[i].time_travel.hour) * 60 + int(bus_list_to[i].time_travel.minute))
                    array_of_date2.append(datetime.date(year=date_end2.year, month=date_end2.month, day=date_end2.day))
                    array_of_time2.append(datetime.time(hour=date_end2.hour, minute=date_end2.minute))
                combined_list2 = zip(bus_list_to, array_of_date2, array_of_time2)
                base_list.append(bus_list_to)
                duration2_price = datetime.datetime(year=int(bus_list_to_price[-1].date.year),
                                                    month=int(bus_list_to_price[-1].date.month),
                                                    day=int(bus_list_to_price[-1].date.day),
                                                    hour=int(bus_list_to_price[-1].time.hour),
                                                    minute=int(
                                                        bus_list_to_price[-1].time.minute)) + datetime.timedelta(
                    minutes=int(bus_list_to_price[-1].time_travel.hour) * 60 + int(
                        bus_list_to_price[-1].time_travel.minute)) - datetime.datetime(
                    year=int(bus_list_to_price[0].date.year),
                    month=int(
                        bus_list_to_price[0].date.month),
                    day=int(bus_list_to_price[0].date.day),
                    hour=int(bus_list_to_price[0].time.hour),
                    minute=int(
                        bus_list_to_price[0].time.minute))
                for i in range(len(bus_list_to_price)):
                    date_end = datetime.datetime(year=int(bus_list_to_price[i].date.year),
                                                 month=int(bus_list_to_price[i].date.month),
                                                 day=int(bus_list_to_price[i].date.day),
                                                 hour=int(bus_list_to_price[i].time.hour),
                                                 minute=int(bus_list_to_price[i].time.minute)) + datetime.timedelta(
                        minutes=int(bus_list_to_price[i].time_travel.hour) * 60 + int(
                            bus_list_to_price[i].time_travel.minute))
                    array_of_date2_price.append(
                        datetime.date(year=date_end.year, month=date_end.month, day=date_end.day))
                    array_of_time2_price.append(datetime.time(hour=date_end.hour, minute=date_end.minute))
                combined_list2_price = zip(bus_list_to_price, array_of_date2_price, array_of_time2_price)
                base_list.append(bus_list_to_price)
                return render(request, 'myapp/list.html', locals())
            else:
                context["error"] = "Sorry no buses availiable"
                return render(request, 'myapp/home.html', context)
    else:
        return render(request, 'myapp/home.html')


@login_required(login_url='signin')
def passportdata(request, new={}):
    return render(request, "myapp/passportdata.html")


@login_required(login_url='signin')
def bookings(request):
    global round_or_one_flag, number_of_seats, adult, base_list, senior, isic, child
    seats_r = number_of_seats
    list_of_books_tmp = []
    list_of_books_tmp2 = []
    if request.method == 'POST':
        id_r = request.POST.get('button')
        adult_r = adult
        senior_r = senior
        isic_r = isic
        child_r = child
        user = request.user
        print(id_r)
        # bus1 = Bus.objects.get(id=id_r)
        if round_or_one_flag == 0:
            if id_r == '2':
                list_of_books = base_list[0][:]
            if id_r == '3':
                list_of_books = base_list[1][:]
            if id_r == '4':
                list_of_books = base_list[2][:]
                print(base_list)
            if id_r == '5':
                list_of_books = base_list[3][:]
                print(base_list)
            uniccode_r = uuid.uuid1()
            for j in range(len(list_of_books)):
                i = j
                bus1 = Bus.objects.get(id=int(list_of_books[i].id))
                cost = adult_r * bus1.price + senior_r * Decimal('0.9') * bus1.price + isic_r * Decimal(
                    '0.9') * bus1.price + child_r * Decimal('0.8') * bus1.price
                rem_r = bus1.rem - number_of_seats
                Bus.objects.filter(id=int(list_of_books[i].id)).update(rem=rem_r)
                book_p = Book.objects.create(user=user, bus=bus1,
                                             price=cost,
                                             uniccode=uniccode_r, status='BOOKED', adult=adult_r, child=child_r,
                                             senior=senior_r, isic=isic_r)
                list_of_books_tmp.append(book_p)
            for i in range(seats_r):
                name_p = request.POST.get('name' + str(i + 1))
                lastname_p = request.POST.get('lastname' + str(i + 1))
                phone_p = request.POST.get('phone' + str(i + 1))
                email_p = request.POST.get('email' + str(i + 1))
                status_p = request.POST.get('status' + str(i + 1))

                for k in list_of_books_tmp:
                    passanger = Passenger(name=name_p, last_name=lastname_p, email=email_p, phone=phone_p,
                                          status=status_p, book=k)
                    k.passenger_set.add(passanger, bulk=False)

        if round_or_one_flag == 1:
            round_or_one_flag = 0
            print(id_r)
            if id_r == '0':
                list_of_books = base_list[0][:]
                list_of_books2 = base_list[2][:]
            if id_r == '1':
                list_of_books = base_list[1][:]
                list_of_books2 = base_list[3][:]
                print(base_list)
            uniccode_r = uuid.uuid1()
            for j in range(len(list_of_books)):
                i = j
                bus1 = Bus.objects.get(id=int(list_of_books[i].id))
                cost = adult_r * bus1.price + senior_r * Decimal('0.9') * bus1.price + isic_r * Decimal(
                    '0.9') * bus1.price + child_r * Decimal('0.8') * bus1.price
                rem_r = bus1.rem - number_of_seats
                Bus.objects.filter(id=int(list_of_books[i].id)).update(rem=rem_r)
                book_p = Book.objects.create(user=user, bus=bus1,
                                             price=cost,
                                             uniccode=uniccode_r, status='BOOKED', adult=adult_r, child=child_r,
                                             senior=senior_r, isic=isic_r)
                list_of_books_tmp.append(book_p)
            uniccode_r = uuid.uuid1()
            for j in range(len(list_of_books2)):
                i = j
                bus1 = Bus.objects.get(id=int(list_of_books2[i].id))
                cost = adult_r * bus1.price + senior_r * Decimal('0.9') * bus1.price + isic_r * Decimal(
                    '0.9') * bus1.price + child_r * Decimal('0.8') * bus1.price
                rem_r = bus1.rem - number_of_seats
                Bus.objects.filter(id=int(list_of_books2[i].id)).update(rem=rem_r)
                book_p = Book.objects.create(user=user, bus=bus1,
                                             price=cost,
                                             uniccode=uniccode_r, status='BOOKED', adult=adult_r, child=child_r,
                                             senior=senior_r, isic=isic_r)
                list_of_books_tmp2.append(book_p)
            for i in range(seats_r):
                name_p = request.POST.get('name' + str(i + 1))
                lastname_p = request.POST.get('lastname' + str(i + 1))
                phone_p = request.POST.get('phone' + str(i + 1))
                email_p = request.POST.get('email' + str(i + 1))
                status_p = request.POST.get('status' + str(i + 1))

                for k in list_of_books_tmp:
                    passanger = Passenger(name=name_p, last_name=lastname_p, email=email_p, phone=phone_p,
                                          status=status_p, book=k)
                    k.passenger_set.add(passanger, bulk=False)
                for k in list_of_books_tmp2:
                    passanger = Passenger(name=name_p, last_name=lastname_p, email=email_p, phone=phone_p,
                                          status=status_p, book=k)
                    k.passenger_set.add(passanger, bulk=False)

            return redirect(seebookings)
        return redirect(seebookings)
    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def data(request):
    if request.method == "POST":
        id_r = request.POST.get('button')
    print(id_r)
    global number_of_seats
    seats = number_of_seats
    list_smp = []
    for i in range(seats):
        list_smp.append(i + 1)
    print(seats)
    return render(request, 'myapp/data.html', locals())


@login_required(login_url='signin')
def delete_booking(request):
    context = {}
    if request.method == 'POST':

        id_r = request.POST.get('booking_id')
        print(id_r)
        booking = Book.objects.filter(uniccode=id_r)
        # seats_r = int(request.POST.get('no_seats'))

        try:
            for i in booking:
                i.delete()
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "can't delete"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/home.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    global number_of_seats
    seats_r = number_of_seats
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        # seats_r = int(request.POST.get('no_seats'))

        try:
            book = Book.objects.filter(uniccode=id_r)
            print(book)
            for i in book:
                bus = i.bus
                rem_r = bus.rem + seats_r
                Bus.objects.filter(id=bus.id).update(rem=rem_r)
                # nos_r = book.nos - seats_r
                Book.objects.filter(uniccode=id_r).update(status='CANCELLED')
            # Book.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that bus"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/findbus.html')


@login_required(login_url='signin')
def seebookings(request):
    context = {}
    id_r = request.user.id
    user = request.user
    book_list_tmp = Book.objects.filter(user=user)
    book_list = dict()
    for i in book_list_tmp:
        book_list[i.uniccode] = []

    for j in book_list:
        for i in book_list_tmp:
            if j == i.uniccode:
                book_list[j].append(
                    (i, datetime.datetime(year=i.bus.date.year, month=i.bus.date.month, day=i.bus.date.day,
                                          hour=i.bus.time.hour, minute=i.bus.time.minute) + datetime.timedelta(
                        hours=i.bus.time_travel.hour, minutes=i.bus.time_travel.minute)))
                print(book_list[j][0][0].bus)
    print(book_list)

    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no buses booked"
        return render(request, 'myapp/home.html', context)


def pdf(request):
    response = HttpResponse(content_type='application/pdf')
    if request.method == "POST":
        id_r = request.POST.get('doc')
        print(id_r)
        response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'
        buffer = BytesIO()
        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        book = Book.objects.filter(uniccode=id_r)
        # print(name)
        p.drawString(inch, 11 * inch, "E-ticket")
        p.line(inch, 10.8 * inch, 7 * inch, 10.8 * inch)
        p.drawString(inch, 10.5 * inch, "Passengers:")
        h = 10.5
        for i in book[0].passenger_set.all():
            p.drawString(2 * inch, h * inch, i.name + " " + i.last_name)
            h -= 0.3
        p.line(inch, h * inch, 7 * inch, h * inch)
        h -= 0.3
        p.drawString(inch, h * inch, "From:")
        p.drawString(2 * inch, h * inch, book[0].bus.source)
        h -= 0.3
        p.drawString(inch, h * inch, "To:")
        p.drawString(2 * inch, h * inch, book[len(book) - 1].bus.dest)
        h -= 0.3
        p.drawString(inch, h * inch, "Date:")
        p.drawString(2 * inch, h * inch, str(book[0].bus.date))
        h -= 0.3
        p.drawString(inch, h * inch, "Time:")
        p.drawString(2 * inch, h * inch, str(book[0].bus.time))
        h -= 0.3
        p.line(inch, h * inch, 7 * inch, h * inch)
        h -= 0.3
        p.drawString(inch, h * inch, "Route:")
        h -= 0.3
        p.drawString(inch, h * inch, "Bus number:")
        p.drawString(2.3 * inch, h * inch, "From:")
        p.drawString(3.3 * inch, h * inch, "To:")
        p.drawString(4 * inch, h * inch, "Date:")
        p.drawString(5 * inch, h * inch, "Time:")
        p.drawString(6 * inch, h * inch, "Travel time:")
        h -= 0.3
        for i in book:
            p.drawString(inch, h * inch, i.bus.bus_name)
            p.drawString(2.3 * inch, h * inch, i.bus.source)
            p.drawString(3.3 * inch, h * inch, i.bus.dest)
            p.drawString(4 * inch, h * inch, str(i.bus.date))
            p.drawString(5 * inch, h * inch, str(i.bus.time))
            p.drawString(6 * inch, h * inch, str(i.bus.time_travel))
            h -= 0.3
        p.line(inch, h * inch, 7 * inch, h * inch)
        h -= 0.3
        p.drawString(inch, h * inch, "Cost:")
        cost = 0
        for i in book:
            cost += int(i.price)
        p.drawString(2 * inch, h * inch, str(cost))
        h -= 0.3
        p.drawString(inch, h * inch, "Unique code:")
        p.drawString(2 * inch, h * inch, str(book[0].uniccode))
        h -= 3
        ean = barcode.get('ean13', '123456789102', writer=ImageWriter())
        filename = ean.save('ean13')
        p.drawImage(filename, 2 * inch, h * inch, width=320, height=171)

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        for i in book[0].passenger_set.all():
            #send_mail(p, 'This e-mail was sent with Django.',
                      #'angelinakhilman@gmail.com', [i.email], fail_silently=False)
            EmailMsg = mail.EmailMessage('E-ticket', 'Ticket for your trip', 'angelinakhilman@gmail.com', [i.email],
                                         headers={'Reply-To': 'angelinakhilman@gmail.com'})
            EmailMsg.attach(i.name+i.last_name+'.pdf', pdf, 'application/pdf')
            EmailMsg.send()

    return response


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

#def get_context_data(self, **kwargs):
    #books, created = Book.objects.get_or_create(name='1', price=2)
    #count = randint(1, 4)
    #amount = count * books.price

    #payment = Payment(order_amount=amount)
    #payment.save()

    #order = Order(books=books, payment=payment,
                      #count=count, amount=amount)
    #order.save()

    #ctx = super(OrderPage, self).get_context_data(**kwargs)
    #return ctx
