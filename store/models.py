from django.db import models
from users.models import User, Owner




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
    name = models.CharField(max_length=50, blank=True, null=True)
    # location = models.CharField(max_length=500)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    rooms = models.IntegerField(blank=True, null=True)
    superficie = models.FloatField(blank=True, null=True)
    # kitchen = models.IntegerField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    # localisation = models.TextField(blank=True, null=True)
    type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="products"
    )
    extra_spec = models.JSONField(blank=True, null=True)
    picture = models.ImageField(upload_to="products/pictures/%Y/%m/%d/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name


class Rent(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rents"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="rents")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration = models.DurationField()
    cost = models.FloatField()
    status = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rents"

    def __str__(self):
        return self.user.username + " a loué le produit : "+self.product.name





