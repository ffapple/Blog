import requests
from time import time 
import hashlib
import json
from django.core.mail import send_mail
from .models import UserProfile
import uuid,os
from Blog.settings import EMAIL_HOST_USER
from qiniu import Auth, put_file, put_data

from Blog.settings import EMAIL_HOST_USER, MEDIA_ROOT

def util_sendmsg(mobile):
    url='https://api.netease.im/sms/sendcode.action'
    data={'mobile':mobile}
    # 以下参数需要放在Http Request Header中 AppKey,Nonce,CurTime,CheckSum
    AppKey='d851cbbc5d67445f80a174417d67afde'
    Nonce='assdefeije'
    CurTime=str(time())
    AppSecret='feab5bc2f74e'
    content=AppSecret+Nonce+CurTime
    CheckSum=hashlib.sha1(content.encode('utf-8')).hexdigest()
    headers={
        'AppKey':AppKey,
        'Nonce':Nonce,
        'CurTime':CurTime,
        'CheckSum':CheckSum
    }


    response=requests.post(url,data,headers=headers)
    # json
    str_result=response.text
    json_result=json.loads(str_result)
    return json_result

def send_email(email,request):
    subject = '个人博客找回密码'
    user = UserProfile.objects.filter(email=email).first()
    ran_code = uuid.uuid4()
    print(ran_code)
    print(type(ran_code))
    ran_code = str(ran_code)
    print(type(ran_code))
    ran_code =ran_code.replace('-','')
    request.session[ran_code] = user.id
    message='''
            亲爱的用户：
                    您好，此链接用于找回密码<a href='http://127.0.0.1:8000/update_pwd?c=%s'>更新密码</a>

    '''%(ran_code)
    result = send_mail(subject, "", EMAIL_HOST_USER, [email, ],html_message=message)
    return result

# 上传图片到七牛云
def upload_image(storeobj,imagepath):
    access_key = '1fXvG9wkbN7AgRUG6usHDcRP5Bb85apcovRAIITP'
    secret_key = 'Aqf1lPAmUG72EdZJ7PxKtWHfWDYNdUycZP1TaAIN'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'myblog'

    # 上传后保存的文件名
    key = storeobj.name

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    localfile = os.path.join(MEDIA_ROOT, imagepath)  # 本地图片
    ret, info = put_data(token, key, localfile )
    print('00000000000')
    print(ret, info)
    filename = ret.get('key')
    save_path = 'http://pr67kkhq9.bkt.clouddn.com/'+filename
    return save_path