from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Client, Contract, Event
from .serializers import ClientListSerializer, ClientDetailSerializer, ContractListSerializer, \
    ContractDetailSerializer, EventSerializer


class ClientListView(APIView):

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientListSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ClientListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sales_contact=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ClientDetailView(APIView):

    def get(self, request, id):
        clients = Client.objects.all()
        client = get_object_or_404(clients, id=id)
        serializer = ClientDetailSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        clients = Client.objects.all()
        client = get_object_or_404(clients, id=id)
        serializer = ClientListSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class ClientContractsList(APIView):

    def get(self, request, id):
        clients = Client.objects.all()
        client = get_object_or_404(clients, id=id)
        contracts = Contract.objects.filter(client=client)
        serializer = ContractListSerializer(contracts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        clients = Client.objects.all()
        client = get_object_or_404(clients, id=id)
        serializer = ContractListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=client, sales_contact=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateClientContract(APIView):

    def post(self, request, client_id, contract_id):
        clients = Client.objects.all()
        client = get_object_or_404(clients, id=client_id)
        contracts = Contract.objects.filter(client=client.id)
        contract = get_object_or_404(contracts, id=contract_id)
        if contract.status:
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(client=client, contract=contract)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("This contract is not yet signed")

    def put(self, request, client_id, contract_id):
        clients = Client.objects.all()
        client = get_object_or_404(clients, id=client_id)
        contracts = Contract.objects.filter(client=client.id)
        contract = get_object_or_404(contracts, id=contract_id)
        serializer = ContractListSerializer(contract, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignContract(APIView):

    def post(self, request, client_id, contract_id):
        clients = Client.objects.all()
        client = get_object_or_404(clients, id=client_id)
        contracts = Contract.objects.filter(client=client.id)
        contract = get_object_or_404(contracts, id=contract_id)
        contract.signed()
        serializer = ContractDetailSerializer(contract)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClientEventList(APIView):

    def get(self, request, id):
        clients = Client.objects.all()
        client = get_object_or_404(clients, id=id)
        events = Event.objects.filter(client=client)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContractListView(APIView):

    def get(self, request):
        contracts = Contract.objects.all()
        serializer = ContractListSerializer(contracts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContractDetailView(APIView):

    def get(self, request, id):
        contracts = Contract.objects.all()
        contract = get_object_or_404(contracts, id=id)
        serializer = ContractDetailSerializer(contract)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventListView(APIView):

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventDetailView(APIView):

    def put(self, request, id):
        events = Event.objects.all()
        event = get_object_or_404(events, id=id)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        events = Event.objects.all()
        event = get_object_or_404(events, id=id)
        event.close()
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FilterByStatusView(APIView):

    def post(self, request):
        category = request.data['category']
        category_status = request.data['status']
        if category == 'contract':
            contracts = Contract.objects.filter(status=category_status)
            serializer = ContractDetailSerializer(contracts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif category == 'event':
            events = Contract.objects.filter(status=category_status)
            serializer = ContractDetailSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("this category does not exist", status=status.HTTP_400_BAD_REQUEST)


