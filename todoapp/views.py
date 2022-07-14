from email import message
import email
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, response
from .models import Items, User
from django.contrib import messages

# Create your views here.


def login(request):
    if(request.method == 'POST'):
        email = request.POST['email']
        password = request.POST['password']
        if(email != "" and password != ""):
            if User.objects.filter(email=email).first():
                users = User.objects.filter(email=email)
                if users.first().password == password:
                    userdata = {'name': users.first().username, 'email': users.first(
                    ).email, 'password': users.first().password}
                    request.session['user'] = userdata
                    return HttpResponseRedirect("/home/")
                else:
                    print("Wrong password")
                    messages.error(request, "wrong password")
                    return render(request, 'login.html')
            else:
                print("email address nit exists")
                messages.error(request, "Email does not exists")
                return render(request, 'login.html')

        else:
            messages.error(request, "All data must be provided")
            return render(request, 'login.html')
    return render(request, 'login.html')


def register(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if(username != "" and email != "" and password != ""):
            if User.objects.filter(email=email).first():
                messages.error(request, "Email already exists")
                return render(request, 'register.html')
            else:
                form = User(username=username, email=email, password=password)
                user = form.save()
                return HttpResponseRedirect("/login/")
        else:
            messages.error(request, "All data must be provided")
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')


def home(request):

    if request.session.get('user') is None:
        return HttpResponseRedirect("/login/")
    else:
        itemdata = Items.objects.filter(
            email=request.session.get('user')['email'])
        data = {"user": request.session.get(
            'user'), "items": itemdata, "total": len(itemdata)}
        return render(request, 'home.html', {'data': data})


def logout(request):
    del request.session['user']
    return HttpResponseRedirect("/login/")


def additem(request):
    if request.method == 'POST':
        item = request.POST['item']
        if item == "":
            return HttpResponseRedirect('/home/')
        else:
            email = request.session.get('user')['email']
            item = Items(email=email, item=item)
            item.save()
            return HttpResponseRedirect('/home/')
    print(request.session.get('user'))
    return render(request, "add.html")


def deleteitem(request, item, email):
    print(item)
    print(email)
    itemdata = Items.objects.filter(email=email, item=item).delete()
    return HttpResponseRedirect('/home/')


def clearall(request):
    Items.objects.filter(email=request.session.get('user')['email']).delete()
    return HttpResponseRedirect('/home/')
