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
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
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
         


def get_tokens_for_user(user):
       refresh = RefreshToken.for_user(user)
       return {
              "username": user.username,
              "refresh": str(refresh),
              "access": str(refresh.access_token)
              }

from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from serializer import LoginSerializer
from django.contrib.auth import authenticate
class LoginAPIView(APIView):
    """This api will handle login and generate access and refresh token for authenticate user."""
    """
        登录接口
    """
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