from rest_framework import serializers
from Center.models import Payment
from Center.models import Order

# make payment
class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["order", "method"]

    def validate_order(self, order):
        request = self.context["request"]

        # Ensure the order belongs to the logged-in user
        if order.user != request.user:
            raise serializers.ValidationError(
                "You can only pay for your own orders."
            )

        # Prevent duplicate payments
        if Payment.objects.filter(order=order).exists():
            raise serializers.ValidationError(
                "This order already has a payment."
            )

        return order

    def create(self, validated_data):
        request = self.context["request"]
        order = validated_data["order"]

        payment = Payment.objects.create(
            user=request.user,
            order=order,
            method=validated_data["method"],
            amount=order.total_amount,
            status="pending",
        )

        return payment
    
# view payments
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "method",
            "amount",
            "transaction_id",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

# allow admin to update status
class AdminPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"