from django.shortcuts import render
from django.http import HttpResponse

def index(request): 
    context = { 'days': [1, 2, 3], } 
    return render(request, 'days.html', context)
