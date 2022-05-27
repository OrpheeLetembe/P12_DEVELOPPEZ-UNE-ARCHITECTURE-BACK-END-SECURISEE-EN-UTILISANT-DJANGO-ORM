from rest_framework.serializers import ModelSerializer

from .models import Client, Event, Contract


class EventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class ContractListSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = ['id', 'date_created', 'date_updated', 'status', 'amount', 'payment_due', 'client']


class ContractDetailSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = ['id', 'client', 'sales_contact', 'date_created', 'date_updated', 'status',
                  'amount', 'payment_due']


class ClientListSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'sales_contact']


class ClientDetailSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'date_created',
                  'date_updated', 'sales_contact']
