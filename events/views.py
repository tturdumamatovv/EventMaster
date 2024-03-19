from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Event, Expense, Guest
from .serializers import EventSerializer, ExpenseSerializer, GuestSerializer, EventListSerializer
from rest_framework.exceptions import PermissionDenied, NotFound, ParseError


class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    permission_classes = [AllowAny]  # Разрешить доступ к списку событий без аутентификации


class EventCreateAPIView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]  # Разрешить создание событий без аутентификации

    def perform_create(self, serializer):
        # Получаем данные из запроса
        title = self.request.data.get('title')
        date = self.request.data.get('date')
        time = self.request.data.get('time')
        location = self.request.data.get('location')
        event_type = self.request.data.get('event_type')
        max_guests = self.request.data.get('max_guests')
        dress_code = self.request.data.get('dress_code')
        description = self.request.data.get('description')
        contact_info = self.request.data.get('contact_info')
        code = self.request.data.get('code')

        # Создаем новое событие
        event = Event.objects.create(
            title=title,
            date=date,
            time=time,
            location=location,
            event_type=event_type,
            max_guests=max_guests,
            dress_code=dress_code,
            description=description,
            contact_info=contact_info,
            code=code
        )

        # Сохраняем событие
        event.save()
        return event


class EventRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]  # Разрешить доступ к отдельному событию без аутентификации


class EventDestroyAPIView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def delete(self, request, *args, **kwargs):
        event = self.get_event_object()
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_event_object(self):
        code = self.request.data.get('code')
        if not code:
            raise PermissionDenied("Event code is required.")
        try:
            return Event.objects.get(code=code)
        except Event.DoesNotExist:
            raise NotFound("Event with the provided code does not exist.")


class EventUpdateAPIView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def update(self, request, *args, **kwargs):
        event = self.get_event_object()
        serializer = self.get_serializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_event_object(self):
        code = self.request.data.get('code')
        if not code:
            raise PermissionDenied("Event code is required.")
        try:
            return Event.objects.get(code=code)
        except Event.DoesNotExist:
            raise NotFound("Event with the provided code does not exist.")


class ExpenseCreateAPIView(generics.CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        event = self.get_event_object()
        serializer.save(event=event)

    def get_event_object(self):
        code = self.request.data.get('code')
        if not code:
            raise PermissionDenied("Event code is required in the request body.")
        try:
            return Event.objects.get(code=code)
        except Event.DoesNotExist:
            raise PermissionDenied("Event with the provided code does not exist.")


class ExpenseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get_event_object(self):
        expense = self.get_object()
        return expense.event


class GuestCreateAPIView(generics.CreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [AllowAny]  # Разрешить создание гостей без аутентификации


class GuestRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get_event_object(self):
        guest = self.get_object()
        return guest.event


class GuestListAPIView(generics.ListAPIView):
    serializer_class = GuestSerializer

    def get_queryset(self):
        event = self.get_event_object()
        return Guest.objects.filter(event=event)

    def get_event_object(self):
        code = self.request.data.get('code')
        if not code:
            raise ParseError("Event code is required in the request body.")
        try:
            event = Event.objects.get(code=code)
            return event
        except Event.DoesNotExist:
            raise NotFound("Event with the provided code does not exist.")


class ExpensesListAPIView(generics.ListAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        event = self.get_event_object()
        return Expense.objects.filter(event=event)

    def get_event_object(self):
        code = self.request.data.get('code')
        if not code:
            raise ParseError("Event code is required in the request body.")
        try:
            event = Event.objects.get(code=code)
            return event
        except Event.DoesNotExist:
            raise NotFound("Event with the provided code does not exist.")
