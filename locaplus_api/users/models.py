from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Model for the basic user

class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50)
    profil_picture = models.ImageField(upload_to='users/profil_picture/%Y/%m/%d/', null=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    # password 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # REQUIRED_FIELDS = ['groups_id']

    def __str__(self):
        return self.username

   
class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner')
    id_card = models.ImageField(upload_to='users/owners/id_card/%Y/%m/%d/', blank=True)

    class Meta:
        db_table = 'owners'

    def __str__(self):
        return self.user.username