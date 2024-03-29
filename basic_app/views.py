from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm
# Create your views here.

# login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
# before django 2.0 from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'basic_app/index.html')

# only logged in user can see it


@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # hashing password with set
            user.set_password(user.password)
            user.save()

            # not saving to db yet, incaseof collision,
            # see if there's pic before save
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    # no request yet
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/register.html', {'registered': registered, 'user_form': user_form, 'profile_form': profile_form})


def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not Active")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("invalid login details supplied")
    else:
        return render(request, 'basic_app/login.html', {})
