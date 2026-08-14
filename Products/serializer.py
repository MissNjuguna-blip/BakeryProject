from rest_framework import serializers
from Center.models import Favorite, Product

# views products
class ProductSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "image",
            "category",
            "available",
            "is_favorite",
        ]

    def get_is_favorite(self, obj):
        request = self.context.get("request")

        if not request or request.user.is_anonymous:
            return False

        try:
            customer = request.user.customer_profile
        except:
            return False

        return Favorite.objects.filter(
            customer=customer,
            product=obj
        ).exists()