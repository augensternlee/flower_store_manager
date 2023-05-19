from django.shortcuts import render


def index(request):
    """首页"""

    return render(request,"index.html")


def permission(request):
    """权限不足"""
    return render(request, "permission.html")
