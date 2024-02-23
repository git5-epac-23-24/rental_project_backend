from rest_framework import serializers
from .models import Rent, Product, ProductType
from users.models import Owner
from users.serializers import UserSerializer, UserRetrieveSerializer, OwnerGetSerializer

class RentedSerializers(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = Rent
        fields = ["start_date", "end_date", "cost","product"]
        
    def create(self, validated_data):
        return Rent(**validated_data)
    
class CreateRentedSerializers(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(required=False, allow_null=True)
    
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("start date must be lower than end_date")
        return data
    
    class Meta:
        model = Rent
        fields = ["start_date", "end_date", "cost","product","quantity"]
    
    def create(self, validated_data):
        return Rent(**validated_data)
    
class updateRentedSerializers(serializers.Serializer):
    status = serializers.BooleanField(required=True)
    
    class Meta:
        model = Rent
        fields = ["status"]
        

    
class ProductSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    picture = serializers.ImageField(required=True, allow_null=False)
    # owner = OwnerGetSerializer()
    type = serializers.PrimaryKeyRelatedField(queryset=ProductType.objects.all())
    
    class Meta:
        model= Product
        fields = '__all__'
        # exclude= ('picture',)
        depth = 1
        
    def create(self, validated_data):
        print(validated_data)
        return Product.objects.create(**validated_data)
    
    
class ProductTypeSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model= ProductType
        fields = '__all__'
        depth = 1
    
         
class getRentedSerialisers(serializers.ModelSerializer):
    user = UserRetrieveSerializer(many=False, read_only=True)
    product = ProductSerializers(many=False, read_only=True)
    class Meta:
        model= Rent
        fields = '__all__'
        depth = 1
    