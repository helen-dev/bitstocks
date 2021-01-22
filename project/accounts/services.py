from django.db import IntegrityError, transaction as tr

from .models import Account, Transaction


def convert_to_satoshi(bitcoin):
    satoshi = bitcoin * 10 ** 8
    return satoshi


def convert_to_bitcoin(satoshi):
    bitcoin = satoshi / 10 ** 8
    return bitcoin


def perform_deposit(user, amount):
    amount = convert_to_satoshi(amount)
    account = Account.objects.get(user=user)
    account.balance += amount

    try:
        with tr.atomic():
            account.save()

            transaction = Transaction.objects.create(
                account=account,
                transaction_type=Transaction.TRANSACTION_TYPE_DEPOSIT,
                amount=amount
            )

        return transaction
    except IntegrityError:
        pass


def perform_withdrawal(user, amount):
    amount = convert_to_satoshi(amount)
    account = Account.objects.get(user=user)
    if account.balance < amount:
        return
    account.balance -= amount

    try:
        with tr.atomic():
            account.save()
            transaction = Transaction.objects.create(
                account=account,
                transaction_type=Transaction.TRANSACTION_TYPE_WITHDRAWAL,
                amount=amount
            )

        return transaction
    except IntegrityError:
        pass
