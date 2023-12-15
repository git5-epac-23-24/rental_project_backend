from django.db import models

# Create your models here.

class User(models.Model):
    firstname = models.CharField("Firstname", max_length=240)
    lastname = models.CharField("Lastname", max_length=240)
    email = models.EmailField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.firstname
