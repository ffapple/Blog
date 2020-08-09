from django.shortcuts import render,HttpResponse,redirect,reverse
from user.forms import UserRegisterForm,RegisterForm,LoginForm
from .models import UserProfile
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

def index(request):
    return render(request,'index.html')

# 用户注册
def register(request):
    if request.method=='GET':
        return render(request,'user/register.html')
    else:
        rform=RegisterForm(request.POST) #使用form获取数据
        print('111111111')
        if rform.is_valid():#进行数据校验
            # 从干净的数据中取值
            print('222222222')
            username=rform.cleaned_data.get('username')
            email=rform.cleaned_data.get('email')
            mobile=rform.cleaned_data.get('mobile')
            password=rform.cleaned_data.get('password')
            print('密码为：' +password)
            if not UserProfile.objects.filter(Q(username=username)|Q(mobile=mobile)).exists():
                # 因为用户名手机号唯一，若数据库中不存在注册的用户名与手机号，则注册到数据库表中
                # 对密码进行加密
                password=make_password(password)
                print('加密后的密码为:'+password)
                # 将表单的值添加到数据库中
                user=UserProfile.objects.create(username=username,password=password,email=email,mobile=mobile)
                return HttpResponse('注册成功，并添加到数据库中啦')
            else:
                return render(request,'user/register.html',context={'msg':'已存在该用户名和手机号'})
            
        return render(request,'user/register.html',context={'msg':'请重新输入'})


# 用户登录
def login(request):
    if request.method=='GET':
        return render(request,'user/login.html')
    else:
        lform=LoginForm(request.POST)
        print('1111111')
        if lform.is_valid():
            print('2222222222')
            username=lform.cleaned_data.get('username')
            password=lform.cleaned_data.get('password')
            user=UserProfile.objects.filter(username=username).first()
            flag=check_password(password,user.password)
            if flag:
                request.session['username']=username
                # 用户登录成功跳转到首页
                return redirect(reverse('user:index'))
        return render(request,'user/login.html',context={'errors':lform.errors})

# 用户注销
def logout(request):
    # request.session.clear()#删除字典
    request.session.flush() #删除django_session+cookie+字典
    return redirect(reverse('user:index'))




def zhuce(request):
    if request.method=='GET':
        rform=RegisterForm()
        return render(request,'user/zhuce.html',context={'rform':rform})
    else:
        rform=RegisterForm(request.POST)
        # 验证表单提交的数据是否合法
        if rform.is_valid():
            print(rform.cleaned_data)
            username=rform.cleaned_data.get('username')
            email=rform.cleaned_data.get('email')
            mobile=rform.cleaned_data.get('mobile')
            password=rform.cleaned_data.get('password')

            # 将数据添加到数据库中
            return HttpResponse('SUCCESS')

