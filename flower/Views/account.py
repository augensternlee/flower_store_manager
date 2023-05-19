from io import BytesIO
from django.shortcuts import render, redirect, HttpResponse
from flower.utils.flowerform import LoginForm
from flower import models
from flower.utils.code import check_code


def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 图片验证码
        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("img_code")
        if user_input_code.upper() != code.upper():
            form.add_error("code", "验证码错误")
            return render(request, "login.html", {"form": form})

        manager_object = models.Manager.objects.filter(**form.cleaned_data).first()
        # 验证用户名密码
        if not manager_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form})

        request.session["info"] = {
            "id": manager_object.id,
            "user": manager_object.user,
            "name": manager_object.name,
            "level": manager_object.level,
            "store_id": manager_object.store_id,

        }
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/index/")
    return render(request, "login.html", {"form": form})


def logout(request):
    """登出"""
    request.session.clear()
    return redirect("/login/")


def image_code(request):
    """生成验证码"""
    img, code_string = check_code()

    # 将图片验证信息写入session
    request.session["img_code"] = code_string
    # 设置session超时时间
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, "png")
    return HttpResponse(stream.getvalue())
