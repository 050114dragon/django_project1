from rest_framework import serializers
from app01.models import Student
from app01.models import Imagetest
from app01.models import Password
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import validators
from app01.models import Notes
from app01.models import Company
from app01.models import Employee
from app01.models import Baby
from app01.models import Toy


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
        
class NotesGetSerializer(serializers.ModelSerializer):
    creater = serializers.SerializerMethodField()
    class Meta:
        model = Notes
        fields = ["title","text","user","creater"]
    def get_creater(self,obj):
        return obj.user.username
               
class NotesPostSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    class Meta:
        model = Notes
        fields = ["title","text","price"]
    def get_price(self,obj):
        return len(obj.text) 
        

class EmployeeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50,
                                 validators=[validators.UniqueValidator(
                                     queryset=Employee.objects.all(),
                                     message="雇员名已存在")]
                                 )
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    class Meta:
        model = Employee
        fields = '__all__'
    def create(self, validated_data):
        company_obj = validated_data.pop('company')  #返回是外键对应model的实例
        # company = Company.objects.get(id=company_obj.id)  #company_obj在函数中的值为model实例或者model的_str__的返回值
        employee = Employee.objects.create(company=company_obj, **validated_data)  #返回值含有外键所在model的id或者__str__的返回值
        return employee
    #还可增加update方法


class BabySerializer(serializers.ModelSerializer):
    class Meta:
        model = Baby    
        fields = ["name","age","toy"]
    def validate_toy(self,value):
        """
        验证通过返回value，否则返回ValidationError
        """
        print("value",value)
        print(len(value))
        if len(value) < 2:
            raise validators.ValidationError("每个baby至少分配二个toy")
        return value    
    def validate(self, attrs):
        """
        attrs为request.data,如果验证通过，返回attrs，否则抛出ValidationError("baby和toys需联合唯一")
        """
        name = attrs.get("name")
        toys = attrs.get("toy") #返回含一个或者多个实例的列表
        for toy in toys:
            print("hello",toy,dir(toy))
            print("hello2",name,toy.id)
            if Baby.objects.filter(name=name,toy=toy.id):
                raise validators.ValidationError("baby和toys需联合唯一")
        return attrs

