from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, "authentication/index.html")


def sign_up(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        pass_confirm = request.POST['pass_confirm']
        fname = request.POST['fname']
        lname = request.POST['lname']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try another username")
            return redirect('home')
        
        elif User.objects.filter(email=email):
            messages.error(request, "Email already reggistered!")
            
        
        elif len(username) > 20:
            messages.error(request, "Username is too long! Username must be under 15 charecters")
            
        
        elif password != pass_confirm:
            messages.error(request, "Passwords didn't match!")
        
        elif not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('home')
        

        user = User.objects.create_user(username, email, password)
        user.first_name = fname
        user.last_name = lname
        if username.startswith("Teacher"):
            user.groups.add("Teachers")
            user.is_staff = True
        else:
            user.groups.add("Students")
        user.save()

        messages.success(request, "Your Account has been Succesfully Created")
        return redirect('sign_in')

    return render(request, "authentication/sign_up.html")


def sign_in(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'authentication/index.html', {'fname':fname})
        
        else:
            messages.error(request, "BAD CREDENTIALS!")
            return redirect('home')


    return render(request, "authentication/sign_in.html")


def sign_out(request):
    logout(request)
    messages.success(request, "You have been signed out")
    return redirect('home')
