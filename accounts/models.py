from django.db import models

class Registration(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    salary = models.FloatField(default=30000)

    def __str__(self):
        return self.email