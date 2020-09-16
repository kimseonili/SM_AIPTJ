from django.shortcuts import render
from django.shortcuts import redirect
import profile
# Create your views here.
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

def runAlphapose(request) :
    os.system('inference.sh')
    return redirect('/')

def index(request):
    return render(request,'index.html')

def video(request):
    return render(request,'video.html')

def result(request):
    data = request.FILES.get('file')
    name = data.name.split('.')
    path = default_storage.save('./somename.' + name[-1], ContentFile(data.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    return render(request,'result.html')

def upload(request):
    
    return render(request,'result.html')