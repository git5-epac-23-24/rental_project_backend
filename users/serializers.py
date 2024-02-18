from django.contrib.auth.models import Group
from users.models import User, Owner, Subscribers
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
        extra_kwargs = {
            "password": {"write_only": True},
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=50, required=True)
    
    class Meta:
        fields = [
            "password",
            "username"
        ]




class UserSerializer(serializers.ModelSerializer):
    # groups = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Group.objects.all(), required=False
    # )
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    
    profil_picture = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "country",
            "profil_picture",
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
        instance.address = validated_data.get("address", instance.address)
        instance.city = validated_data.get("city", instance.city)
        instance.country = validated_data.get("country", instance.country)
        instance.profil_picture = validated_data.get("profil_picture", instance.profil_picture)
        instance.set_password(validated_data.get("password", instance.password))
        instance.save()
        return instance
    
    
# class OwnerSerializer(serializers.ModelSerializer):
#     # groups = serializers.PrimaryKeyRelatedField(
#     #     many=True, queryset=Group.objects.all(), required=False
#     # )
#     id = serializers.IntegerField(read_only=True)
#     class Meta:
#         model = Owner
#         fields = [
#             "id",
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "phone",
#             "address",
#             "city",
#             "country",
#             "profil_picture",
#             # "groups",
#             "password",
#             "id_card",
#         ]
#         extra_kwargs = {
#             "password": {"write_only": True},
#         }

#     def create(self, validated_data):
#         user_data = {
#             "username": validated_data.get("username"),
#             "first_name": validated_data.get("first_name"),
#             "last_name": validated_data.get("last_name"),
#             "email": validated_data.get("email"),
#             "phone": validated_data.get("phone"),
#             "address": validated_data.get("address"),
#             "city": validated_data.get("city"),
#             "country": validated_data.get("country"),
#             "profil_picture": validated_data.get("profil_picture"),
#             "password": validated_data.get("password"),
#         }
#         user = User.objects.create_user(**user_data)
#         owner = Owner(user=user, id_card=validated_data.get("id_card"))
#         return owner

#     def update(self, instance, validated_data):
#         instance.username = validated_data.get("username", instance.username)
#         instance.first_name = validated_data.get("first_name", instance.first_name)
#         instance.last_name = validated_data.get("last_name", instance.last_name)
#         instance.email = validated_data.get("email", instance.email)
#         instance.phone = validated_data.get("phone", instance.phone)
#         instance.address = validated_data.get("address", instance.address)
#         instance.city = validated_data.get("city", instance.city)
#         instance.country = validated_data.get("country", instance.country)
#         instance.profil_picture = validated_data.get("profil_picture", instance.profil_picture)
#         instance.id_card = validated_data.get("id_card", instance.id_card)
#         instance.set_password(validated_data.get("password", instance.password))
        
#         instance.save()
#         return instance
        
class SubscriberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subscribers
        fields = '__all__' 
        
class MailSerializer(serializers.Serializer):
    subject = serializers.CharField(required = True, max_length = 255)
    message = serializers.CharField(required = True)
    
    
    
class OwnerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer()
    class Meta:
        model = Owner
        fields = [
            "id",
            "user",
            "id_card",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }
        
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        owner = Owner.objects.create(user=user, **validated_data)
        return owner
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user = instance.user
        user.username = user_data.get("username", user.username)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.email = user_data.get("email", user.email)
        user.phone = user_data.get("phone", user.phone)
        user.address = user_data.get("address", user.address)
        user.city = user_data.get("city", user.city)
        user.country = user_data.get("country", user.country)
        user.profil_picture = user_data.get("profil_picture", user.profil_picture)
        user.set_password(user_data.get("password", user.password))
        user.save()
        
        instance.id_card = validated_data.get("id_card", instance.id_card)
        instance.save()
        return instance    
