#coding:utf-8
import json

from django.shortcuts               import    render_to_response,render, get_object_or_404
from django.template                import    RequestContext
from django.contrib.auth.decorators import    login_required
from django.contrib                 import    messages
from django.core.urlresolvers       import    reverse
from django.http                    import    HttpResponseRedirect, HttpResponse

from markdown import markdown as md

from blogapp.models import      Post, Category, FriendLink
from blogapp.forms  import      PostForm
from tagging.models import      TaggedItem, Tag
from django.core.cache import   cache




def index(request):

    if not cache.has_key("posts"):
        posts = Post.objects.all()
        cache.set("posts",posts,timeout=120)
    else:
        posts = cache.get("posts")

    if not cache.has_key("categories"):
        categories = Category.objects.all()
        cache.set("categories",categories,timeout=120)
    else:
        categories = cache.get("categories")

    if not cache.has_key("links"):
        links = FriendLink.objects.all()
        cache.set("links",links,timeout=120)
    else:
        links = cache.get("links")

    if not cache.has_key("tags"):
        tags = Tag.objects.all()
        cache.set("tags",tags,timeout=120)
    else:
        tags = cache.get("tags")

    return render(request,'blogapp/index.html',{
        'posts':posts,
        "categories": categories,
        'links':links,
        'tags':tags,
        'index_active':'active',
    })


def post(request,pk,title=None):

    post = get_object_or_404(Post,pk=pk)

    if not cache.has_key("categories"):
        categories = Category.objects.all()
        cache.set("categories",categories)
    else:
        categories = cache.get("categories")

    if not cache.has_key("links"):
        links = FriendLink.objects.all()
        cache.set("links",links)
    else:
        links = cache.get("links")

    if not cache.has_key("tags"):
        tags = Tag.objects.all()
        cache.set("tags",tags)
    else:
        tags = cache.get("tags")

    return render(request,'blogapp/post.html',{
        'post':post,
        "categories": categories,
        'links':links,
        'tags':tags,
    })


def category(request, pk, name=None):
    cate = get_object_or_404(Category,pk=pk)

    posts = cate.post_set.all() ## 获取分类下的所有文章

    if not cache.has_key("categories"):
        categories = Category.objects.all()
        cache.set("categories",categories)
    else:
        categories = cache.get("categories")

    if not cache.has_key("links"):
        links = FriendLink.objects.all()
        cache.set("links",links)
    else:
        links = cache.get("links")

    if not cache.has_key("tags"):
        tags = Tag.objects.all()
        cache.set("tags",tags)
    else:
        tags = cache.get("tags")

    return render(request,'blogapp/index.html',{
        "posts": posts,
        "cate": cate,
        "is_category": True,
        "categories": categories,
        'links':links,
        'tags':tags,
    })


def about(request):

    if not cache.has_key("categories"):
        categories = Category.objects.all()
        cache.set("categories",categories)
    else:
        categories = cache.get("categories")

    if not cache.has_key("links"):
        links = FriendLink.objects.all()
        cache.set("links",links)
    else:
        links = cache.get("links")

    if not cache.has_key("tags"):
        tags = Tag.objects.all()
        cache.set("tags",tags)
    else:
        tags = cache.get("tags")

    return render(request,'blogapp/about.html',{
        'about_active':'active',
        "categories": categories,
        'links':links,
        'tags':tags,
    })


def tag(request,tag_id):

    t = get_object_or_404(Tag,id=tag_id)
    posts = TaggedItem.objects.get_by_model(Post,t)
    
    if not cache.has_key("categories"):
        categories = Category.objects.all()
        cache.set("categories",categories)
    else:
        categories = cache.get("categories")

    if not cache.has_key("links"):
        links = FriendLink.objects.all()
        cache.set("links",links)
    else:
        links = cache.get("links")

    if not cache.has_key("tags"):
        tags = Tag.objects.all()
        cache.set("tags",tags)
    else:
        tags = cache.get("tags")

    return render(request,'blogapp/index.html',{
        "posts": posts,
        "is_tag": True,
        'tag_active':'active',
        "tag_name": t,
        "categories": categories,
        'links':links,
        'tags':tags,
    })


# CURD
@login_required
def add(request):
    context = RequestContext(request)

    add_instance = Post(author=request.user)

    if request.method == "POST":
        forms = PostForm(instance=add_instance,data=request.POST)
        if forms.is_valid():
            forms.save()

            # 添加文章之后，我们更新 cache
            posts = Post.objects.all()
            cache.set("posts",posts)

            categories = Category.objects.all()
            cache.set("categories",categories)

            links = FriendLink.objects.all()
            cache.set("links",links)

            tags = Tag.objects.all()
            cache.set("tags",tags)

            return HttpResponseRedirect(reverse("index"))
        else:
            messages.info(request,forms.errors)
            return HttpResponseRedirect(reverse("add"))
    else:
        forms = PostForm(instance=add_instance)
        tags = Tag.objects.all()
        categories = Category.objects.all()
        return render_to_response('blogapp/post_forms.html',{
            "forms":forms,
            "tags":tags,
            "categories": categories,
            'action':'add',
        },context)


@login_required
def edit(request,pk):
    context = RequestContext(request)

    try:
        p = Post.objects.get(id=pk)
    except Post.DoesNotExist:  ## 读取分类，如果不存在，则引发错误，并404
        raise Http404

    if request.method == "POST":
        forms = PostForm(instance=p,data=request.POST)
        if forms.is_valid():
            forms.save()
            # 文章更新，我们也更新 cache
            posts = Post.objects.all()
            cache.set("posts",posts)

            categories = Category.objects.all()
            cache.set("categories",categories)

            links = FriendLink.objects.all()
            cache.set("links",links)

            tags = Tag.objects.all()
            cache.set("tags",tags)

            return HttpResponseRedirect(reverse('post_default',kwargs={'pk':pk}))
        else:
            messages.info(request,forms.errors)
            return HttpResponseRedirect(reverse("edit",kwargs={'pk':pk}))
    else:
        forms = PostForm(instance=p)
        tags = Tag.objects.all()
        categories = Category.objects.all()
        return render_to_response('blogapp/post_forms.html',{
            "forms":forms,
            'tags':tags,
            'post':p,
            "categories": categories,
            'action':'edit',
        },context)

# @login_required
def ajax_markdown_preview(request):
    d = {}
    if request.method == "POST":
        raw = request.POST.get('md','')
        raw.lstrip()
        html = md(raw, extensions=['gfm'])
        d['html'] = html
        d['code'] = 0
        d['msg']  = 'success'
        return HttpResponse(json.dumps(d),content_type="application/json")
    else:
        d['code'] = 1
        d['msg'] = 'invalid request method'
        return HttpResponse(json.dumps(d),content_type="application/json")
