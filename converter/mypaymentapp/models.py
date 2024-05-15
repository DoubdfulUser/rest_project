from typing import Iterable

from decimal import Decimal

from payments import PurchasedItem
from payments.models import BasePayment
from django.db import models


class Payment(BasePayment):

    buy_currency = models.CharField(max_length=10)
    access_token = models.CharField(max_length=255, null=True, blank=True)


    def get_failure_url(self) -> str:
        # Return a URL where users are redirected after
        # they fail to complete a payment:
        return f"http://localhost:8000/payments/{self.pk}/failure"

    def get_success_url(self) -> str:
        # Return a URL where users are redirected after
        # they successfully complete a payment:
        return f"http://localhost:8000/payments/{self.pk}/success"

    def get_purchased_items(self) -> Iterable[PurchasedItem]:
        # Return items that will be included in this payment.
        yield PurchasedItem(
            name='The Hound of the Baskervilles',
            sku='BSKV',
            quantity=9,
            price=Decimal(10),
            currency='USD',
        )
