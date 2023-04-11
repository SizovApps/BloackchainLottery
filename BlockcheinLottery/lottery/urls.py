from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', LotteryHome.as_view(), name='home'),
    path('my_lotteries/', MyLotteries.as_view(), name='my_lotteries'),
    path('set_address/<int:pk>/', UpdateLottery.as_view(), name="set_address"),
    path('about/', about, name='about'),
    path('start_lottery/<int:pk>/', start_lottery, name='start_lottery'),
    path('enter_lottery/<int:pk>/', enter_lottery, name='enter_lottery'),
    path('end_lottery/<int:pk>/', end_lottery, name="end_lottery"),
    path('saveContractAddress', save_contract_address, name="save_contract_address"),
    path('createLottery/', create_lottery, name='create_lottery'),
    path('lottery/<int:pk>/', LotteryView.as_view(), name='show_lottery'),
    path('moralis_auth/', moralis_auth, name='moralis_auth'),
    path('request_message/', request_message, name='request_message'),
    path('my_profile/', my_profile, name='my_profile'),
    path('verify_message/', verify_message, name='verify_message'),
    path('sign_contract/<str:title>/', sing_contract, name='sing_contract')
]
