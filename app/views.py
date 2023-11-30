from rest_framework import viewsets
from .models import Employee, Client, Product, Order, OrderProduct
from .serializers import (
    EmployeeSerializer,
    ClientSerializer,
    ProductSerializer,
    OrderSerializer,
    EmployeeStatisticsSummarySerializer, ClientStatisticsSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from .serializers import EmployeeStatisticsSerializer
from django.db.models import Sum, Count, F


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class EmployeeStatisticsViewSet(viewsets.ViewSet):
    def list(self, request, id, *args, **kwargs):
        # Get the employee
        try:
            employee = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the month and year from the query parameters
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        # Filter orders based on employee, month, and year
        orders = Order.objects.filter(employee=employee, date__month=month, date__year=year)

        # Calculate statistics
        number_of_clients = orders.values('client').distinct().count()
        number_of_products = OrderProduct.objects.filter(order__in=orders).count()
        sum_of_sales = orders.aggregate(total_sales=Sum('price'))['total_sales']

        # Serialize the data
        serializer = EmployeeStatisticsSerializer({
            'employee_name': employee.full_name,
            'number_of_clients': number_of_clients,
            'number_of_products': number_of_products,
            'sum_of_sales': sum_of_sales,
        })

        return Response(serializer.data)


class EmployeeStatisticsSummaryViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        # Get the month and year from the query parameters
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        # Filter orders based on month and year
        orders = Order.objects.filter(date__month=month, date__year=year)

        # Calculate statistics
        employee_statistics = (
            orders.values('employee')
            .annotate(
                employee_id=F('employee__id'),
                full_name=F('employee__full_name'),
                number_of_clients=Count('client', distinct=True),
                number_of_products=Count('orderproduct', distinct=True),
                sum_of_sales=Sum('price')
            )
        )

        # Serialize the data
        serializer = EmployeeStatisticsSummarySerializer(employee_statistics, many=True)

        return Response(serializer.data)


class ClientStatisticsViewSet(viewsets.ViewSet):
    def list(self, request, id, *args, **kwargs):
        # Get the client
        try:
            client = Client.objects.get(id=id)
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the month and year from the query parameters
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        # Filter orders based on client, month, and year
        orders = Order.objects.filter(client=client, date__month=month, date__year=year)

        # Calculate statistics
        number_of_products_bought = OrderProduct.objects.filter(order__in=orders).count()
        amount_of_products = orders.aggregate(amount=Sum('price'))['amount']

        # Serialize the data
        serializer = ClientStatisticsSerializer({
            'client_id': client.id,
            'full_name': client.full_name,
            'number_of_products_bought': number_of_products_bought,
            'amount_of_products': amount_of_products,
        })

        return Response(serializer.data)
