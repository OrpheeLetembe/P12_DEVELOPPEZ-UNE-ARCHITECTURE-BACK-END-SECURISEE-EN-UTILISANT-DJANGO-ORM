import logging
import datetime

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Client, Contract, Event
from .serializers import ClientListSerializer, ClientDetailSerializer, ContractListSerializer, \
    ContractDetailSerializer, EventSerializer

from .permissions import IsSalesContact, IsSupportContactOrSalesContact

logger = logging.getLogger('django')


class MiximViews:
    """
       mixim class which provides the different views with the methods to obtain the client and contract
    """

    permission_classes = [IsSalesContact]

    def get_client(self, request, id):
        client = get_object_or_404(Client, id=id)
        return client

    def get_client_contract(self, request, client_id, contract_id):
        contract = get_object_or_404(Contract, client=client_id, id=contract_id)
        return contract


"""     CLIENT    """


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


"""     CONTRACT   """


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


class AddContractView(MiximViews, APIView):

    """ Class that provides method for create a contract. """

    def post(self, request, id):
        client = self.get_client(request, id=id)
        if request.user.team == 'SALE':
            serializer = ContractListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(client=client, sales_contact=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("You do not have permission to perform this action.", status=status.HTTP_403_FORBIDDEN)


class UpdateContractView(MiximViews, APIView):
    """
        Class that provides methods for contract :
                - create an event for a contract.
                - update contract data.
    """

    def post(self, request, client_id, contract_id):
        """Link an event to a contract if the one is signed and request user is a seller"""

        contract = self.get_client_contract(request, client_id, contract_id)
        if request.user != contract.sales_contact:
            return Response("You do not have permission to perform this action.", status=status.HTTP_403_FORBIDDEN)
        if contract.status:
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


"""     EVENT    """


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

    def get(self, request, id):
        events = Event.objects.all()
        event = get_object_or_404(events, id=id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        events = Event.objects.all()
        event = get_object_or_404(events, id=id)
        self.check_object_permissions(request, event)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        """ Mark that an event is close"""

        events = Event.objects.all()
        event = get_object_or_404(events, id=id)
        self.check_object_permissions(request, event)
        event.close()
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""     FILTERS    """


class FilterView(APIView):

    """ Class that allows users to filter:
        client by last name or email.
        contracts by the client last name, the client email, the date of creation or the contract amount.
        events based on the client last name, client email or event date.

        """

    def post(self, request):
        model = request.data['category']
        model_field = request.data['field']
        search_key = request.data['search']

        if model == 'client':
            search_fields = ['last_name', 'email']
            if model_field in search_fields:
                client = self.filter_client(model_field, search_key)
                serializer = ClientDetailSerializer(client)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response('Field error: try last_name or email', status=status.HTTP_400_BAD_REQUEST)

        elif model == 'contract':
            search_fields = ['last_name', 'email', 'amount', 'date_created']
            if model_field in search_fields:
                contracts = self.filter_contract(model_field, search_key)
                serializer = ContractListSerializer(contracts, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response('Field error: try last_name, email, amount or date_created',
                            status=status.HTTP_400_BAD_REQUEST)

        elif model == 'event':
            search_fields = ['last_name', 'email', 'event_date']
            if model_field in search_fields:
                events = self.filter_event(model_field, search_key)
                serializer = EventSerializer(events, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response('Field error: try last_name, email or event_date',
                            status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response("this category does not exist : try client, contract or event",
                            status=status.HTTP_400_BAD_REQUEST)

    def filter_client(self, field, search):
        """ Method for performing client filters"""

        if field == 'last_name':
            return get_object_or_404(Client, last_name=search)
        if field == 'email':
            return get_object_or_404(Client, email=search)

    def filter_contract(self, field, search):
        """ Method for performing contract filters"""
        if field == 'last_name':
            client = get_object_or_404(Client, last_name=search)
            return Contract.objects.filter(client=client)
        if field == 'email':
            client = get_object_or_404(Client, email=search)
            return Contract.objects.filter(client=client)

        if field == 'amount' and search.isdigit():
            return Contract.objects.filter(amount=search)
        if field == 'date_created':
            contract_date = self.check_date(search)
            if contract_date is not None:
                return Contract.objects.filter(date_created=search)

    def filter_event(self, field, search):
        """ Method for performing event filters"""
        if field == 'last_name':
            client = get_object_or_404(Client, last_name=search)
            return Event.objects.filter(client=client)
        if field == 'email':
            client = get_object_or_404(Client, email=search)
            return Event.objects.filter(client=client)
        if field == 'event_date':
            event_date = self.check_date(search)
            if event_date is not None:
                return Event.objects.filter(event_date=search)

    def check_date(self, value):
        format_date = '%Y-%m-%dT%H:%M:%S.%fZ'
        try:
            valid_date = datetime.datetime.strptime(value, format_date)
        except ValueError:
            return None
        return valid_date






