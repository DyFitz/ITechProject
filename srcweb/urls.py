from django.urls import path
from srcweb import views

app_name = 'srcweb'
urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('eventdetails_student/', views.eventdetails_student, name='eventdetails_student'),
    path('eventdetails_staff/', views.eventdetails_staff, name='eventdetails_staff'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('dancingsociety/', views.dancingsociety, name='dancingsociety'),

]