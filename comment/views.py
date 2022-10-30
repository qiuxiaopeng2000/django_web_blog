from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse

from blog.models import blog_data
from .forms import comment_form
from .models import comment_data


# Create your views here.
@login_required(login_url='/userinfo/login/')
def create_comment(request, blog_id, user_id=None):
    comment_blog = get_object_or_404(blog_data, id=blog_id)
    if request.method == 'POST':
        create_comment_form = comment_form(data=request.POST)
        if create_comment_form.is_valid():
            created_comment = create_comment_form.save(commit=False)
            created_comment.article = comment_blog
            created_comment.comment_user = request.user
            if user_id is not None:
                pre_comment = comment_data.objects.get(id=user_id)
                created_comment.parent_id = pre_comment.get_root().id
                created_comment.reply_to_obj = pre_comment.user
                created_comment.save()
                # return HttpResponse("评论成功")
            created_comment.save()
            return redirect("blog_detail", blog_id)
        else:
            return HttpResponse("格式错误")
    # elif request.method == "GET":
    #     new_comment_form = comment_form()
    #     context = {
    #         'new_comment_form': new_comment_form,
    #         'blog_id': blog_id,
    #         'user_id': user_id,
    #     }
    #     return render(request, 'comment/reply.html', context)
    else:
        return HttpResponse("仅接受POST请求")


@login_required(login_url='/userinfo/login/')
def delete_comment(request, id):
    deleted_comment = comment_data.objects.get(id=id)
    if request.user != deleted_comment.comment_user:
        return HttpResponse("你不是该评论的作者，你无权删除")
    article_id = deleted_comment.article_id
    if request.method == 'POST':
        deleted_comment.delete()
        return redirect("blog_detail", article_id)
    else:
        return HttpResponse("删除操作仅允许post请求")
