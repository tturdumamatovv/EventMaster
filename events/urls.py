from django.urls import path
from .views import (EventCreateAPIView,
                    EventListAPIView,
                    EventRetrieveAPIView,
                    EventDestroyAPIView,
                    EventUpdateAPIView,
                    ExpenseCreateAPIView, 
                    ExpenseRetrieveUpdateDestroyAPIView, 
                    GuestCreateAPIView, 
                    GuestRetrieveUpdateDestroyAPIView, 
                    GuestListAPIView, 
                    ExpensesListAPIView)

urlpatterns = [
    path('event-create/', EventCreateAPIView.as_view(), name='event-create'),
    path('events/', EventListAPIView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventRetrieveAPIView.as_view(), name='event-retrieve'),
    path('events-delete/<int:pk>/', EventDestroyAPIView.as_view(), name='event-delete'),
    path('events-update/<int:pk>/', EventUpdateAPIView.as_view(), name='event-update'),
    path('expenses/', ExpenseCreateAPIView.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/', ExpenseRetrieveUpdateDestroyAPIView.as_view(), name='expense-detail'),
    path('guests/', GuestCreateAPIView.as_view(), name='guest-list-create'),
    path('guests/<int:pk>/', GuestRetrieveUpdateDestroyAPIView.as_view(), name='guest-retrieve-update-destroy'),
    path('events/<int:event_id>/guests/', GuestListAPIView.as_view(), name='event-guests-list'),
    path('events/<int:event_id>/expenses/', ExpensesListAPIView.as_view(), name='event-expenses-list'),
]
