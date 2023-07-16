from rest_framework import serializers
from app01.models import Student
from app01.models import Imagetest
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import validators


# class StudentSerializer(serializers.Serializer):
#     name = serializers.CharField(allow_blank=True, max_length=20)
#     age = serializers.IntegerField(min_value=0,max_value=100)
    
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Student.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.age)
#         instance.age = validated_data.get('age', instance.age)
#         instance.save()
#         return instance

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
