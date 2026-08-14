from rest_framework import serializers
from Center.models import Order
from Center.models import Payment


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["order", "method"]

    def validate_order(self, order):
        request = self.context["request"]

        # Make sure the order belongs to the logged-in user
        if order.customer.user != request.user:
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


class AdminPaymentSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_email = serializers.SerializerMethodField()
    order_total = serializers.SerializerMethodField()
    order_status = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "customer_name",
            "customer_email",
            "order_total",
            "order_status",
            "method",
            "amount",
            "transaction_id",
            "checkout_request_id",
            "merchant_request_id",
            "result_desc",
            "status",
            "paid_at",
            "created_at",
            "updated_at",
        ]

    def get_customer_name(self, obj):
        try:
            user = obj.order.customer.user
            return user.get_full_name() or user.username
        except AttributeError:
            return "Unknown customer"

    def get_customer_email(self, obj):
        try:
            return obj.order.customer.user.email
        except AttributeError:
            return ""

    def get_order_total(self, obj):
        return obj.order.total_amount

    def get_order_status(self, obj):
        return obj.order.status