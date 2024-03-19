from django.contrib import admin
from .models import EventImage, Event, Expense, Guest


admin.site.register(Event)
admin.site.register(EventImage)
admin.site.register(Expense)
admin.site.register(Guest)
