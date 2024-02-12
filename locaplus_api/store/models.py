from django.db import models
from users.models import Customer, Owner




# Create your models here.



class ProductType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product_types"

    def __str__(self):
        return self.name

class Product(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=500)
    availability = models.BooleanField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="products"
    )
    picture = models.ImageField(upload_to="products/pictures/%Y/%m/%d/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name



class Rent(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="rents"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="rents")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rents"

    def __str__(self):
        return self.customer.user.username





