from django.urls import path
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .views import *
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Page


from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request ,'home.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, template_name='register.html', context={'error': 'Username already exists'})
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                return redirect('login')

    return render(request, template_name='register.html')



def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        user = authenticate(username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, template_name='login.html', context={'error': 'Invalid username or password'})

    return render(request, template_name='login.html')



@login_required
def user_logout(request):
    logout(request)
    return redirect('login')




def create_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('context')

        Page.objects.create(
            title=title,
            content=content,
            author=request.user
        )

    return render(request, template_name='create_page.html')


def all_pages(request):
    pages = Page.objects.all()
    if request.GET.get('q', False):
        pages = Page.objects.filter(title__icontains=request.GET.get('q'))
    context = {'pages': pages}
    return render(request, template_name='all_pages.html', context=context)


def detail_page(request, page_id):
    page = Page.objects.get(id=page_id)
    return render(request, template_name='detail_page.html', context={'page': page})



@login_required
def del_page(request, page_id):
    page = Page.objects.get(id=page_id)
    if page.author == request.user:
        page.delete()
    return redirect('all_pages')


@login_required
def edit_page(request, page_id):
    page = Page.objects.get(id=page_id)
    if page.author == request.user:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            page.title = title
            page.content = content
            page.save()
            return redirect('all_pages')
        return render(request, template_name='edit_page.html', context={'page': page})
    else:
        return redirect('all_pages')