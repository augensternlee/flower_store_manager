import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class LoginAuthMiddleWare(MiddlewareMixin):
    """用户登录验证中间件"""

    def process_request(self, request):
        """ 请求验证 """
        # 如果用户请求的是login页面,直接放行
        # print("来", request.path_info)
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 如果用户请求其他页面验证是否登录
        info = request.session.get("info")
        if info:
            return

        # 没有登录,就重定向到登录页面
        return redirect("/login/")

    def process_response(self, request, response):
        """ 返回验证 """
        return response


class PermissionAuthMiddleWare(MiddlewareMixin):
    """用户登录验证中间件"""

    def process_request(self, request):
        """ 请求验证 """

        # 获取用户权限级别
        info = request.session.get("info")
        if not info:
            return
        level = info.get("level")
        page = re.match(r'/store/.*|/manager/.*', request.path_info)
        
        if page and level != 0:
            return redirect("/permission/")

        # 非老板请求其他界面一律放行
        return 

    def process_response(self, request, response):
        """ 返回验证 """
        return response
