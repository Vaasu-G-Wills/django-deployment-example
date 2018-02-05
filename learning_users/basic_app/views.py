from django.shortcuts import render, reverse
from basic_app.forms import UserForm, UserProfileInfoForm
#Login purpose
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login ,logout
from basic_app.models import UserProfileInfo
# from django.core.urlresolvers import reverse
# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return render(request, 'basic_app/special.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                logged_in_user_id = UserProfileInfo.objects.get(id=1)
                # logged_in_user_portfolio = UserProfileInfo.objects.get('portfolio_site')
                print(logged_in_user_id)
                # print(logged_in_user_portfolio)
                print()
                return HttpResponseRedirect(reverse('special'))
            else:
                return HttpResponse("Account not active")
        else:
            print('someone tried to login and failed')
            print('Usernaem {} and password {}'.format(username,password))
            return HttpResponse('<em><b>Invalid login details supplied</b></em>')
    else:
        return render(request,'basic_app/login.html',{})


def registration(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form =UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',{'user_form':user_form, 'profile_form':profile_form,'registered':registered})
