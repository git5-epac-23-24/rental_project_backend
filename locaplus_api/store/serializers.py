from rest_framework import serializers
from .models import Rent, Product

class RentedSerializers(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = Rent
        fields = ["start_date", "end_date", "cost","product"]
        
    def create(self, validated_data):
        return Rent(**validated_data)
    
class CreateRentedSerializers(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("start date must be lower than end_date")
        return data
    
    class Meta:
        model = Rent
        fields = ["start_date", "end_date", "cost","product"]
    
    def create(self, validated_data):
        return Rent(**validated_data)
    
class updateRentedSerializers(serializers.Serializer):
    status = serializers.BooleanField(required=True)
    
    class Meta:
        model = Rent
        fields = ["status"]
        
class getRentedSerialisers(serializers.ModelSerializer):
    class Meta:
        model= Rent
        fields = '__all__'
        depth = 1
    
    
class ProductSerializers(serializers.Serializer):
     id = serializers.IntegerField(read_only=True)
     
     class Meta:
         model= Product
         fields = ['__all__']
         depth = 1