from django.db import models

# Create your models here.


class UserInfo(models.Model):
    id_wx = models.CharField(max_length = 20)
    id_ykt = models.CharField(max_length = 20, null=True)
    id_xh = models.CharField(max_length = 20, null=True)
    pwd_tyx = models.CharField(max_length = 30 , null=True)
    pwd_tsg = models.CharField(max_length = 30, null = True)



