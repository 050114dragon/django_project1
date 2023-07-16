from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .models import Imagetest
from serializer import StudentSerializer
from serializer import ImagetestSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class StudentPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 50
    page_query_param = "page"
    page_size_query_param = "page_size"

def index(request):
    return HttpResponse("hello app01 index!")


class StudentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()    
    serializer_class = StudentSerializer

class ImagetestViewSet(ModelViewSet):
    queryset = Imagetest.objects.all()    
    serializer_class = ImagetestSerializer
    
    
class StudentPaginationViewSet(ModelViewSet):
    """
    增加分页功能
    """
    queryset = Student.objects.all()    
    serializer_class = StudentSerializer
    pagination_class = StudentPagination
         



