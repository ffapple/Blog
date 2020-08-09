from django.shortcuts import render,HttpResponse,redirect,reverse
from user.forms import UserRegisterForm,RegisterForm,LoginForm,CaptchaTestForm
from .models import UserProfile
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from .utils import util_sendmsg,send_email,upload_image
from django.http import JsonResponse
from captcha.models import CaptchaStore
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
# from django.core.mail import send_mail
# Create your views here.
from article.models import Articel

def index(request):
    farticles=Articel.objects.order_by('-click_num')
    darticles=Articel.objects.order_by('-date')[:8]
    print(farticles,darticles)
   
    return render(request,'index.html',context={'figure_articles':farticles,'darticles':darticles})

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
def user_login(request):
    if request.method=='GET':
        return render(request,'user/login.html')
    else:
        lform=LoginForm(request.POST)
        print('1111111')
        if lform.is_valid():
            username = lform.cleaned_data.get('username')
            password = lform.cleaned_data.get('password')
            # 进行数据库的查询
            # user = UserProfile.objects.filter(username=username).first()
            # flag = check_password(password, user.password)
            # if flag:
            #     # 保存session信息
            #     request.session['username'] = username

            # 方式二前提是继承了AbstractUser
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)  # 将用户对象保存在底层的request中  （session）

                return redirect(reverse('user:index'))
        return render(request, 'user/login.html', context={'errors': lform.errors})

# 用户注销
def logout(request):
    # request.session.clear()  # 删除字典
    request.session.flush()  # 删除django_session + cookie +字典
    # logout(request)

    return redirect(reverse('user:index'))


# 手机验证码登录
def code_login(request):
    if request.method=='GET':
        return render(request,'user/codelogin.html')
    else:
        mobile=request.POST.get('mobile')
        code=request.POST.get('code')

        # 根据mobile去session中取值
        check_code=request.session.get('mobile')
        if code==check_code:
            user=UserProfile.objects.filter(mobile=mobile).first()
            print(user)
            if user:
                request.session['username']=user.username
                return redirect(reverse('user:index'))
        else:
            return render(request,'user/codelogin.html',context={'msg':'验证码有误'})




# 发送验证码，ajax发过来的请求
def send_code(request):
    mobile=request.GET.get('mobile')
    # 由第三方发送验证码
    json_result=util_sendmsg(mobile)
    print("json_result:"+str(json_result))
    # 取值
    status=json_result.get('code')
    print('status'+str(status))
    data={}
    if status==200:
        print('ssssss')
        check_code=json_result.get('obj')
        # 使用session保存
        request.session['mobile']=check_code
        data['status']=200
        data['msg']='验证码发送成功'
    else:
        data['status']=500
        data['msg']='验证码发送失败'
    return JsonResponse(data)

# 更新密码
def update_pwd(request):
    if request.method=='GET':
        c=request.GET.get('c')
        return render(request,'user/update_pwd.html',context={'c':c})
    else:
        print('12121212121212')
        code=request.POST.get('code')
        print('code:'+str(code))
        uid=request.session.get(code)
        print('uid:'+str(uid))
        user=UserProfile.objects.get(pk=uid)
        print(user)
        pwd=request.POST.get('password')
        print(pwd)
        repwd=request.POST.get('repassword')
        print(repwd)
        if pwd==repwd and user:
            pwd=make_password(pwd)
            user.password=pwd
            user.save()
            return render(request,'user/update_pwd.html',context={'msg':'用户密码更新成功'})
        else:
            return render(request,'user/update_pwd.html',context={'msg':'更新失败'})




def valide_code(request):
    if request.is_ajax():
        key=request.GET.get('key')
        # 手动输入的验证码
        code=request.GET.get('code')
        captche=CaptchaStore.objects.filter(hashkey=key).first()
        if captche.response == code.lower():
            # 正确
            data = {'status': 1}
        else:
            # 错误的
            data = {'status': 0}
        return JsonResponse(data)

# 忘记密码
def forget_pwd(request):
    if request.method=='GET':
        form=CaptchaTestForm()
        return render(request,'user/forget_pwd.html',context={'form':form})
    else:
        # 获取提交的邮箱，发送邮件，通过发送的邮件链接设置新的密码
        email=request.POST.get('email')
        # 给此邮箱发送邮件
        result=send_email(email,request)
        return HttpResponse(result)


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


# 个人中心（修改用户信息）
# @login_required
def center(request):
    user=request.user
    if request.method=='GET':
        print(user)
        return render(request,'user/center.html',context={'user':user})
    else:
        username=request.POST.get('username')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        icon=request.FILES.get('icon')
        print('333333333')
        # print(icon)
        user.username=username
        user.email=email
        user.mobile=mobile
        user.icon=icon
        user.save()
        return render(request,'user/center.html',context={'user':user})

def center1(request):
    user=request.user
    if request.method=='GET':
        print(user)
        return render(request,'user/center1.html',context={'user':user})
    else:
        username=request.POST.get('username')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        icon=request.FILES.get('icon')
        print('333333333')
        # print(icon)
        user.username=username
        user.email=email
        user.mobile=mobile
        user.icon=icon
        user.save()
        save_path=upload_image(icon,str(user.icon))
        user.yunicon=save_path
        user.save()
       
        return render(request,'user/center.html',context={'user':user})