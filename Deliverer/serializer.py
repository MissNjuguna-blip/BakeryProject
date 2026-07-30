from rest_framework import serializers

from Center.models import Deliverer,Order

# code starts here
class DelivererSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliverer
        fields = ['name','phone']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "deliverer",
            "total_amount",
            "status",
            "delivery_address",
            "delivered_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "total_amount",
            "delivered_at",
            "created_at",
            "updated_at",
        ]


