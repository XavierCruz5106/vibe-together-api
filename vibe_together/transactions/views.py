from rest_framework.routers import DefaultRouter
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from decimal import Decimal

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @action(detail=True, methods=['post'])
    def deposit(self, request, pk=None):
        account = self.get_object()
        amount = request.data.get('amount')
        if amount and Decimal(amount) > 0:
            account.balance += Decimal(amount)
            account.save()
            return Response({'message': 'Deposit successful', 'balance': account.balance})
        return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        account = self.get_object()
        amount = request.data.get('amount')
        if amount and 0 < Decimal(amount) <= account.balance:
            account.balance -= Decimal(amount)
            account.save()
            return Response({'message': 'Withdrawal successful', 'balance': account.balance})
        return Response({'error': 'Invalid amount or insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        sender_id = data.get('sender')
        recipient_id = data.get('recipient')
        amount = data.get('amount')

        try:
            sender = Account.objects.get(id=sender_id)
            recipient = Account.objects.get(id=recipient_id)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        if sender.balance < Decimal(amount):
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

        sender.balance -= Decimal(amount)
        recipient.balance += Decimal(amount)
        sender.save()
        recipient.save()

        transaction = Transaction.objects.create(sender=sender, recipient=recipient, amount=amount)
        serializer = self.get_serializer(transaction)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# URL Router
router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')
