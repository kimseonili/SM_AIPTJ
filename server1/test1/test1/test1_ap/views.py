from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def index(request):
    return render(request,'index.html')

def video(request):
    return render(request,'video.html')

def result(request):
    return render(request,'result.html')

def upload(request):
    return render(request,'result.html')

def signup(request):
    context = {}
    
    if request.method == 'POST':
        if (request.POST['username'] and
            request.POST['password'] and
            request.POST['password'] == request.POST['password_check']):

            new_user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
            )

            auth.login(request, new_user)
            return redirect('index')
        
        else:
            context['error'] = '아이디와 비밀번호를 다시 확인해주세요.'
    
    return render(request, 'signup.html', context)

def login(request):
    context = {}

    if request.method == 'POST':
        if request.POST['username'] and request.POST['password']:

            user =auth.authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password']
            )

            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                context['error'] = '아이디와 비밀번호를 다시 확인해주세요.'

        else:
            context['error'] = '아이디와 비밀번호를 모두 입력해주세요.'

    return render(request, 'login.html',context)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)

    return redirect('index')