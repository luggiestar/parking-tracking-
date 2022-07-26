from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
User = get_user_model()

from parking.forms import StaffRegistrationForm


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
            messages.error(request, 'Invalid username or password')
            return redirect('parking:login')
            return HttpResponse("error")

    context = {
        'title': title

    }

    return render(request, template, context)


def logout_view(request):
    logout(request)
    return redirect("parking:login")





def staff_entry(request):
    title = "Staff List"
    template = 'parking/staff_entry.html'
    get_staff = User.objects.filter(is_staff=True)
    form = StaffRegistrationForm()

    if request.method == "POST":
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            get_username = f"{form.cleaned_data['first_name']}.{form.cleaned_data['last_name']}"
            get_pas = form.cleaned_data['last_name']
            make_password_upper_case = get_pas.upper()
            save_form.username = get_username
            save_form.is_staff = True
            save_form.set_password(make_password_upper_case)
            save_form.save()
            messages.success(request, f'{get_pas} created successfully!')

            return redirect('parking:staff_list')

    context = {
        'title': title,
        'form': form,
        'staff': get_staff
    }
    return render(request, template, context)


def update_staff(request, object_pk):
    try:
        instance = User.objects.get(id=object_pk)
    except User.DoesNotExist:
        instance = None
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('parking:staff_list')
    else:
        form = StaffRegistrationForm(instance=instance)
    context_dict = {'form': form, 'instance': instance}
    return render(request, 'parking/update_user.html', context_dict)