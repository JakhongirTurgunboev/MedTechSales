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
        fields = ['id', 'name', 'quantity', 'price']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['client', 'employee', 'products', 'date', 'price']

    def create(self, validated_data):
        product_ids = validated_data.pop('products', [])
        price = 0
        for product_id in product_ids:
            product = Product.objects.get(pk=product_id)
            price += product.price
        order = Order.objects.create(**validated_data, price=price)

        for product_id in product_ids:
            product = Product.objects.get(pk=product_id)

            OrderProduct.objects.create(order=order, product=product, quantity=1)

        return order


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

