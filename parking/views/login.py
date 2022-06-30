from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    title = "Login Page"
    template = "login.html"

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                if request.user.is_superuser or request.user.is_staff:
                    return redirect("admin:index")
                    # return HttpResponse("Success")

        else:
            # messages.error(request, f"Invalid username or password. please make sure you enter valid credentials")
            messages.success(request, 'Invalid username or password')
            # return redirect('parking:login')
            return HttpResponse("error")

    context = {
        'title': title

    }

    return render(request, template, context)


def logout_view(request):
    logout(request)
    return redirect("parking:login")
