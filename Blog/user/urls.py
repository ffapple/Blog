from . import views

from django.urls import path

app_name='user'
urlpatterns = [
    path('', views.index,name='index'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('zhuce',views.zhuce,name='zhuce')

]
