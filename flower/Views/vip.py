from django.shortcuts import render, redirect
from flower.utils.pagination import Pagination
from flower.utils.flowerform import VipAddModelForm, VipTopupModelForm
from flower import models
from decimal import Decimal


def vip_list(request):
    """会员列表"""
    search_dict = {}
    num = request.GET.get("p", "")
    if num:
        search_dict["tel__contains"] = num
    queryset = models.Vip.objects.filter(**search_dict)

    # 分页
    pagination = Pagination(request, queryset, page_size=10, page_params="page", plus=10)
    pagination_query, pagination_str = pagination.html()

    context = {
        "queryset": pagination_query,
        "pagination_str": pagination_str,
        "num": num
    }

    return render(request, "vip_list.html", context)


def vip_add(request):
    """添加会员"""
    title = "新增会员"
    if request.method == "GET":
        form = VipAddModelForm()
        return render(request, "change.html", {"title": title, "form": form})

    form = VipAddModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/vip/list/")
    return render(request, "change.html", {"title": title, "form": form})


def vip_topup(request, vid):
    """会员充值"""
    title = "会员充值"
    vip = models.Vip.objects.filter(id=vid).first()
    if not vip:
        return redirect("/vip/list/")

    if request.method == "GET":
        form = VipTopupModelForm(initial={'vip_num': vip.id, "type": 1})
        return render(request, "change.html", {"title": title, "form": form})

    form = VipTopupModelForm(data=request.POST)

    if form.is_valid():
        vip.balance += Decimal(request.POST.get("amount"))
        form.save()
        vip.save()
        return redirect("/vip/list/")
    return render(request, "change.html", {"title": title, "form": form})


def vip_detail(request, vid):
    """会员费用详情"""
    queryset = models.VipCost.objects.filter(vip_num=vid).order_by("-time")

    pagination = Pagination(request, queryset, page_size=10, page_params="page", plus=10)
    pagination_query, pagination_str = pagination.html()
    context = {
        "queryset": pagination_query,
        "pagination_str": pagination_str
    }

    return render(request, "vip_detail.html", context)


