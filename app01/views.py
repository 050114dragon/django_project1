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
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication
# Create your views here.
import csv
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
import time
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponseBadRequest
from django.contrib.sessions.backends.db import SessionStore
import random
from io import BytesIO


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
from .models import Article
from serializer import ArticleSerialize
from serializer import UserRegisterSerializer


class MyDefaultPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 50
    page_query_param = "page"
    page_size_query_param = "page_size"

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
        
        
class ArticleListMixin(GenericAPIView,ListModelMixin):
    """
    GenericAPIView和ModelMixin适合搭配使用，
    GenericAPIView负责query,serializer,pagination,filter等
    ModelMixin负责业务逻辑，响应等
    需要自定义get，post等方法,apiview的dispatch方法根据request的请求方法调用get,post等方法
    get,post等方法中调用ModelMixin中的list,create等方法，最终返回response
    请求失败时返回的字典中含有detail字段，提示失败原因
    """
    serializer_class = ArticleSerialize
    queryset = Article.objects.all()
    pagination_class = MyDefaultPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = "__all__" #对指定字段进行过滤，比如?name=
    # filter_backends = [filters.SearchFilter]
    # # filter_backends = [filters.SearchFilter] #对指定字段进行全局搜索，比如?search=
    # filter_backends = [filters.OrderingFilter,filters.SearchFilter]  #依据指定字段进行排序，如ordering=-name,author
    # ordering_fields = "__all__"
    #ordering = ['username'] #指定默认排序的一个或者多个字段
    filter_backends = [filters.OrderingFilter,filters.SearchFilter] #同时进行搜索和排序
    search_fields = ["name","author","text"]
    ordering_fields = "__all__"
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
class ArticleListGenericAPIView(GenericAPIView):
    """
    测试仅GenericAPIView是否能够进行分页等
    """
    serializer_class = ArticleSerialize
    queryset = Article.objects.all()
    pagination_class = MyDefaultPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = "__all__" #对指定字段进行过滤，比如?name=
    # filter_backends = [filters.SearchFilter]
    # # filter_backends = [filters.SearchFilter] #对指定字段进行全局搜索，比如?search=
    # filter_backends = [filters.OrderingFilter,filters.SearchFilter]  #依据指定字段进行排序，如ordering=-name,author
    # ordering_fields = "__all__"
    #ordering = ['username'] #指定默认排序的一个或者多个字段
    filter_backends = [filters.OrderingFilter,filters.SearchFilter] #同时进行搜索和排序
    search_fields = ["name","author","text"]
    ordering_fields = "__all__"
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)  #如果未设置分页，则返回None，如果正确分页，则返回page，否则返回错误response
        #分页
        if page is not None: 
            serializer = self.get_serializer(page, many=True)            
            return self.get_paginated_response(serializer.data)    
        #未分页
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)     

class ArticleCreate(GenericAPIView,CreateModelMixin):
    """
    新增一个实例，新增失败时，返回字典的键可能含有失败的字段，提示该字段失败的原因
    """
    questset = Article.objects.all()
    serializer_class = ArticleSerialize
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)



class UserRegisterAPIView(APIView):
    """
    用户注册功能
    """
    authentication_classes = []       #任何人均可注册，需去除token验证
    #permission_classes = [IsAdminUser] #设置仅管理员能够进行用户注册
    def post(self,request):    
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"messgae":"注册成功","status":200})
        else:
            return Response(data={"messgae":"注册失败","status":400})


class CaptchaAPIView(APIView):
    """
    生成图片验证码
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    def get(self, request):
        # 生成四位随机验证码
        length=int(request.GET.get('length',4))
        captcha = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))
        # 创建图片对象，设置字体和字体大小
        img = Image.new('RGB', (150, 50), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 35)
        # 在图片上绘制验证码
        draw.text((10, 10), captcha, font=font, fill=(random.randint(0,150), random.randint(0,255), random.randint(0,255)))
        # 绘制干扰线
        for _ in range(10):
            x1 = random.randint(0, 150)
            y1 = random.randint(0, 50)
            x2 = random.randint(0, 150)
            y2 = random.randint(0, 50)
            draw.line((x1, y1, x2, y2), fill=(0, 0, 0))
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        # 把验证码存储在session中，以便后续验证
        request.session['captcha'] = captcha
        request.session.set_expiry(1200)
        print("hello",captcha)
        data = buffer.getvalue()
        # 输出图片
        response = HttpResponse(data,content_type="image/png")
        return response 

class VerifyCaptchaAPIView(APIView):
    """
    对图片验证码进行验证
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        expected_captcha = request.session.get('captcha')
        received_captcha = request.data.get('captcha')
        if not expected_captcha or not received_captcha or expected_captcha.lower() != received_captcha.lower():
            return Response("验证码错误")
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
               