"""xihuamanyu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from flower.Views import index, store, manager, account, vip, order, meituan, dianping, attendance, business

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 静态图片
    re_path(r"^media/(?P<path>.*)$", serve, {'document_root': settings.MEDIA_ROOT}, name="media"),

    # 首页
    path('index/', index.index),
    path('', index.index),

    # 权限不足页面
    path('permission/', index.permission),

    # 门店管理
    path('store/list/', store.store_list),
    path('store/add/', store.store_add),
    path('store/<int:store_id>/edit/', store.store_edit),
    path('store/delete/', store.store_delete),

    # 店长管理
    path('manager/list/', manager.manager_list),
    path('manager/add/', manager.manager_add),
    path('manager/<int:mid>/edit/', manager.manager_edit),
    path('manager/eidt/password/', manager.manager_eidt_pw),
    path('manager/delete/', manager.manager_delete),

    # 登录管理
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    # 会员卡管理
    path('vip/list/', vip.vip_list),
    path('vip/add/', vip.vip_add),
    path('vip/<int:vid>/topup/', vip.vip_topup),
    path('vip/<int:vid>/detail/', vip.vip_detail),

    # 订单中心
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/<int:oid>/edit/', order.order_edit),
    path('order/<int:oid>/detail/', order.order_detail),
    path('order/delete/', order.order_delete),

    # 美团外卖数据
    path('meituan/list/', meituan.meituan_list),
    path('meituan/add/', meituan.meituan_add),
    path('meituan/<int:mid>/detail/', meituan.meituan_detail),
    path('meituan/<int:mid>/delete/', meituan.meituan_delete),
    path('meituan/delete/', meituan.meituan_delete),

    # 大众点评数据
    path('dianping/list/', dianping.dianping_list),
    path('dianping/add/', dianping.dianping_add),
    path('dianping/<int:did>/detail/', dianping.dianping_detail),
    path('dianping/<int:did>/delete/', dianping.dianping_delete),
    path('dianping/delete/', dianping.dianping_delete),

    # 考勤管理
    path('attendance/list/', attendance.attendance_list),
    path('attendance/add/', attendance.attendance_add),
    path('attendance/<int:eid>/edit/', attendance.attendance_edit),
    path('attendance/delete/', attendance.attendance_delete),

    # 经营业绩仪表板
    path('business/dashboard/', business.dashboard),
    # path('business/turnover/', business.turnover),
]
