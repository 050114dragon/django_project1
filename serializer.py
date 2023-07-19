from rest_framework import serializers
from app01.models import Student
from app01.models import Imagetest
from app01.models import Password
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import validators
from app01.models import Notes


class StudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=10,validators=[validators.UniqueValidator(queryset=Student.objects.all())])
    age = serializers.IntegerField(min_value=0,max_value=100)
    class Meta:
        model = Student
        fields = ["id","name","age"]
        
class ImagetestSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=20)
    image = serializers.ImageField(use_url=False)
    class Meta:
        model = Imagetest
        fields = ["id","name","image"]
        
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
            model = User
            fields = ['username','password']
            
class PasswordSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    password_1 = serializers.CharField()
    password_2 = serializers.CharField()
    class Meta:
        model = Password
        fields = ["name","password_1","password_2"]
    def validate_password_1(self,value):
        if value != self.initial_data['password_2']:
            raise serializers.ValidationError(
                'Passwords do not match'
            )
        else:
            return value
        
               
class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ["title","text","user"]     
            
