from django.conf import settings
from django.db import models


class Client(models.Model):

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      limit_choices_to={"team": "SALE"})

    def __str__(self):
        return self.company_name


class Contract(models.Model):
    sales_contact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      limit_choices_to={"team": "SALE"})

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField()
    payment_due = models.DateField()

    def signed(self):
        if self.status is True:
            return
        self.status = True
        self.save()

    def __str__(self):
        return f' id : {self.id} - client: {self.client}'


class Event(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    event_status = models.BooleanField(default=False)
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField()
    support_contact = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,  on_delete=models.CASCADE,
                                        limit_choices_to={"team": "SUPPORT"})

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, limit_choices_to={"status": True})

    def close(self):
        if self.event_status is True:
            return
        self.event_status = True
        self.save()

    def __str__(self):
        return f' id : {self.id} - client: {self.client}'








