from django.urls import path, include, re_path
from . import views


app_name='article'
urlpatterns = [
   path('',views.index,name='index'),
   path('detail/',views.detail,name='detail'),
   path('show/',views.show,name='show'),
   path('write/',views.write,name='write'),
   path('comment/',views.comment,name='comment'),
   path('message/',views.message,name='message')

  
]