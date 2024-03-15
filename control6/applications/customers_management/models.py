from django.db import models

class Customer(models.Model):
    customer_number = models.CharField(max_length = 8, primary_key = True)
    transformer = models.CharField(max_length = 8)
    address = models.TextField()


