from rest_framework import serializers
from Center.models import Category,Deliverer

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Assign Deliverer
class AssignDelivererSerializer(serializers.Serializer):
    deliverer_id = serializers.IntegerField()

    def validate_deliverer_id(self, value):
        try:
            deliverer = Deliverer.objects.get(id=value)
        except Deliverer.DoesNotExist:
            raise serializers.ValidationError("Deliverer does not exist.")

        if not deliverer.available:
            raise serializers.ValidationError("Deliverer is currently unavailable.")

        return value
    
# Create Deliverer Serializer
class DelivererCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    phone = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = Deliverer
        fields = [
            "username",
            "email",
            "password",
            "name",
            "phone",
            "profile_image",
        ]

    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role="DELIVERER",
        )

        deliverer = Deliverer.objects.create(
            user=user,
            available=True,
            **validated_data
        )

        return deliverer