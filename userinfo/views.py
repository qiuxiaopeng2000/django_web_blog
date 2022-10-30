from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, HttpResponse, redirect
from .models import user_info_data, Follow
from .forms import user_login_form, user_register_form, user_info_form, user_change_password_form, user_follow_form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.


def user_login(request):
    if request.method == 'POST':
        new_user_login_form = user_login_form(data=request.POST)
        if new_user_login_form.is_valid():
            data = new_user_login_form.cleaned_data
            # 检验账号、密码是否正确
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect("blog_list")
            else:
                return HttpResponse("账号或密码输入有误。请重新输入!")
        else:
            return HttpResponse("账号或密码格式不正确")
    elif request.method == 'GET':
        new_user_login_form = user_login_form()
        context = {'form': new_user_login_form}
        return render(request, 'userinfo/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


def user_logout(request):
    logout(request)
    return redirect("blog_list")


def user_register(request):
    if request.method == "POST":
        new_user_register_form = user_register_form(data=request.POST)
        new_user_info_form = user_info_form()
        if new_user_register_form.is_valid():
            new_user = new_user_register_form.save(commit=False)
            new_user.set_password(new_user_register_form.cleaned_data['password'])
            new_user_info_data = new_user_info_form.save(commit=False)
            new_user_info_data.user = new_user
            new_user.save()
            new_user_info_data.save()
            login(request, new_user)
            return redirect("blog_list")
        else:
            return HttpResponse("注册信息格式不正确")
    else:
        return render(request, 'userinfo/register.html')


@login_required(login_url='/userinfo/login/')
def user_delete(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        if request.user == user:
            logout(request)
            user.delete()
            return redirect("blog_list")
        else:
            return HttpResponse("你没有通过身份验证，你无权注销用户")
    else:
        return HttpResponse("注销用户仅接受POST请求")


@login_required(login_url='/userinfo/login/')
def user_info_edit(request, user_id):
    user = User.objects.get(id=user_id)
    if user_info_data.objects.filter(user_id=user_id).exists():
        get_user_info = user_info_data.objects.get(user_id=user_id)
    else:
        get_user_info = user_info_data.objects.create(user=user)

    if request.method == "POST":
        if request.user != user:
            return HttpResponse("你没有通过身份验证，你无权修改用户信息")

        new_user_info_form = user_info_form(request.POST, request.FILES)
        if new_user_info_form.is_valid():
            new_user_info_data = new_user_info_form.cleaned_data
            if 'portrait' in request.FILES:
                get_user_info.portrait = new_user_info_data['portrait']
            if 'background_img' in request.FILES:
                get_user_info.background_img = new_user_info_data['background_img']
            get_user_info.phone = new_user_info_data['phone']
            get_user_info.age = new_user_info_data['age']
            get_user_info.sex = new_user_info_data['sex']
            get_user_info.self_introduce = new_user_info_data['self_introduce']
            get_user_info.signature = new_user_info_data['signature']
            get_user_info.save()
            return redirect("blog_list")
        else:
            return HttpResponse("数据格式有误，请重新输入")
    elif request.method == "GET":
        context = {'user_info': get_user_info, 'user': user}
        return render(request, 'userinfo/personal_page.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


def change_password(request, user_id):
    if request.method == "GET":
        return render(request, 'userinfo/change_password.html')
    elif request.method == "POST":
        user = User.objects.get(id=user_id)
        if request.user != user:
            return HttpResponse("用户身份验证失败，无权修改密码！")
        # new_password_form = user_change_password_form(data=request.POST)
        if check_password(request.POST.get('old_password'), user.password):
            if request.POST.get('password') != request.POST.get('password2'):
                return HttpResponse("两次密码输入不一致，请重新输入")
            user.password = make_password(request.POST.get('password'))
            user.save()
            return redirect("blog_list")
        else:
            return HttpResponse("原密码输入错误")
    else:
        return HttpResponse("只允许GET请求和POST请求修改密码")


@login_required(login_url='/userinfo/login/')
def follow_other(request, user_id1, user_id2, blog_id):
    user2 = User.objects.get(id=user_id2)
    user1 = User.objects.get(id=user_id1)
    if user1 != user2:
        if Follow.objects.filter(user=user1).exists():
            get_user1 = Follow.objects.get(user=user1)
        else:
            get_user1_form = user_follow_form()
            get_user1 = get_user1_form.save(commit=False)

        if Follow.objects.filter(user=user2).exists():
            get_user2 = Follow.objects.get(user=user2)
        else:
            get_user2_form = user_follow_form()
            get_user2 = get_user2_form.save(commit=False)

        # if Follow.objects.filter(user=user1).exists():
        #     get_user1 = Follow.objects.get(user=user1)
        # else:
        #     get_user1 = user_info_data.objects.create(user_id=user_id1)
        #     get_user1.user = user1
        # if Follow.objects.filter(user=user2).exists():
        #     get_user2 = Follow.objects.get(user=user2)
        # else:
        #     get_user2 = user_info_data.objects.create(user_id=user_id2)
        get_user1.follow = user2
        get_user1.user = user1
        get_user2.fan = user1
        get_user2.user = user2
        get_user1.save()
        get_user2.save()
    return redirect("blog_detail", blog_id)


def my_follow(request, user_id):
    user = User.objects.get(id=user_id)
    all_follow = Follow.objects.filter(fan=user)
    # all_follow = user.follow_user.all()
    user_list = []
    for item in all_follow:
        user_list.append(item.follow)
    if len(user_list) == 0:
        return HttpResponse("你还没有关注任何人")
    all_follow_info = []
    for i in all_follow:
        obj = i.user
        user_info = user_info_data.objects.get(user=obj)
        all_follow_info.append(user_info)
    context = {'all_follow': all_follow, 'all_follow_info': all_follow_info, 'usr': user}
    return render(request, 'userinfo/my_follow.html', context)


def my_fans(request, user_id):
    user = User.objects.get(id=user_id)
    all_fans = Follow.objects.filter(follow=user)
    # all_fans = user.fan_user.all()
    user_list = []
    for item in all_fans:
        user_list.append(item.follow)
    if len(user_list) == 0:
        return HttpResponse("你还没有粉丝")
    all_fans_info = []
    for i in all_fans:
        obj = i.user
        user_info = user_info_data.objects.get(user=obj)
        all_fans_info.append(user_info)
    context = {'all_fan': all_fans, 'all_fans_info': all_fans_info, 'user': user}
    return render(request, "userinfo/my_fans.html", context)

