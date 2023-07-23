from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from rest_framework.decorators import api_view
from django.http.response import  JsonResponse
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
# Create your views here.
import csv
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
# from rest_framework import request


from .models import Student
from .models import Imagetest
from .models import Password
from serializer import StudentSerializer
from serializer import ImagetestSerializer
from rest_framework import status
from serializer import LoginSerializer
from serializer import PasswordSerializer
from .models import Notes
from django.views.generic import CreateView
from rest_framework.serializers import ListSerializer
from serializer import NotesPostSerializer
from serializer import NotesGetSerializer
from serializer import EmployeeSerializer
from serializer import BabySerializer
from .models import Baby
from .models import Toy




class StudentPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 50
    page_query_param = "page"
    page_size_query_param = "page_size"
        
@api_view(["GET"])
@permission_classes([IsAuthenticated])
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
         


def get_tokens_for_user(user):
       refresh = RefreshToken.for_user(user)
       return {
              "username": user.username,
              "refresh": str(refresh),
              "access": str(refresh.access_token)
              }

class LoginAPIView(APIView):
    """This api will handle login and generate access and refresh token for authenticate user."""
    """
        登录接口
    """
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
                username = serializer.validated_data["username"]
                password = serializer.validated_data["password"]
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    res_data = get_tokens_for_user(User.objects.get(username=username))
                    response = {
                            "status": status.HTTP_200_OK,
                            "message": "success",
                            "data": res_data
                            }
                    return Response(response, status = status.HTTP_200_OK)
                else :
                    response = {
                            "status": status.HTTP_401_UNAUTHORIZED,
                            "message": "Invalid Email or Password",
                            }
                    return Response(response, status = status.HTTP_401_UNAUTHORIZED)
        response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "data": serializer.errors
                }
        return Response(response, status = status.HTTP_400_BAD_REQUEST)   

class PasswordMixinView(ListModelMixin,CreateModelMixin,GenericAPIView):
    queryset = Password.objects.all()
    serializer_class = PasswordSerializer
    def get(self, request):
        return self.list(request)
    def post(self,request):
        self.create(request)
        return Response(data={"message":"success","status":200},status=200)
    
@api_view(["POST"])
def import_csv(request):
    csv_file = request.FILES['csv_file']
    print(csv_file)
    decoded_file = csv_file.read().decode('utf-8').splitlines()
    print(decoded_file)
    reader = list(csv.DictReader(decoded_file))
    serializer = StudentSerializer(data=reader, many=True) # create a new serializer instance with the data from the CSV file
    if serializer.is_valid(): # validate the data using the serializer
        serializer.save() # save the validated data to the database using the serializer
        return Response(serializer.data, status=status.HTTP_201_CREATED) # return a JSON response with the saved data and HTTP status code 201 Created
    else: # handle any validation errors that occurred during validation/saving process
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # return an error response with the validation error messages and HTTP status code 400 Bad Request 


class NotesAPIview(APIView):
    """
    get和post使用不同的序列化器,
    get可以返回在数据库不存在的衍生字段
    post可以设置外键的值
    """
    permission_classes=[IsAuthenticated,]
    def get(self, request, format=None):
        notes = Notes.objects.filter(user=request.user.id)
        serializer = NotesGetSerializer(notes, many=True)
        return Response(data={"data":serializer.data,"message": "success","status":200},status=status.HTTP_200_OK)
    def post(self, request, format=None):
        serializer = NotesPostSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            serializer.save(user=User.objects.get(username=self.request.user))
            # user这样的外键的值可以通过user=objects.get(username=self.request.user)这样获取，外键的取值必须是一个user对象
            # 序列化时外键不包含在fields中
            # 其他普通字段如果不在request.data中，也可能通过其他方式设置，比如creater=User.objects.get(username=self.request.user).username
            # 序列化时其他普通字段需要在fields中
            return Response(data={"data":serializer.data,"message": "success","status":201},status=status.HTTP_201_CREATED)
        return Response(data={"data":serializer.errors,"message": "success","status":201},status=status.HTTP_201_CREATED)
    
class EmployeeView(APIView):
    def post(self,request,format=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"data":serializer.data,"message": "success","status":201},status=status.HTTP_201_CREATED)
        else:
            return Response(data={"data":serializer.errors,"message": "failed","status":400})
        
        
class BabyView(APIView):
    def post(self,request,format=None):
        serializer = BabySerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"data":serializer.data,"message": "success","status":201},status=status.HTTP_201_CREATED)
        else:
            return Response(data={"data":serializer.errors,"message": "failed","status":400},status=status.HTTP_201_CREATED)        