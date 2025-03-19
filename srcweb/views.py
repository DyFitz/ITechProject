from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'srcweb/home.html')

def events(request):
    return render(request, 'srcweb/events.html')

def eventdetails(request):
    return render(request, 'srcweb/eventdetails.html')

def myaccount(request):
    return render(request, 'srcweb/myaccount.html')

def dancingsociety(request):
    return render(request, 'srcweb/dancingsociety.html')
