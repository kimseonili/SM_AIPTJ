from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
import os

def runAlphapose(request) :
    os.system('inference.sh')
    return redirect('/')

def index(request):
    return render(request,'index.html')

def video(request):
    return render(request,'video.html')

def result(request):
    return render(request,'result.html')

def upload(request):
    return render(request,'result.html')