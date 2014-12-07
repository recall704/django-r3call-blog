#coding:utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.template  import RequestContext

from .models import Post, Category, FriendLink





def index(request):
    context = RequestContext(request)
    posts = Post.objects.all()


    categories = Category.objects.all()
    links = FriendLink.objects.all()

    return render_to_response('blogapp/index.html',{
        'posts':posts,
        "categories": categories,
        'links':links,
    },context)


def post(request,pk,title=None):
    context = RequestContext(request)

    post = get_object_or_404(Post,pk=pk)

    categories = Category.objects.all()
    links = FriendLink.objects.all()

    return render_to_response('blogapp/post.html',{
        'post':post,
        "categories": categories,
        'links':links,
    },context)


def category(request, pk):
    context = RequestContext(request)

    try:
        cate = Category.objects.get(pk=pk)
    except Category.DoesNotExist:  ## 读取分类，如果不存在，则引发错误，并404
        raise Http404

    posts = cate.post_set.all() ## 获取分类下的所有文章
    links = FriendLink.objects.all()

    return render_to_response('blogapp/index.html',{
        "posts": posts,
        "is_category": True,
        "cate_name": cate.name,
        "categories": Category.objects.all(),
        'links':links,
    },context)