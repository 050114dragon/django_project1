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
# Create your views here.

def index(request):
    return HttpResponse("hello app01 index!")


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()    
    serializer_class = StudentSerializer

class ImagetestViewSet(ModelViewSet):
    queryset = Imagetest.objects.all()    
    serializer_class = ImagetestSerializer
    
    

        



