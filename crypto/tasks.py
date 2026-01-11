from celery import shared_task
from .services import CryptoService
from .models import CryptoAddress


@shared_task
def monitor_crypto_transactions():
    addresses = CryptoAddress.objects.filter(merchant_id__isnull=False)
    for address_obj in addresses:
        try:
            CryptoService.listen_for_transactions(
                address_obj.address,
                address_obj.network
            )
        except Exception as e:
            print(f"Error monitoring {address_obj.address}: {e}")

