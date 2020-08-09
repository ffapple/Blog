from django.shortcuts import render,HttpResponse,redirect,reverse
from django.http import JsonResponse
from .models import Articel,Tag,Comment,Message
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    farticles=Articel.objects.order_by('-click_num')
    darticles=Articel.objects.order_by('-date')[:8]
    print(farticles,darticles)
   
    return render(request,'index.html',context={'figure_articles':farticles,'darticles':darticles})

def detail(request):
    id=request.GET.get('id')
    article=Articel.objects.get(pk=id)
    article.click_num+=1
    article.save()
    article_list_about=[]
    # 与这个标签相关得所有文章(反向查询)
    a_tags=article.tags.all() 
    print(a_tags)
    for t in a_tags:
        print(t.articel_set.all())
        for a in t.articel_set.all():
            if a not in article_list_about and len(article_list_about)<6:
                article_list_about.append(a)
    print('0000000000')
    print(article_list_about)
    # 查询评论数
    comments=Comment.objects.filter(article=id)

    return render(request,'article/info.html',context={'article':article,'article_list_about':article_list_about,'comments':comments})


# 学无止境
def show(request):
    tags=Tag.objects.all()[:6]
    tid=request.GET.get('tid','')
    if tid:
        tag=Tag.objects.get(pk=tid)
        articles=tag.articel_set.all()
        print(articles)
    else:
        articles=Articel.objects.all()


    # 分页器
    paginator=Paginator(articles,2) #对象列表，每页显示几条数据
    # 方法get_page()
    page=request.GET.get('page',1)
    page=paginator.get_page(page)
    print(page.paginator.num_pages)

    return render(request,'article/show.html',context={'tags':tags,'page':page,'tid':tid})

from article.forms import ArticleForm,MessageForm
def write(request):
    if request.method=='GET':
        aform=ArticleForm()
        return render(request,'article/write.html',context={'form':aform})
    else:
        aform=ArticleForm(request.POST)
        if aform.is_valid():
            print('成功6666')
            data=aform.cleaned_data
            article=Articel()
            article.title=data.get('title')
            article.desc=data.get('desc')
            article.content=data.get('content')
            # article.date=data.get('date')
            # article.click_num=data.get('click_num')
            # article.love_num=data.get('love_num')
            article.image=data.get('image')
            article.user=data.get('user')
            article.save()
            # tags是多对多得属性，在保存之后写
            article.tags.set(data.get('tags'))
            return redirect(reverse('article:index'))
        else:
            print('失败5555')
        return HttpResponse('aaaaa')

# 评论不是通过表单获取数据，而是js
def comment(request):
    nickname=request.GET.get('nickname')
    saytext=request.GET.get('saytext')
    aid=request.GET.get('aid')

    comment=Comment.objects.create(nickname=nickname,content=saytext,article_id=aid)

    if comment:
        data={'status':1}
    else:
        data={'status':0}
    return JsonResponse(data)


def message(request):
    messages=Message.objects.all()
    if request.method=='GET':
        
        form=MessageForm()
        print(form)
        return render(request,'article/message.html',context={'messages':messages,'form':form})
    else:
        nickname=request.POST.get('nickname')
        content=request.POST.get('content')
        icon=request.POST.get('icon')
        print(nickname,content)
        message=Message()
        message.nickname=nickname
        message.content=content
        message.icon=icon
        message.save()
        form=MessageForm()
        return render(request,'article/message.html',context={'messages':messages,'form':form})

