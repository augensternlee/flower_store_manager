from django.shortcuts import render, redirect
from django.http import JsonResponse
from flower import models
from flower.utils.flowerform import ManagerModelForm, ManagerEditPasswdModelForm
from flower.utils.pagination import Pagination


def manager_list(request):
    """店长清单首页"""
    queryset = models.Manager.objects.all()
    pagination = Pagination(request, queryset, page_size=10, page_params="page", plus=10)
    pagination_query, pagination_str = pagination.html()

    context = {
        "queryset": pagination_query,
        "pagination_str": pagination_str
    }
    return render(request, "manager_list.html", context)


def manager_add(request):
    """添加店长账号"""
    title = "新增店长账号"
    if request.method == "GET":
        form = ManagerModelForm()
        return render(request, "change.html", {"title": title, "form": form})

    form = ManagerModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/manager/list/")
    return render(request, "change.html", {"title": title, "form": form})


def manager_eidt_pw(request):
    """ 修改密码 """

    title = "修改账号密码"
    mid = request.session.get("info").get("id")
    manager = models.Manager.objects.filter(id=mid).first()
    if request.method == "GET":
        form = ManagerEditPasswdModelForm(instance=manager)
        return render(request, "change.html", {"title": title, "form": form})
    form = ManagerEditPasswdModelForm(data=request.POST, instance=manager)
    if form.is_valid():
        form.save()
        return redirect("/manager/list/")
    return render(request, "change.html", {"title": title, "form": form})


def manager_edit(request, mid):
    """ 修改密码 """

    title = "修改店长账号"
    manager = models.Manager.objects.filter(id=mid).first()
    if request.method == "GET":
        form = ManagerModelForm(instance=manager)
        return render(request, "change.html", {"title": title, "form": form})
    form = ManagerModelForm(data=request.POST, instance=manager)
    if form.is_valid():
        form.save()
        return redirect("/manager/list/")
    return render(request, "change.html", {"title": title, "form": form})

def manager_delete(request):
    """ 修改密码 """
    mid = request.GET.get("id", None)
    if not mid:
        return JsonResponse({"status": False, "error": "错误,无效的记录"})

    row_obj = models.Manager.objects.filter(id=mid).first()
    if not row_obj:
        return JsonResponse({"status": False, "error": "错误,没有找到该数据,请刷新页面"})

    row_obj.delete()
    return JsonResponse({"status": True})
