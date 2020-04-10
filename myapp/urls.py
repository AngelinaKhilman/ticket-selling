from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('findbus', views.findbus, name="findbus"),
    path('passportdata', views.passportdata, name="passportdata"),
    path('show_my_bus', views.show_my_bus, name='show_my_bus'),
    path('contacts', views.contacts, name='contacts'),
    path('aboutas', views.aboutas, name='aboutas'),
    path('info', views.info, name='info'),
    #path('seepassportdata', views.see_passport_data, 'seepassportdata'),
    path('bookings', views.bookings, name="bookings"),
    path('cancellings', views.cancellings, name="cancellings"),
    path('seebookings', views.seebookings, name="seebookings"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('success', views.success, name="success"),
    path('signout', views.signout, name="signout"),

]
