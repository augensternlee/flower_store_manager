from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from flower.utils.flowerform import DianPingModelForm
from flower.utils.data_filter import data_filter
from flower.utils.pagination import Pagination
from flower import models


def dianping_list(request):
    """ 美团数据 """
    search_dict, date = data_filter(request)

    queryset = models.DianPing.objects.filter(**search_dict).order_by("-date")
    # 分页
    pagination = Pagination(request, queryset, page_size=10, page_params="page", plus=10)
    pagination_query, pagination_str = pagination.html()

    context = {
        "queryset": pagination_query,
        "pagination_str": pagination_str,
        "date": date
    }

    return render(request, "dianping_list.html", context)


def dianping_add(request):
    """增加外卖数据"""
    title = "新增数据"
    if request.method == "GET":
        store_id = request.session.get("info").get("store_id")
        form = DianPingModelForm(initial={"store": store_id})
        store = get_object_or_404(models.Store, pk=store_id)
        return render(request, "change.html", {"title": title, "form": form, "store": store})
    form = DianPingModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/dianping/list/")
    return render(request, "change.html", {"title": title, "form": form})


def dianping_detail(request, did):
    """订单详情"""
    title = "美团外卖-经营业绩详情"
    obj = get_object_or_404(models.DianPing, pk=did)
    form = DianPingModelForm(instance=obj)
    return render(request, "detail.html", {"title": title, "form": form})


def dianping_delete(request):
    """删除订单"""
    mid = request.GET.get("id", None)
    if not mid:
        return JsonResponse({"status": False, "error": "错误,无效的记录"})

    row_obj = models.DianPing.objects.filter(id=mid).first()
    if not row_obj:
        return JsonResponse({"status": False, "error": "错误,没有找到该数据,请刷新页面"})

    row_obj.delete()
    return JsonResponse({"status": True})

