"""
使用分页类需要先实例化对象
request:请求对象
queryset: ORM查询出来的数据
page_size: 每页显示的数量 可选
page_params: 请求携带分页页码指示的参数名 可选
plus: 最大显示页数 可选

实例化对象之后调用html方法获取分页后的queryset与分页html代码
pagination = Pagination(request, queryset, page_size=10, page_params="page", plus=10)
pagination_query, pagination_str = pagination.html()

将需要传递给前端的参数封装到字典中传给html页面
context = {
    "queryset": pagination_query,
    "pagination_str": pagination_str
}

在前端页面中添加代码:
<!-- 分页栏 -->
<nav aria-label="Page navigation">
    <ul class="pagination">
        {{ pagination_str }}
    </ul>
</nav>

"""


from django.utils.safestring import mark_safe
import copy


class Pagination(object):
    """
    分页类
    """

    def __init__(self, request, queryset, page_size=10, page_params="page", plus=10):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数，例如：/etty/list/?page=12
        :param plus: 显示当前页的 前或后几页（页码）
        """
        self.queryset = queryset
        self.page_size = page_size
        self.page_params = page_params
        self.plus = plus

        # 计算总数据量
        self.total_queryset_num = self.queryset.count()

        # 在原有的参数上添加页码参数
        self.query_dict = copy.deepcopy(request.GET)
        # 设置query_dict可以修改添加参数
        self.query_dict._mutable = True

        # 用户请求的页数
        self.page = request.GET.get(page_params, "1")
        if self.page.isdecimal():
            self.page = int(self.page)
        else:
            self.page = 1

        # 计算最大页数
        self.total_page_count, div = divmod(self.total_queryset_num, self.page_size)
        if div:
            self.total_page_count += 1

        # 计算显示数据分页的起始值与停止值
        self.start_num = (self.page - 1) * page_size
        self.end_num = self.page * page_size

        # 将数据切分
        self.page_queryset = queryset[self.start_num: self.end_num]

    def html(self):
        """
        分页
        :return:
        """

        # 分页按钮
        page_str_list = []

        # 上一页
        if self.page == 1:
            previous_page_str = ''
        else:
            # 在请求参数中添加参数
            self.query_dict.setlist(self.page_params, [self.page - 1])
            previous_page_str = f'<li><a href="?{self.query_dict.urlencode()}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
        page_str_list.append(previous_page_str)

        # 网页最多显示n个分页按钮
        page_str_list.append("<li>")

        # 如果总数据量没有达到5页,则页面只显示总数据量页数的分页按钮
        if self.total_page_count <= self.plus:
            start_page = 1
            end_page = self.total_page_count+1
        else:
            if self.page <= self.plus // 2:
                start_page = 1
                end_page = self.plus + 1
            elif self.page > self.total_page_count - self.plus / 2:
                start_page = self.total_page_count - self.plus + 1
                end_page = self.total_page_count + 1
            else:
                start_page = self.page - self.plus // 2
                end_page = self.page + self.plus // 2 + 1

        for i in range(start_page, end_page):
            self.query_dict.setlist(self.page_params, [i])
            if i == self.page:
                page_str_list.append(f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}</a></li>')
            else:
                page_str_list.append(f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>')
        page_str_list.append("</li>")

        # 下一页
        if self.page >= self.total_page_count:
            next_page_str = ''
        else:
            self.query_dict.setlist(self.page_params, [self.page + 1])
            next_page_str = f'<li><a href="?{self.query_dict.urlencode()}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
        page_str_list.append(next_page_str)

        # 拼接所有的上一页地址与下一页地址
        page_str = mark_safe("".join(page_str_list))
        return self.page_queryset, page_str
