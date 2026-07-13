from rest_framework import serializers
from Center.models import Order, OrderItem
from Center.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "subtotal",
        ]


class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "product",
            "quantity",
        ]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.ReadOnlyField(source="customer.username")

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_name",
            "items",
            "total_amount",
            "status",
            "delivery_address",
            "created_at",
            "updated_at",
            "delivered_at",
        ]

class CreateOrderSerializer(serializers.ModelSerializer):
    items = CreateOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "delivery_address",
            "items",
        ]


    def create(self, validated_data):
        items_data = validated_data.pop("items")

        customer = self.context["request"].user.customer_profile

        order = Order.objects.create(
            customer=customer,
            delivery_address=validated_data["delivery_address"],
            total_amount=0
        )

        for item in items_data:
            product = item["product"]
            quantity = item["quantity"]

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price
            )

        order.update_total()

        return order