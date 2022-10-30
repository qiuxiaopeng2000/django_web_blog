import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views import View

from .models import blog_data, blog_classification
from .forms import blog_create_form
from comment.models import comment_data
from comment.forms import comment_form
from userinfo.models import user_info_data


# Create your views here.

@login_required(login_url='/userinfo/login/')
def create_blog(request):
    if request.method == 'POST':
        blog_post_form = blog_create_form(request.POST)
        if blog_post_form.is_valid():
            new_blog = blog_post_form.save(commit=False)
            new_blog.author = User.objects.get(id=request.user.id)
            new_blog.is_original = True
            if request.POST['category'] != 'none':
                new_blog.classification = blog_classification.objects.get(id=request.POST['category'])
            new_blog.save()
            blog_post_form.save_m2m()
            return redirect('blog_list')
        else:
            return HttpResponse("请输入正确的格式")
    else:
        category = blog_classification.objects.all()
        blog_form = blog_create_form()
        context = {'category': category, 'blog_form': blog_form}
        return render(request, 'blog/create.html', context)


@login_required(login_url='/userinfo/login/')
def update_blog(request, id):
    old_blog = blog_data.objects.get(id=id)
    if request.user != old_blog.author:
        return HttpResponse("你不是该文章作者，你无权修改")
    if request.method == 'POST':
        new_blog = blog_create_form(data=request.POST)
        if new_blog.is_valid():
            old_blog.title = request.POST['title']
            old_blog.body = request.POST['body']
            if request.POST['category'] != 'none':
                old_blog.classification = blog_classification.objects.get(id=request.POST['category'])
            else:
                old_blog.classification = None
            old_blog.tags.set(*request.POST.get('tags').split(','), clear=True)
            old_blog.save()
            return redirect("blog_detail", id=id)
        else:
            return HttpResponse("请输入正确的格式")
    else:
        blog_form = blog_create_form()
        category = blog_classification.objects.all()
        context = {'category': category, 'old_blog': old_blog, 'blog_form': blog_form}
        return render(request, 'blog/update.html', context)


@login_required(login_url='/userinfo/login/')
def delete_blog(request, id):
    deleted_blog = blog_data.objects.get(id=id)
    if request.user != deleted_blog.author:
        return HttpResponse("你不是该文章的作者，你无权删除")
    if request.method == 'POST':
        deleted_blog.delete()
        return redirect("blog_list")
    else:
        return HttpResponse("删除操作仅允许post请求")


def blog_list(request, category_id=None):
    # 查找功能
    search = request.GET.get('search')
    # 排序功能
    order = request.GET.get('order')
    all_category = blog_classification.objects.all()
    try:
        category = blog_classification.objects.get(id=category_id)
    except blog_classification.DoesNotExist:
        category = None
    tag = request.GET.get('tag')

    all_blog = blog_data.objects.all()

    # 查找
    if search:
        all_blog = all_blog.filter(
            # ???
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 分类
    if category is not None:
        all_blog = all_blog.filter(classification=category)

    if tag and tag != 'None':
        all_blog = all_blog.filter(tags__name__in=[tag])

    if order == 'num_of_views':
        # 按浏览量排序
        all_blog = all_blog.order_by('-num_of_views')

    mda = markdown_apply()
    mda.__int__()
    for blog in all_blog:
        blog.body = mda.apply(text=blog.body)
    # 每页显示3篇文章
    # num_per_page = Paginator(all_blog, 3)
    # page = request.GET.get('page')
    # blogs = num_per_page.get_page(page)
    blogs = all_blog
    context = {'blogs': blogs, 'search': search, 'order': order, 'category': category, 'all_category': all_category,
               'tag': tag}
    return render(request, 'blog1/list.html', context)


def blog_detail(request, id):
    now_blog = get_object_or_404(blog_data, id=id)
    get_user_info = user_info_data.objects.get(user=now_blog.author)
    now_blog.num_of_views += 1
    now_blog.save(update_fields=['num_of_views'])
    all_category = blog_classification.objects.all()
    # 取出评论
    comments = comment_data.objects.filter(article=id)

    # 相邻发表文章的快捷导航
    pre_blogs = blog_data.objects.filter(id__lt=now_blog.id).order_by('-id')
    next_blogs = blog_data.objects.filter(id__gt=now_blog.id).order_by('id')
    if pre_blogs.count() > 0:
        pre_blogs = pre_blogs[0]
    else:
        pre_blogs = None
    if next_blogs.count() > 0:
        next_blogs = next_blogs[0]
    else:
        next_blogs = None
    mda = markdown_apply()
    mda.__int__()
    now_blog.body = mda.apply(text=now_blog.body)
    create_comment = comment_form()
    context = {'blog': now_blog,
               'toc': mda.md.toc,
               'comments': comments,
               'pre_blog': pre_blogs,
               'next_blog': next_blogs,
               'create_comment': create_comment,
               'get_user_info': get_user_info,
               'all_category': all_category}
    return render(request, 'blog1/detail.html', context)


@login_required(login_url='/userinfo/login/')
def transmit_blog(request, id):
    transmitted_blog = blog_data.objects.get(id=id)
    new_blog_form = blog_create_form()
    new_blog_data = new_blog_form.save(commit=False)
    new_blog_data.title = transmitted_blog.title
    new_blog_data.body = transmitted_blog.body
    new_blog_data.tags = transmitted_blog.tags
    new_blog_data.classification = transmitted_blog.classification
    new_blog_data.author = User.objects.get(id=request.user.id)
    new_blog_data.is_original = False
    new_blog_data.from_author = transmitted_blog
    new_blog_data.save()
    return redirect('blog_detail', id)


@login_required(login_url='/userinfo/login/')
def my_blog(request, user):
    my_blogs = blog_data.objects.filter(author__username=user)
    all_category = blog_classification.objects.all()
    mda = markdown_apply()
    mda.__int__()
    for blog in my_blogs:
        blog.body = mda.apply(text=blog.body)
    context = {'my_blogs': my_blogs, 'all_category': all_category}
    return render(request, 'blog1/myblog.html', context)


class markdown_apply:
    def __int__(self):
        self.md = markdown.Markdown(
            extensions=[
                # 包含 缩写、表格等常用扩展
                'markdown.extensions.extra',
                # 语法高亮扩展
                'markdown.extensions.codehilite',
                # 目录扩展
                'markdown.extensions.toc',
            ])

    def apply(self, text):
        text = self.md.convert(text)
        return text


# # 点赞功能
# def increase_likes(request, id):
#     blog = blog_data.objects.get(id=id)
#     # if request.method == "POST":
#     #     artical = blog_data.objects.get(id=id)
#     #     artical.num_of_likes += 1
#     #     artical.save()
#     #     return redirect('blog_detail', blog.id)
#     # elif request.method == "GET":
#     #     context = {'blog': blog}
#     #     return render(request, 'blog/artical_likes.html', context)
#     artical = blog_data.objects.get(id=id)
#     artical.num_of_likes += 1
#     artical.save()
#     context = {'blog': blog}
#     return render(request, 'blog/artical_likes.html', context)

class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = blog_data.objects.get(id=kwargs.get('id'))
        article.num_of_likes += 1
        article.save()
        return HttpResponse('success')
