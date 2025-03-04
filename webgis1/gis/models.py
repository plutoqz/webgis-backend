from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager,AbstractUser
# Create your models here.
from django.contrib.gis.db import models

class GisFeature(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    geom = models.GeometryField()  # 使用 PostGIS 几何字段
    properties = models.JSONField()
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class webgisUser(AbstractBaseUser):
    objects = UserManager()

    username = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False)
    password=models.CharField(max_length=20, blank=True, null=True)
    #confirm_password=models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'email'  # 用 email 作为登录标识
    REQUIRED_FIELDS = ['username']  # 必填字段（createsuperuser 时会提示）

    class Meta:
        #app_label = 'gis'  # 替换为你的应用名称
        db_table = 'gis_webgisuser'  # 如果需要自定义表名

    def __str__(self):
        return self.username



class User(AbstractUser):
    email = models.EmailField(unique=True)
    # 可添加其他自定义字段
    
    def __str__(self):
        return self.username
    