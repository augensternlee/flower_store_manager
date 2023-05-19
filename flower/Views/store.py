from django.shortcuts import render, redirect
from django.http import JsonResponse
from flower.utils.flowerform import StoreModelForm
from flower.utils.pagination import Pagination
from flower import models


def store_list(request):
    """管理列表"""
    queryset = models.Store.objects.all()

    pagination = Pagination(request, queryset, page_size=10, page_params="page", plus=10)
    pagination_query, pagination_str = pagination.html()

    context = {
        "queryset": pagination_query,
        "pagination_str": pagination_str
    }

    return render(request, "store_list.html", context)


def store_add(request):
    """ 新增门店 """
    title = "新增门店"
    if request.method == "GET":
        form = StoreModelForm()
        return render(request, "change.html", {"title": title, "form": form})

    form = StoreModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/store/list/")
    return render(request, "change.html", {"title": title})


def store_edit(request, store_id):
    """ 修改门店 """
    title = "修改门店"
    store = models.Store.objects.filter(id=store_id).first()
    if request.method == "GET":
        form = StoreModelForm(instance=store)
        return render(request, "change.html", {"title": title, "form": form})

    form = StoreModelForm(data=request.POST, instance=store)
    if form.is_valid():
        form.save()
        return redirect("/store/list/")
    return render(request, "change.html", {"title": title})


def store_delete(request):
    """ 删除门店 """
    sid = request.GET.get("id", None)
    if not sid:
        return JsonResponse({"status": False, "error": "错误,无效的记录"})

    row_obj = models.Store.objects.filter(id=sid).first()
    if not row_obj:
        return JsonResponse({"status": False, "error": "错误,没有找到该数据,请刷新页面"})

    row_obj.delete()
    return JsonResponse({"status": True})
