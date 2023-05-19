from flower.utils.flowerform import DateSelectForm


def data_filter(request):
    """
    对数据进行筛选
    筛选出当前登录用户的门店对应的数据
    筛选选定日期之间的数据
    :param request: 请求
    :return: search_dict 筛选条件
             date  页面显示的日期
    """
    search_dict = {}
    if request.session.get("info", {}).get("store_id", "") != 1:
        search_dict["store"] = request.session.get("info", {}).get("store_id", "")
    start = request.GET.get("start_date", "")
    end = request.GET.get("end_date", "")
    if start:
        search_dict["created__gte"] = start
    if end:
        search_dict["created__lte"] = end
    date = DateSelectForm(initial={"start_date": start, "end_date": end})

    return search_dict, date
