from . import views

from django.urls import path

app_name='user'
urlpatterns = [
    path('', views.index,name='index'),
    path('register',views.register,name='register'),
    path('user_login',views.user_login,name='user_login'),
    path('logout',views.logout,name='logout'),
    path('codelogin',views.code_login,name='codelogin'),
    path('sendcode',views.send_code,name='send_code'),
    path('forget_pwd',views.forget_pwd,name='forget_pwd'),
    path('valide_code',views.valide_code,name='valide_code'),
    path('update_pwd',views.update_pwd,name='update_pwd'),
    path('center',views.center,name='center'),
    path('center1',views.center1,name='center1'),
    path('zhuce',views.zhuce,name='zhuce')

]
