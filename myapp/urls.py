from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('pdf', views.pdf, name="pdf"),
    path('findbus', views.findbus, name="findbus"),
    path('passportdata', views.passportdata, name="passportdata"),
    path('show_my_bus', views.show_my_bus, name='show_my_bus'),
    path('contacts', views.contacts, name='contacts'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('info', views.info, name='info'),
    path('gallery', views.gallery, name='gallery'),
    path('mediacenter', views.mediacenter, name='mediacenter'),
    path('service_on_board', views.service_on_board, name='service_on_board'),
    #path('seepassportdata', views.see_passport_data, 'seepassportdata'),
    path('data', views.data, name='data'),
    path('bookings', views.bookings, name="bookings"),
    path('cancellings', views.cancellings, name="cancellings"),
    path('delete_booking', views.delete_booking, name='delete_booking'),
    path('seebookings', views.seebookings, name="seebookings"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('success', views.success, name="success"),
    path('signout', views.signout, name="signout"),
    path('home_minsk_moscow', views.home_minsk_moscow, name='home_minsk_moscow'),
    path('home_minsk_warsaw', views.home_minsk_warsaw, name='home_minsk_warsaw'),
    path('home_minsk_saint_petersburg', views.home_minsk_saint_petersburg, name='home_minsk_saint_petersburg'),
    path('home_minsk_vilnius', views.home_minsk_vilnius, name='home_minsk_vilnius'),
    path('home_minsk_kiev', views.home_minsk_kiev, name='home_minsk_kiev'),

]
