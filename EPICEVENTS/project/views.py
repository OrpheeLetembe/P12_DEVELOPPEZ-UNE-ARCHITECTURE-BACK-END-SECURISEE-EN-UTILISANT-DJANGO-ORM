from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Client, Contract, Event
from .serializers import ClientListSerializer, ClientDetailSerializer, ContractListSerializer, \
    ContractDetailSerializer, EventSerializer

from .permissions import IsSalesContact, IsSupportContactOrSalesContact


class MiximViews:
    """
       mixim class which provides the different views with the methods to obtain the client and contract
    """

    permission_classes = [IsSalesContact]

    def get_client(self, request, id):
        clients = Client.objects.all()
        client = get_object_or_404(clients, id=id)
        return client

    def get_client_contract(self, request, client_id, contract_id):
        client = self.get_client(request, client_id)
        contracts = Contract.objects.filter(client=client)
        contract = get_object_or_404(contracts, id=contract_id)
        return contract


class ClientListView(MiximViews, APIView):

    """
        Class that provides methods for client :
               - get the list of clients.
               - create a new client.
    """

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientListSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        if user.team == 'SALE':
            serializer = ClientListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(sales_contact=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("You do not have permission to perform this action.", status=status.HTTP_403_FORBIDDEN)


class ClientDetailView(MiximViews, APIView):
    """
        Class that provides methods for client :
                - get the details of a client.
                - update client data.
    """

    def get(self, request, id):
        client = self.get_client(request, id=id)
        serializer = ClientDetailSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        client = self.get_client(request, id=id)
        self.check_object_permissions(request, client)
        serializer = ClientListSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class ClientContractsList(MiximViews, APIView):

    """
        Class that provides methods for contract :
                - get a client contracts list.
                - create a contract for a client.
    """

    def get(self, request, id):
        client = self.get_client(request, id=id)
        contracts = Contract.objects.filter(client=client)
        serializer = ContractListSerializer(contracts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        client = self.get_client(request, id=id)
        self.check_object_permissions(request, client)
        serializer = ContractListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=client, sales_contact=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateClientContract(MiximViews, APIView):
    """
        Class that provides methods for contract :
                - create an event for a contract.
                - update contract data.
    """

    # link an event to a contract if the one is signed and request user is a seller
    def post(self, request, client_id, contract_id):
        contract = self.get_client_contract(request, client_id, contract_id)
        if contract.status and request.user.team == 'SALE':
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(client=contract.client, contract=contract)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("This contract is not yet signed")

    def put(self, request, client_id, contract_id):
        contract = self.get_client_contract(request, client_id, contract_id)
        self.check_object_permissions(request, contract)
        serializer = ContractListSerializer(contract, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignContract(MiximViews, APIView):
    """ mark that an contract is signed """

    def post(self, request, client_id, contract_id):
        contract = self.get_client_contract(request, client_id, contract_id)
        self.check_object_permissions(request, contract)
        contract.signed()
        serializer = ContractDetailSerializer(contract)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClientEventList(MiximViews, APIView):

    def get(self, request, id):
        client = self.get_client(request, id=id)
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
    """
        Class that provides methods for event :
               - update event data.
               - mark that an event is finished.
    """
    permission_classes = [IsSupportContactOrSalesContact]

    def put(self, request, id):
        events = Event.objects.all()
        event = get_object_or_404(events, id=id)
        self.check_object_permissions(request, event)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # mark that an event is close
    def post(self, request, id):
        events = Event.objects.all()
        event = get_object_or_404(events, id=id)
        self.check_object_permissions(request, event)
        event.close()
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FilterByStatusView(APIView):
    """ Class that allows users to filter contracts or events according to their status """

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


