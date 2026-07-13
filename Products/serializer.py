from rest_framework import serializers
from Center.models import Product

# views products
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"