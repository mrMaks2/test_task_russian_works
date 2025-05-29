from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Organization, Payment, BalanceLog
from .serializers import OrganizationSerializer, PaymentSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def handle_bank_webhook(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        operation_id = validated_data['operation_id']

        # Проверка на дубли
        if Payment.objects.filter(operation_id=operation_id).exists():
            return Response({'message': 'Операция уже обработана'}, status=status.HTTP_200_OK)

        payer_inn = validated_data['payer_inn']
        amount = validated_data['amount']
        document_number = validated_data['document_number']
        document_date = validated_data['document_date']


        try:
            organization, created = Organization.objects.get_or_create(inn=payer_inn)
            old_balance = organization.balance
            organization.balance += amount
            organization.save()

            payment = Payment.objects.create(
                operation_id=operation_id,
                organization=organization,
                amount=amount,
                document_number=document_number,
                document_date=document_date
            )

            # Логирование изменения баланса
            BalanceLog.objects.create(
                organization=organization,
                old_balance=old_balance,
                new_balance=organization.balance,
                payment=payment
            )
            logger.info(f"Баланс организации {payer_inn} был обновлен. Старый баланс: {old_balance}, новый баланс: {organization.balance}")


            return Response({'message': 'Платеж успешно обработан'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Ошибка обработки webhook-а: {e}")
            return Response({'message': f'Ошибка обработки webhook-а: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_organization_balance(request, inn):
    try:
        organization = Organization.objects.get(inn=inn)
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Organization.DoesNotExist:
        return Response({'message': 'Организация не найдена'}, status=status.HTTP_404_NOT_FOUND)