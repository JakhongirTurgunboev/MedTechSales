from django.db import models
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from .models import Employee, Client, Product, Order, OrderProduct
from .serializers import (
    EmployeeSerializer,
    ClientSerializer,
    ProductSerializer,
    OrderSerializer,
    EmployeeStatisticsSummarySerializer, ClientStatisticsSerializer, OrderProductSerializer
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


class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class EmployeeStatisticsViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'month',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Month parameter',
                required=False,
            ),
            openapi.Parameter(
                'year',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Year parameter',
                required=False,
            ),
        ],
    )
    def list(self, request, id, *args, **kwargs):
        # Get the employee
        try:
            employee = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the month and year from the query parameters
        month, year = None, None
        if request.query_params.get('month'):
            month = request.query_params.get('month')
        if request.query_params.get('year'):
            year = request.query_params.get('year')

        if month and year:
            orders = Order.objects.filter(employee=employee, date__month=month, date__year=year)
        elif month:
            orders = Order.objects.filter(employee=employee, date__month=month)
        elif year:
            orders = Order.objects.filter(employee=employee, date__year=year)
        else:
            orders = Order.objects.filter(employee=employee)

        # Calculate statistics
        number_of_clients = orders.values('client').distinct().count()
        counter = 0
        total_price = 0
        for order in orders:
            order_product = OrderProduct.objects.filter(order_id=order.id)
            total_price += sum(op.product.price for op in order_product)
            counter += order_product.count()

        # Serialize the data
        serializer = EmployeeStatisticsSerializer({
            'employee_name': employee.full_name,
            'number_of_clients': number_of_clients,
            'number_of_products': counter,
            'sum_of_sales': total_price,
        })

        return Response(serializer.data)


class EmployeeStatisticsSummaryViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'month',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Month parameter',
                required=False,
            ),
            openapi.Parameter(
                'year',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Year parameter',
                required=False,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        # Get the month and year from the query parameters
        month, year = None, None
        if request.query_params.get('month'):
            month = request.query_params.get('month')
        if request.query_params.get('year'):
            year = request.query_params.get('year')

        if month and year:
            orders = Order.objects.filter(date__month=month, date__year=year)
        elif month:
            orders = Order.objects.filter(date__month=month)
        elif year:
            orders = Order.objects.filter(date__year=year)
        else:
            orders = Order.objects.all()

        # Calculate statistics
        employee_statistics = (
            orders.values('employee')
            .annotate(
                employee_id=F('employee__id'),
                full_name=F('employee__full_name'),
                number_of_clients=Count('client', distinct=True),
                number_of_products=Count('orderproduct', distinct=True),
                sum_of_sales=Sum('orderproduct__product__price')
            )
        )

        # Serialize the data
        serializer = EmployeeStatisticsSummarySerializer(employee_statistics, many=True)

        return Response(serializer.data)


class ClientStatisticsViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'month',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Month parameter',
                required=False,
            ),
            openapi.Parameter(
                'year',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Year parameter',
                required=False,
            ),
        ],
    )
    def list(self, request, id, *args, **kwargs):
        # Get the client
        try:
            client = Client.objects.get(id=id)
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the month and year from the query parameters
        month, year = None, None
        if request.query_params.get('month'):
            month = request.query_params.get('month')
        if request.query_params.get('year'):
            year = request.query_params.get('year')

        if month and year:
            number_of_products_bought = Order.objects.filter(client_id=id, date__month=month, date__year=year)
        elif month:
            number_of_products_bought = Order.objects.filter(client_id=id, date__month=month)
        elif year:
            number_of_products_bought = Order.objects.filter(client_id=id, date__year=year)
        else:
            number_of_products_bought = Order.objects.filter(client_id=id)
        # Calculate statistics

        counter = 0
        total_price = 0
        for order in number_of_products_bought:
            order_product = OrderProduct.objects.filter(order_id=order.id)
            total_price += sum(op.product.price for op in order_product)
            counter += order_product.count()

        # Serialize the data
        serializer = ClientStatisticsSerializer({
            'client_id': client.id,
            'full_name': client.full_name,
            'number_of_products_bought': counter,
            'amount_of_products': total_price,
        })

        return Response(serializer.data)
