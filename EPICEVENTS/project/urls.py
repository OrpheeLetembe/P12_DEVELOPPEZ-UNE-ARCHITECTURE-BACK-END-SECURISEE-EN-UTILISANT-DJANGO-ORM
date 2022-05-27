from django.urls import path


from .views import ClientListView, ClientDetailView, ClientContractsList, ContractListView, ContractDetailView, \
    UpdateClientContract, EventListView, ClientEventList,  SignContract, EventDetailView, FilterByStatusView


urlpatterns = [
    path('clients/', ClientListView.as_view()),
    path('clients/<int:id>/', ClientDetailView.as_view()),
    path('clients/<int:id>/contracts/', ClientContractsList.as_view()),
    path('clients/<int:client_id>/contracts/<int:contract_id>', UpdateClientContract.as_view()),
    path('clients/<int:client_id>/contracts/<int:contract_id>/signed/', SignContract.as_view()),
    path('clients/<int:id>/events/', ClientEventList.as_view()),

    path('contracts/', ContractListView.as_view()),
    path('contracts/<int:id>/', ContractDetailView.as_view()),

    path('events/', EventListView.as_view()),
    path('events/<int:id>', EventDetailView.as_view()),

    path('filter_by_status', FilterByStatusView.as_view()),

]
