from django.forms import Form
from django import forms
import re
from django.forms import ValidationError ,EmailField
from django.forms import ModelForm
from user.models import UserProfile
from captcha.fields import CaptchaField

class UserRegisterForm(Form):
    # 继承From需要自己定义比较灵活
    username=forms.CharField(max_length=50,min_length=6,required=True,error_messages={'min_length':'至少填写6位',},label='用户名')
    email=forms.EmailField(required=True,error_messages={'required':'必须填写邮箱'},label='邮箱')
    mobile=forms.CharField(required=True,error_messages={'required':'必须填写手机号码'},label='手机号')
    password=forms.CharField(required=True,error_messages={'required':'必须填写密码'},label='密码',widget=forms.widgets.PasswordInput)
    repassword=forms.CharField(required=True,error_messages={'required':'必须填写确认密码'},label='密码',widget=forms.widgets.PasswordInput)
    
    def clean_username(self):
        username=self.cleaned_data.get('username')
        result=re.match(r'[a-zA-Z]\w{5,}',username)
        if not result:
            raise ValidationError('用户名必须字母开头')
        else:
            return username

class RegisterForm(ModelForm):
    # 继承ModelFrom是跟模型关联起来，不用再自己一个一个定义
    # repassword=forms.CharField(required=True,error_messages={'required':'必须填写确认密码'},label='密码',widget=forms.widgets.PasswordInput)
    class Meta:
        model=UserProfile
        fields=['username','email','mobile','password']
    
    # def clean_username(self):
    #     username=self.cleaned_data.get('username')
    #     result=re.match(r'[a-zA-Z]\w{5,}',username)
    #     if not result:
    #         raise ValidationError('用户名必须字母开头')
    #     else:
    #         return username

class LoginForm(Form):
    username=forms.CharField(max_length=50,min_length=6,required=True,error_messages={'min_length':'至少填写6位',},label='用户名')
    password=forms.CharField(required=True,error_messages={'required':'必须填写密码'},label='密码',widget=forms.widgets.PasswordInput)
    class Meta:
        model=UserProfile
        fields=['username','password']
    
    def clean_username(self):
        username=self.cleaned_data.get('username')
        if not UserProfile.objects.filter(username=username).exists():
            raise  ValidationError('用户不存在')
        return username


class CaptchaTestForm(forms.Form):
    email = EmailField(required=True,error_messages={'required':'必须填写邮箱'},label='邮箱')
    captcha = CaptchaField()

