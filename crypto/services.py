from web3 import Web3
from django.conf import settings
from decimal import Decimal
from .models import CryptoAddress, CryptoTransaction


class CryptoService:
    _providers = {}

    @staticmethod
    def get_provider(network='ethereum'):
        if network in CryptoService._providers:
            return CryptoService._providers[network]

        rpc_urls = {
            'ethereum': getattr(settings, 'ETHEREUM_RPC_URL', 'https://mainnet.infura.io/v3/YOUR_KEY'),
            'polygon': getattr(settings, 'POLYGON_RPC_URL', 'https://polygon-rpc.com'),
            'bsc': getattr(settings, 'BSC_RPC_URL', 'https://bsc-dataseed.binance.org'),
        }

        rpc_url = rpc_urls.get(network)
        if not rpc_url:
            raise ValueError(f"Unsupported network: {network}")

        provider = Web3(Web3.HTTPProvider(rpc_url))
        CryptoService._providers[network] = provider
        return provider

    @staticmethod
    def create_payment_address(payment_id, address, amount):
        return {
            'address': address,
            'amount': str(amount),
            'payment_id': str(payment_id)
        }

    @staticmethod
    def register_address(user_id, merchant_id, address, network='ethereum'):
        crypto_address, created = CryptoAddress.objects.get_or_create(
            user_id=user_id,
            merchant_id=merchant_id,
            network=network,
            defaults={'address': address}
        )
        return crypto_address

    @staticmethod
    def get_transaction_status(tx_hash, network='ethereum'):
        try:
            tx = CryptoTransaction.objects.get(tx_hash=tx_hash)
            return {
                'tx_hash': tx.tx_hash,
                'status': tx.status,
                'confirmations': tx.confirmations,
                'block_number': tx.block_number,
                'amount': str(tx.amount)
            }
        except CryptoTransaction.DoesNotExist:
            provider = CryptoService.get_provider(network)
            try:
                receipt = provider.eth.get_transaction_receipt(tx_hash)
                if receipt:
                    status = 'confirmed' if receipt.status == 1 else 'failed'
                    tx_obj = CryptoTransaction.objects.create(
                        tx_hash=tx_hash,
                        merchant_id=None,
                        from_address=receipt.get('from', ''),
                        to_address=receipt.get('to', ''),
                        amount=Decimal('0'),
                        network=network,
                        status=status,
                        block_number=receipt.blockNumber,
                        confirmations=1
                    )
                    return {
                        'tx_hash': tx_hash,
                        'status': status,
                        'confirmations': 1,
                        'block_number': tx_obj.block_number
                    }
            except Exception:
                pass

            return {
                'tx_hash': tx_hash,
                'status': 'pending',
                'confirmations': 0
            }

    @staticmethod
    def listen_for_transactions(address, network='ethereum'):
        provider = CryptoService.get_provider(network)
        latest_block = provider.eth.block_number
        from_block = max(0, latest_block - 100)

        logs = provider.eth.get_logs({
            'fromBlock': from_block,
            'toBlock': 'latest',
            'address': Web3.to_checksum_address(address)
        })

        transactions = []
        for log in logs:
            tx_hash = log.transactionHash.hex()
            tx = provider.eth.get_transaction(tx_hash)
            receipt = provider.eth.get_transaction_receipt(tx_hash)

            if receipt and receipt.status == 1:
                CryptoTransaction.objects.update_or_create(
                    tx_hash=tx_hash,
                    defaults={
                        'from_address': tx['from'],
                        'to_address': tx['to'],
                        'amount': Decimal(str(provider.from_wei(tx.value, 'ether'))),
                        'network': network,
                        'status': 'confirmed',
                        'block_number': receipt.blockNumber,
                        'confirmations': latest_block - receipt.blockNumber + 1
                    }
                )
                transactions.append(tx_hash)

        return transactions

