from django.shortcuts import render, redirect
from .models import Post
from django.utils import timezone
import os
import sys
# Create your views here.
def runAlphapose(request) :
    os.system('inference.sh')
    return redirect('/')

def index(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request,'posts/index.html',context)

def detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {'post':post}
    return render(request, 'posts/detail.html', context)

def new(request):
    return render(request, 'posts/new.html')

def create(request):
    author = request.POST['author']
    body = request.POST['body']
    post = Post(author=author, body=body, created_at=timezone.now())
    post.save()

    return redirect('posts:detail', post_id=post.id)

def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    context = { 'post':post }
    return render(request, 'posts/edit.html', context)

def update(request, post_id):
    post = Post.objects.get(id=post_id)
    post.author = request.POST['author']
    post.body = request.POST['body']
    post.save()

    return redirect('posts:detail', post_id=post.id)

def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()

    return redirect('posts:index')