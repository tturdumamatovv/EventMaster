from django.db import models
from django.db.models import Sum


class EventImage(models.Model):
    event = models.ForeignKey('Event', related_name='event_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self): 
        return self.event.title


class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    event_type = models.CharField(max_length=100)
    max_guests = models.PositiveIntegerField()
    dress_code = models.CharField(max_length=100)
    description = models.TextField()
    contact_info = models.TextField()
    images = models.ManyToManyField(EventImage, related_name='events', blank=True)
    code = models.CharField(max_length=50)

    def __str__(self): 
        return self.title


class Expense(models.Model):
    event = models.ForeignKey(Event, related_name='expenses', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self): 
        return self.event.title

    @classmethod
    def total_expenses(cls, event_code):
        try:
            event = Event.objects.get(code=event_code)
            return cls.objects.filter(event=event).aggregate(total=Sum('amount'))['total'] or 0
        except Event.DoesNotExist:
            return 0


class Guest(models.Model):
    event = models.ForeignKey(Event, related_name='guests', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self): 
        return self.event.title
