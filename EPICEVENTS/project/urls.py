from django.urls import path


from .views import ClientListView, ClientDetailView, AddContractView, ContractListView, ContractDetailView, \
    UpdateContractView, EventListView,  SignContract, EventDetailView, FilterView


urlpatterns = [

    path('clients/', ClientListView.as_view()),
    path('clients/<int:id>/', ClientDetailView.as_view()),
    path('clients/<int:id>/contracts/', AddContractView.as_view()),
    path('clients/<int:client_id>/contracts/<int:contract_id>', UpdateContractView.as_view()),
    path('clients/<int:client_id>/contracts/<int:contract_id>/signed/', SignContract.as_view()),


    path('contracts/', ContractListView.as_view()),
    path('contracts/<int:id>/', ContractDetailView.as_view()),

    path('events/', EventListView.as_view()),
    path('events/<int:id>', EventDetailView.as_view()),

    path('filters', FilterView.as_view()),

]
