from django.contrib.auth.models import Group
from users.models import User, Customer, Owner
from rest_framework import serializers





class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=50, required=True)
    
    class Meta:
        fields = [
            "username",
            "password",
        ]




class UserSerializer(serializers.ModelSerializer):
    # groups = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Group.objects.all(), required=False
    # )
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "city",
            "country",
            # "groups",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.city = validated_data.get("city", instance.city)
        instance.country = validated_data.get("country", instance.country)
        instance.set_password(validated_data.get("password", instance.password))
        instance.save()
        return instance
    
    
class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, required=False)
    first_name = serializers.CharField(max_length=50, required=False)
    last_name = serializers.CharField(max_length=50, required=False)
    email = serializers.EmailField(max_length=50, required=False)
    phone = serializers.CharField(max_length=50, required=False)
    city = serializers.CharField(max_length=50, required=False) 
    country = serializers.CharField(max_length=50, required=False)
    password = serializers.CharField(max_length=50, required=False)
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "city",
            "country",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "city",
            "country",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.city = validated_data.get("city", instance.city)
        instance.country = validated_data.get("country", instance.country)
        instance.set_password(validated_data.get("password", instance.password))
        instance.save()
        return instance


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "city",
            "country",
            "created_at",
            "updated_at",
            "profil_picture",
        ]
        # extra_kwargs = {
        #     "password": {"write_only": True},
        # }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.city = validated_data.get("city", instance.city)
        instance.country = validated_data.get("country", instance.country)
        instance.profil_picture = validated_data.get(
            "profil_picture", instance.profil_picture
        )
        # instance.set_password(validated_data.get("password", instance.password))
        instance.save()
        return instance


class UserCreationTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]
        # extra_kwargs = {
        #     "password": {"write_only": True},
        # }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.set_password(validated_data.get("password", instance.password))
        instance.save()
        return instance


class CustomerSerializer(serializers.ModelSerializer):
    user = UserRetrieveSerializer()

    class Meta:
        model = Customer
        fields = ["id", "user"]


class OwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Owner
        fields = ["id", "user", "address", "created_at", "updated_at"]


# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = [ 'name']