# class OwnerSerializer(serializers.Serializer):
#     # groups = serializers.PrimaryKeyRelatedField(
#     #     many=True, queryset=Group.objects.all(), required=False
#     # )
#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(max_length=50, required=False)
#     first_name = serializers.CharField(max_length=50, required=False)
#     last_name = serializers.CharField(max_length=50, required=False)
#     email = serializers.EmailField(max_length=50, required=False)
#     phone = serializers.CharField(max_length=50, required=False)
#     address = serializers.CharField(max_length=50, required=False)
#     city = serializers.CharField(max_length=50, required=False)
#     country = serializers.CharField(max_length=50, required=False)
#     profil_picture = serializers.ImageField(required=False)
#     password = serializers.CharField(max_length=50, required=True)
#     id_card = serializers.ImageField(required=False)
#     class Meta:
#         extra_kwargs = {
#             "password": {"write_only": True},
#         }

#     def create(self, validated_data):
#         user_data = {
#             "username": validated_data.get("username"),
#             "first_name": validated_data.get("first_name"),
#             "last_name": validated_data.get("last_name"),
#             "email": validated_data.get("email"),
#             "phone": validated_data.get("phone"),
#             "address": validated_data.get("address"),
#             "city": validated_data.get("city"),
#             "country": validated_data.get("country"),
#             "profil_picture": validated_data.get("profil_picture"),
#             "password": validated_data.get("password"),
#         }
#         user = User.objects.create_user(**user_data)
#         owner = Owner(user=user, id_card=validated_data.get("id_card"))
#         return owner

#     # def update(self, instance, validated_data):
#     #     instance.username = validated_data.get("username", instance.username)
#     #     instance.first_name = validated_data.get("first_name", instance.first_name)
#     #     instance.last_name = validated_data.get("last_name", instance.last_name)
#     #     instance.email = validated_data.get("email", instance.email)
#     #     instance.phone = validated_data.get("phone", instance.phone)
#     #     instance.address = validated_data.get("address", instance.address)
#     #     instance.city = validated_data.get("city", instance.city)
#     #     instance.country = validated_data.get("country", instance.country)
#     #     instance.profil_picture = validated_data.get("profil_picture", instance.profil_picture)
#     #     instance.id_card = validated_data.get("id_card", instance.id_card)
#     #     instance.set_password(validated_data.get("password", instance.password))
        
#     #     instance.save()
#     #     return instance
    
class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, required=False)
    first_name = serializers.CharField(max_length=50, required=False)
    last_name = serializers.CharField(max_length=50, required=False)
    email = serializers.EmailField(max_length=50, required=False)
    phone = serializers.CharField(max_length=50, required=False)
    address = serializers.CharField(max_length=50, required=False)
    city = serializers.CharField(max_length=50, required=False) 
    country = serializers.CharField(max_length=50, required=False)
    profil_picture = serializers.ImageField(required=False)
    password = serializers.CharField(max_length=50, required=False)
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "country",
            "profil_picture",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class UserCreationSerializer(serializers.ModelSerializer):
    profil_picture = serializers.ImageField(required=True)
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "country",
            "profil_picture",
            "password",
            "profil_picture"
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
        instance.address = validated_data.get("address", instance.address)
        instance.city = validated_data.get("city", instance.city)
        instance.country = validated_data.get("country", instance.country)
        instance.profil_picture = validated_data.get("profil_picture", instance.profil_picture)
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
            "address",
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
        instance.address = validated_data.get("address", instance.address)
        instance.city = validated_data.get("city", instance.city)
        instance.country = validated_data.get("country", instance.country)
        instance.profil_picture = validated_data.get(
            "profil_picture", instance.profil_picture
        )
        # instance.set_password(validated_data.get("password", instance.password))
        instance.save()
        return instance


class FileListSerializer ( serializers.Serializer ) :
    image = serializers.ListField(
                       child=serializers.FileField( max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False )
                                )

class OwnerCreationSerializer(serializers.ModelSerializer):
    files = serializers.ListField(child=serializers.FileField())
    class Meta:
        model = Owner
        fields = '__all__'

class OwnerGetSerializer(serializers.ModelSerializer):
    user = UserRetrieveSerializer(many=False, read_only=True)
    class Meta:
        model = Owner
        fields = '__all__'
        
class OwnerUpgradeSerializer(serializers.ModelSerializer):
    id_card = serializers.ImageField(required=True)
    class Meta:
        model = Owner
        fields = ['id_card']  

# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = [ 'name']
