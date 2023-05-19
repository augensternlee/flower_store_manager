from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from flower.utils.pagination import Pagination
from flower.utils.data_filter import data_filter
from flower.utils.flowerform import AttendanceModelForm
from flower import models


def attendance_list(request):
    """考情清单"""
    search_dict, date = data_filter(request)

    queryset = models.Attendance.objects.filter(**search_dict).order_by("-date")
    # 分页
    pagination = Pagination(request, queryset, page_size=10, page_params="page", plus=10)
    pagination_query, pagination_str = pagination.html()

    context = {
        "queryset": pagination_query,
        "pagination_str": pagination_str,
        "date": date
    }

    return render(request, "attendance_list.html", context)


def attendance_add(request):
    """添加考勤信息"""
    title = "添加考勤信息"
    store_id = request.session.get("info").get("store_id")
    if request.method == "GET":
        form = AttendanceModelForm(store=store_id)
        store = get_object_or_404(models.Store, pk=store_id)
        return render(request, "change.html", {"title": title, "form": form, "store": store})

    form = AttendanceModelForm(data=request.POST, store=store_id)
    if form.is_valid():
        form.save()
        return redirect("/attendance/list/")
    return render(request, "change.html", {"title": title, "form": form})


def attendance_edit(request, eid):
    """修改考勤信息"""
    title = "修改考勤信息"
    attendace = models.Attendance.objects.filter(id=eid).first()
    store_id = request.session.get("info").get("store_id")
    if request.method == "GET":
        form = AttendanceModelForm(store=store_id, instance=attendace)
        return render(request, "change.html", {"title": title, "form": form})

    form = AttendanceModelForm(data=request.POST, instance=attendace, store=store_id)
    if form.is_valid():
        form.save()
        return redirect("/attendance/list/")
    return render(request, "change.html", {"title": title, "form": form})


def attendance_delete(request):
    """删除订单"""
    aid = request.GET.get("id", None)
    if not aid:
        return JsonResponse({"status": False, "error": "错误,无效的记录"})

    row_obj = models.Attendance.objects.filter(id=aid).first()
    if not row_obj:
        return JsonResponse({"status": False, "error": "错误,没有找到该数据,请刷新页面"})

    row_obj.delete()
    return JsonResponse({"status": True})
