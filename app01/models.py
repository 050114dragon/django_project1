from django.db import models

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
      

