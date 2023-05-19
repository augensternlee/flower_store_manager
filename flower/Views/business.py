import jwt
import time
from django.shortcuts import render


def dashboard(request):
    """图形展示"""
    METABASE_SITE_URL = "http://120.48.103.141:3000"
    METABASE_SECRET_KEY = "bc6eb07347b6c169a309d7835318d517c96197a2925e8056f061a9ff4f7fe7a7"

    payload = {
        "resource": {"dashboard": 1},
        "params": {

        },
        "exp": round(time.time()) + (60 * 10)  # 10 minute expiration
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=true"
    return render(request, "dashboard.html", {"iframeUrl": iframeUrl})
