from rest_framework import serializers

from Center.models import Deliverer,Order

# code starts here
class DelivererSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliverer
        fields = ['name','phone']

