from django.db import models
from django.contrib.auth.models import User
from django import forms
import time
# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=20,blank=True)
    age = models.IntegerField()
    def __str__(self):
        return self.name
    
class Imagetest(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to="upload/")
    def __str__(self):
        return self.name
    
class Password(models.Model):
    """
    用于验证两次密码是否一致
    """
    name = models.CharField(max_length=20)
    password_1 = models.CharField(max_length=20)
    password_2 = models.CharField(max_length=20)
    def __str__(self):
        return self.name


class Notes(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    price = models.IntegerField(blank=True,null=True)
    user = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            name = "user")

class Company(models.Model):
    """
    外键序列化测试model
    """
    name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.name
        
    
class Employee(models.Model):
    """
    外键序列化测试model
    """
    name = models.CharField(max_length=50)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)


class Toy(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Baby(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    toy = models.ManyToManyField(to="Toy",related_name="baby",db_constraint=False)
    def __str__(self):
        return self.name
    
class Article(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    text = models.CharField(max_length=500)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
