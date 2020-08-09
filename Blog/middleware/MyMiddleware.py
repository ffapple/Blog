from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


login_list = ['/center', ]


class MiddleWare1(MiddlewareMixin):
    # 重写方法
    def process_request(self,request):
        print('------------------->1')
        # print(request.META)
        path=request.path
        print('path:'+str(path))
        if path in login_list:
            print("user:"+str(request.user)) #request.user认为就是用户登录的对象
            if not request.user.is_authenticated:
                return redirect(reverse('user:user_login'))
    
    # def process_reponse(self,request,reponse):
    #     print("========================="+str(reponse))
    #     return reponse

