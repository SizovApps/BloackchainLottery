from ..models import Lottery
from .create_smart_contract_service import create_smart_contract


class CreateLotteryService:

    def create_lottery_object(self, cleaned_data):
        print("create_lottery")

        lot = Lottery.objects.create(**cleaned_data)
        print(lot.content)
        return lot


