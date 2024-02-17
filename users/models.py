from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Model for the basic user

class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, unique=True, error_messages={
            "unique": "A user with that username already exists.",
        },)
    profil_picture = models.ImageField(upload_to='users/profil_picture/%Y/%m/%d/', null=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    id_card = models.ImageField(upload_to='users/owners/id_card/%Y/%m/%d/', blank=True, null=True)
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
    

class Role(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=255, unique=True, error_messages={
            "unique": "This role already exists.",
        },)
    description = models.TextField()

    def __str__(self) :
        return self.name

class Email(models.Model):
    sender = models.EmailField()
    name = models.CharField(max_length=255 )
    # subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class NewsLetter(models.Model):
    mail = models.EmailField()