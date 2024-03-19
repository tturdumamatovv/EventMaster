from rest_framework import serializers
from .models import Event, Expense, Guest, EventImage


class ExpenseSerializer(serializers.ModelSerializer):
    total_expenses = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = '__all__'
    
    def get_total_expenses(self, obj):
        return Expense.total_expenses(obj.event.code) 


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ('id', 'image')


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'date', 'time', 'location', 'description']


class EventSerializer(serializers.ModelSerializer):
    images = EventImageSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
