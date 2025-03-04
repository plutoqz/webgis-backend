from rest_framework import serializers
from .models import GisFeature
from .models import webgisUser
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()


class GisFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = GisFeature
        fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password = serializers.CharField(write_only=True)  # 密码字段只写
    confirm_password = serializers.CharField(write_only=True)  # 确认密码字段只写

    class Meta:
        model = webgisUser
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        """
        验证密码和确认密码是否一致
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("两次输入的密码不一致")
        return data

    def create(self, validated_data):
        """
        创建用户
        """
        # 移除 confirm_password 字段
        validated_data.pop('confirm_password')
        # 创建用户
        user = webgisUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            #confirm_password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    用户登录序列化器
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        验证用户登录信息
        """
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("用户账号未激活")
                data['user'] = user
            else:
                raise serializers.ValidationError("用户名或密码错误")
        else:
            raise serializers.ValidationError("必须提供用户名和密码")
        return data
    

#注册
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
#登录
class UserSerializerlogin(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")