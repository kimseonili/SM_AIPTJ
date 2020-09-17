from django.shortcuts import render
from django.shortcuts import redirect
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import cv2 
import sys

# def runAlphapose(request) :
#     os.system('inference.sh')
#     return render(request, 'result.html')

def index(request):
    return render(request,'index.html')

def video(request):
    return render(request,'video.html')

def result(request):
    data = request.FILES.get('file')
    name = data.name.split('.')
    path = default_storage.save('./action.' + name[-1], ContentFile(data.read()))

    
    cap = cv2.VideoCapture(settings.MEDIA_ROOT + "/action." + name[-1])
    frames = 0
    count = 0
    interval = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / 100
    length = 0
    while(cap.isOpened()):
            frames += 1
            ret, frame = cap.read()
            if frame is None:
                    break
            if length <= frames :
                    length += interval
                    cv2.imwrite(settings.MEDIA_ROOT + "./img/" + str(count).zfill(3) + ".jpg", frame)
                    count += 1
    cap.release()

    # os.system('inference.sh')

    os.remove(settings.MEDIA_ROOT + "/action." + name[-1])
    from AlphaPose.scripts import demo_inference
    return render(request,'result.html')

def upload(request):
    
    return render(request,'result.html')