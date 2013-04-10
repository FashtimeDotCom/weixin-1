from django.db import models

# Create your models here.


class UserInfo(models.Model):
    id_wx = models.CharField(max_length = 20)
    id_ykt = models.CharField(max_length = 20, null=True)
    id_xh = models.CharField(max_length = 20, null=True)
    pwd_tyx = models.CharField(max_length = 30 , null=True)
    pwd_tsg = models.CharField(max_length = 30, null = True)


class KB(models.Model):
    id_wx = models.CharField(max_length=100)
    course_1 = models.CharField(max_length=200,null=True)
    course_2 = models.CharField(max_length=200,null=True)
    course_3 = models.CharField(max_length=200,null=True)
    course_4 = models.CharField(max_length=200,null=True)
    course_5 = models.CharField(max_length=200,null=True)
    course_6 = models.CharField(max_length=200,null=True)    
    course_7 = models.CharField(max_length=200,null=True)
    course_8 = models.CharField(max_length=200,null=True)    
    course_9 = models.CharField(max_length=200,null=True)    
    course_10 = models.CharField(max_length=200,null=True)    
    course_11 = models.CharField(max_length=200,null=True)    
    course_12 = models.CharField(max_length=200,null=True)
    course_13 = models.CharField(max_length=200,null=True)
    course_14 = models.CharField(max_length=200,null=True)
    course_15 = models.CharField(max_length=200,null=True)
    course_16 = models.CharField(max_length=200,null=True)
    course_17 = models.CharField(max_length=200,null=True)
    course_18 = models.CharField(max_length=200,null=True)
    
    
    
    