from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from flower.utils.pagination import Pagination
from flower.utils.data_filter import data_filter
from flower import models
from flower.utils.flowerform import DateSelectForm, OrderAddModelForm, OrderEditModelForm, OrderDetailModelForm


def order_list(request):
    """订单清单"""

    search_dict, date = data_filter(request)
    queryset = models.Order.objects.filter(**search_dict).order_by("-created")
    # 分页
    pagination = Pagination(request, queryset, page_size=10, page_params="page", plus=10)
    pagination_query, pagination_str = pagination.html()

    context = {
        "queryset": pagination_query,
        "pagination_str": pagination_str,
        "date": date
    }

    return render(request, "order_list.html", context)


def order_add(request):
    """新增订单"""
    title = "新增订单"
    if request.method == "GET":
        store_id = request.session.get("info").get("store_id")
        form = OrderAddModelForm(initial={"store": store_id})
        store = get_object_or_404(models.Store, pk=store_id)
        return render(request, "change.html", {"title": title, "form": form, "store": store})


    form = OrderAddModelForm(data=request.POST, files=request.FILES)
    # 验证不通过则就再页面提示
    if not form.is_valid():
        return render(request, "change.html", {"title": title, "form": form})

    # 非会员卡消费直接保存
    print(form.cleaned_data.get("paid_type", "") == 7)
    if form.cleaned_data.get("paid_type", "") != 7:
        form.save()
        return redirect("/order/list/")

    # 是否选择了会员卡
    vip_id = form.cleaned_data.get("vip", "")
    vip_id = str(vip_id).split("-")[0]
    if not vip_id:
        form.add_error("vip", "请输入会员卡号")
        return render(request, "change.html", {"title": title, "form": form})

    # 会员是否存在
    vip = models.Vip.objects.filter(vip=vip_id).first()
    if not vip:
        form.add_error("vip", "会员不存在")
        return render(request, "change.html", {"title": title, "form": form})

    # 会员余额是否充足
    if vip.balance < form.cleaned_data.get("paid"):
        form.add_error("vip", "账户余额不足,请充值")
        return render(request, "change.html", {"title": title, "form": form})

    employee_id = str(form.cleaned_data.get("receiver")).split("--")[0]
    employee = models.Employee.objects.filter(id=employee_id).first()
    models.VipCost.objects.create(vip_num=vip, type=0, amount=form.cleaned_data.get("amount"),
                                  employee=employee).save()
    form.cleaned_data["store"] = request.session.get("info").get("store_id")
    form.save()
    vip.balance -= form.cleaned_data.get("paid")
    vip.save()
    return redirect("/order/list/")


def order_edit(request, oid):
    """订单修改"""
    title = "修改订单"
    order = models.Order.objects.filter(id=oid).first()
    if request.method == "GET":
        form = OrderEditModelForm(instance=order)
        return render(request, "change.html", {"title": title, "form": form})

    form = OrderEditModelForm(data=request.POST, instance=order)
    if form.is_valid():
        form.save()
        return redirect("/order/list/")
    return render(request, "change.html", {"title": title, "form": form})


def order_detail(request, oid):
    """订单详情"""
    title = "订单详情"
    obj = get_object_or_404(models.Order, pk=oid)
    form = OrderDetailModelForm(instance=obj)
    return render(request, "order_detail.html", {"title": title, "form": form})


def order_delete(request):
    """删除订单"""
    oid = request.GET.get("id", None)
    if not oid:
        return JsonResponse({"status": False, "error": "错误,无效的记录"})

    row_obj = models.Order.objects.filter(id=oid).first()
    if not row_obj:
        return JsonResponse({"status": False, "error": "错误,没有找到该数据,请刷新页面"})

    row_obj.delete()
    return JsonResponse({"status": True})
