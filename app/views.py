from django.shortcuts import render
from azbankgateways.exceptions import AZBankGatewaysException
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from django.urls import reverse
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
from . forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt


def home(request):
    context = {

    }
    return render(request, 'app/home.html', context)


def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not Exised")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is Wrong")

    context = {'page': page}
    return render(request, 'app/login_register.html', context)


def logoutuser(request):
    logout(request)
    return redirect('/')


@csrf_exempt
def registerpage(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'An error required during registeration')
    return render(request, 'app/login_register.html', {'form': form})


def go_to_gateway_view(request):
    amount = 100000
    user_mobile_number = '+989373056539'

    factory = bankfactories.BankFactory()
    try:
        # or factory.create(bank_models.BankType.BMI) or set identifier
        bank = factory.auto_create()
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('home'))
        bank.set_mobile_number(user_mobile_number)  # اختیاری

        bank_record = bank.ready()
        print(bank_record)
        # هدایت کاربر به درگاه بانک
        context = bank.get_gateway()
        return render(request, 'app/redirect_to_bank.html', context=context)
    except AZBankGatewaysException as e:
        logging.critical(e)
        return render(request, 'app/redirect_to_bank.html')
