from django.urls import path
from srcweb import views

app_name = 'srcweb'
urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('eventdetails/', views.eventdetails, name='eventdetails'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('dancingsociety/', views.dancingsociety, name='dancingsociety'),

]