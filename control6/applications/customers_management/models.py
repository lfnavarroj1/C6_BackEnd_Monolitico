from django.db import models

class Customer(models.Model):
    customer_number = models.CharField(max_length = 15, primary_key = True)
    transformer = models.CharField(max_length = 15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)


