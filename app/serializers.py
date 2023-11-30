# serializers.py
from rest_framework import serializers
from .models import Employee, Client, Product, OrderProduct, Order

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class EmployeeStatisticsSerializer(serializers.Serializer):
    employee_name = serializers.CharField()
    number_of_clients = serializers.IntegerField()
    number_of_products = serializers.IntegerField()
    sum_of_sales = serializers.DecimalField(max_digits=15, decimal_places=2)


class EmployeeStatisticsSummarySerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    full_name = serializers.CharField()
    number_of_clients = serializers.IntegerField()
    number_of_products = serializers.IntegerField()
    sum_of_sales = serializers.DecimalField(max_digits=10, decimal_places=2)


class ClientStatisticsSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()
    full_name = serializers.CharField()
    number_of_products_bought = serializers.IntegerField()
    amount_of_products = serializers.DecimalField(max_digits=10, decimal_places=2)

