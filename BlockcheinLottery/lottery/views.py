from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from .forms import AddLotteryForm
from .models import Lottery
from django.views.generic import ListView, DetailView, UpdateView
from .services.create_lottery_service import CreateLotteryService
from .services.create_smart_contract_service import get_lottery_info, create_smart_contract, start_lottery_transaction, enter_lottery_transaction, end_lottery_transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import json
from web3 import Web3
import requests
menu = [
        {'title': "Лоттереи", 'url_name': 'home'},
        {'title': "Создать лотерею", 'url_name': 'create_lottery'},
        {'title': "Мои лотереи", 'url_name': 'my_lotteries'},
        {'title': "Войти в аккаунт", 'url_name': 'moralis_auth'}
        ]


class LotteryHome(ListView):
    model = Lottery
    template_name = 'lottery/index.html'
    context_object_name = 'lotteries'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # lottery_state = get_lottery_state(Lottery.objects.get(title="Новая лоттерея").address)

        context['lottery_state'] = 1
        context['menu'] = menu
        return context


class MyLotteries(ListView):
    model = Lottery
    template_name = 'lottery/index.html'
    context_object_name = 'lotteries'

    def get_queryset(self):
        return Lottery.objects.filter(creator_address=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # lottery_state = get_lottery_state(Lottery.objects.get(title="Новая лоттерея").address)

        context['lottery_state'] = 1
        context['menu'] = menu
        return context


class LotteryView(DetailView):
    model = Lottery
    template_name = 'lottery/lotteryDetail.html'
    context_object_name = 'lot'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        # lottery_state = get_lottery_state(Lottery.objects.get(title="Новая лоттерея").address)
        context['menu'] = menu
        lottery_state, recent_winner, players_size, is_participating = get_lottery_info(context['lot'].address, self.request.user)
        context['lottery_state'] = lottery_state
        context['recent_winner'] = recent_winner
        context['players_size'] = players_size
        context['is_participating'] = is_participating
        return context


class UpdateLottery(UpdateView):
    model = Lottery
    fields = ["address"]
    template_name = "lottery/set_address.html"

    def get_success_url(self):
        return reverse("home")

def index(request):
    return render(request, 'lottery/index.html', {'title': 'Главная', 'menu': menu})


def about(request, lotId):
    return render(request, 'lottery/sign_transaction.html', {'title': 'О Сайте'})


def save_contract_address(request):
    print(request)
    return redirect("home")


def create_lottery(request):
    if request.method == 'POST':
        form = AddLotteryForm(request.POST, request.FILES)
        if form.is_valid():
            #print(form.cleaned_data)
            try:
                print("Enter")
                create_lottery_service = CreateLotteryService()
                print(form.cleaned_data)
                current_user = request.user
                print(current_user)
                form.cleaned_data["creator_address"] = current_user

                lot = create_lottery_service.create_lottery_object(form.cleaned_data)
                print(lot.title)

                return redirect(reverse('sing_contract', kwargs={'title': lot.title}))
            except Exception as e:
                form.add_error(None, e)
    else:
        form = AddLotteryForm()
    return render(request, 'lottery/create_lottery.html', {'form': form, 'title': 'Создание лотереи', 'menu': menu})


def sing_contract(request, title):
    if request.method == 'POST':
        print("sing_contract")
        print(request)
    else:
        lottery = Lottery.objects.filter(title=title)[0]
        transaction_data = create_smart_contract(lottery)
        return render(request, 'lottery/sign_transaction.html', {'title': 'Создание смарт-контракта', 'code': 1, "transaction_data": transaction_data, "to": ""})


def start_lottery(request, pk):
    lottery = Lottery.objects.get(pk=pk)
    print(lottery)
    transaction_data = start_lottery_transaction(lottery)
    return render(request, 'lottery/sign_transaction.html', {'title': 'Запуск лотереи', 'code': 2, "transaction_data": transaction_data, "to": lottery.address})


def enter_lottery(request, pk):
    print("enter_lottery!")
    lottery = Lottery.objects.get(pk=pk)
    transaction_data = enter_lottery_transaction(lottery)
    print("Exit!")
    print(transaction_data)
    return render(request, 'lottery/sign_transaction.html',
                  {'title': 'Купить билет', 'code': 3, "transaction_data": transaction_data, "to": lottery.address,
                   "value": lottery.gwei_fee * (10 ** 9)})


def end_lottery(request, pk):
    print("Winner")
    lottery = Lottery.objects.get(pk=pk)
    end_lottery_transaction(lottery)
    return redirect("home")


API_KEY = 'DYEG2TcEdh2jxVFOzsTezn1m6APIVEMsjS1XlUVxSHnXqqIDLeUme7esL68d9Ua3'
def moralis_auth(request):
    return render(request, 'lottery/login.html', {'title': "Вход", 'menu': menu})
def my_profile(request):
    return render(request, 'lottery/profile.html', {})
def request_message(request):
    data = json.loads(request.body)
    print("ENTER!!!!!")
    print(data)
    REQUEST_URL = 'https://authapi.moralis.io/challenge/request/evm'
    request_object = {
      "domain": "localhost",
      "chainId": data['chain'],
      "address": data['address'],
      "statement": "Please confirm",
      "uri": "http://127.0.0.1:8000/",
      "expirationTime": "2024-01-01T00:00:00.000Z",
      "notBefore": "2020-01-01T00:00:00.000Z",
      "timeout": 15
    }
    x = requests.post(
        REQUEST_URL,
        json=request_object,
        headers={'X-API-KEY': API_KEY})
    return JsonResponse(json.loads(x.text))
def verify_message(request):
    print("VERIFY!!!")
    data = json.loads(request.body)
    print(data)
    REQUEST_URL = 'https://authapi.moralis.io/challenge/verify/evm'
    x = requests.post(
        REQUEST_URL,
        json=data,
        headers={'X-API-KEY': API_KEY})
    print(json.loads(x.text))
    print(x.status_code)
    if x.status_code == 201:
        # user can authenticate
        eth_address=json.loads(x.text).get('address')
        print("eth address", eth_address)
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            user = User(username=eth_address)
            user.is_staff = False
            user.is_superuser = False
            user.save()
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['auth_info'] = data
                request.session['verified_data'] = json.loads(x.text)
                return JsonResponse({'user': user.username})
            else:
                return JsonResponse({'error': 'account disabled'})
    else:
        return JsonResponse(json.loads(x.text))