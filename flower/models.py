from django.db import models


# Create your models here.
class Store(models.Model):
    """ 门店表 """
    name = models.CharField(verbose_name="店名", max_length=32)
    address = models.CharField(verbose_name="地址", max_length=32)

    def __str__(self):
        return self.name


class Manager(models.Model):
    """ 管理员表 """
    store = models.ForeignKey(verbose_name='所属门店', to='Store', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='姓名', max_length=32)
    level_choices = (
        (0, "boss"),
        (1, "店长"),
        (2, "员工"),
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices)
    user = models.CharField(verbose_name='账号', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=32)


class Employee(models.Model):
    """员工表"""
    # 基本信息
    name = models.CharField(verbose_name="姓名", max_length=16)
    tel = models.CharField(verbose_name="联系电话", max_length=11)
    level_coices = (
        (0, "初级学员"),
        (1, "高级学员"),
        (2, "初级花艺师"),
        (3, "高级花艺师"),
        (4, "店长")
    )
    level = models.SmallIntegerField(verbose_name="员工级别", choices=level_coices)
    hiredate = models.DateField(verbose_name="入职日期", auto_now_add=True)
    store = models.ForeignKey(to="Store", on_delete=models.DO_NOTHING)
    gender_choices = (
        (1, "男"),
        (0, "女")
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)

    # 薪资待遇
    base_salary = models.DecimalField(verbose_name="基本工资", max_digits=10, decimal_places=2, default=0)
    attendance_bonus = models.DecimalField(verbose_name="全勤奖金", max_digits=10, decimal_places=2, default=0)
    performance_bonus = models.DecimalField(verbose_name="绩效奖金", max_digits=10, decimal_places=2, default=0)
    meal_subsidy = models.DecimalField(verbose_name="餐补", max_digits=10, decimal_places=2, default=0)
    manager_subsidy = models.DecimalField(verbose_name="店长补贴", max_digits=10, decimal_places=2, default=0)
    welfare_subsidy = models.DecimalField(verbose_name="福利补贴", max_digits=10, decimal_places=2, default=0)
    house_subsidy = models.DecimalField(verbose_name="租房补贴", max_digits=10, decimal_places=2, default=0)
    other_subsidy = models.DecimalField(verbose_name="其他补贴", max_digits=10, decimal_places=2, default=0)
    social_company = models.DecimalField(verbose_name="社保缴纳", max_digits=10, decimal_places=2, default=0)
    social_amount = models.DecimalField(verbose_name="社保扣款", max_digits=10, decimal_places=2, default=0)
    on_job_choices = (
        (1, "在职"),
        (0, "离职")
    )
    on_job = models.SmallIntegerField(verbose_name="是否在职", choices=on_job_choices, default=1)
    leave_date = models.DateField(verbose_name="离职日期", null=True, blank=True)

    def __str__(self):
        return f"{self.id}--{self.name}--{self.store.name}"


class Vip(models.Model):
    """ 会员中心 """
    vip = models.CharField(verbose_name="会员卡号", max_length=32, unique=True)
    name = models.CharField(verbose_name="会员姓名", max_length=32, null=True, blank=True)
    tel = models.CharField(verbose_name="联系电话", max_length=11, null=True, blank=True)
    balance = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.vip + "---" + self.name


class VipCost(models.Model):
    """会员费用记录"""
    vip_num = models.ForeignKey(verbose_name="会员编号", to='Vip', on_delete=models.DO_NOTHING)
    type_choices = (
        (0, "消费"),
        (1, "充值"),
    )
    type = models.SmallIntegerField(verbose_name="费用类型", choices=type_choices)
    amount = models.DecimalField(verbose_name="金额", max_digits=10, decimal_places=2)
    time = models.DateTimeField(verbose_name="费用发生时间", auto_now_add=True)
    employee = models.ForeignKey(verbose_name="操作员工", to=Employee, on_delete=models.DO_NOTHING)


class Order(models.Model):
    """订单表"""
    store = models.ForeignKey(verbose_name="门店", to="Store", related_name='orders', on_delete=models.DO_NOTHING)
    status_choices = (
        (0, "未完成"),
        (1, "已完成"),
    )
    status = models.SmallIntegerField(verbose_name="订单状态", choices=status_choices)
    created = models.DateTimeField(verbose_name="下单时间", auto_now_add=True)
    send = models.DateTimeField(verbose_name="配送时间", null=True, blank=True)
    send_type_choices = (
        (0, "自提"),
        (1, "配送"),
    )
    send_type = models.SmallIntegerField(verbose_name="配送类型", choices=send_type_choices)
    orderer = models.CharField(verbose_name="订花人", max_length=32, null=True, blank=True)
    orderer_tel = models.CharField(verbose_name="订花人电话", max_length=11, null=True, blank=True)
    consignee = models.CharField(verbose_name="收花人", max_length=32, null=True, blank=True)
    consignee_tel = models.CharField(verbose_name="收花人电话", max_length=11, null=True, blank=True)
    address = models.CharField(verbose_name="收花地址", max_length=255, null=True, blank=True)
    product_type_choices = (
        (0, "零花"),
        (1, "花束"),
        (2, "礼盒"),
        (3, "手提篮"),
        (4, "绿植"),
        (5, "开业花篮"),
        (6, "白事花圈"),
        (7, "布置：包厢、气球"),
        (8, "婚庆：手捧花、婚车"),
        (9, "其他类型"),
    )
    product_type = models.SmallIntegerField(verbose_name="产品类型", choices=product_type_choices)
    amount = models.DecimalField(verbose_name="总金额", max_digits=10, decimal_places=2, default=0)
    paid = models.DecimalField(verbose_name="已支付", max_digits=10, decimal_places=2, default=0)
    unpaid = models.DecimalField(verbose_name="未支付", max_digits=10, decimal_places=2, default=0)
    paid_type_choices = (
        (0, "现金"),
        (1, "微信"),
        (2, "收款码"),
        (3, "大众点评"),
        (4, "美团外卖"),
        (5, "饿了么"),
        (6, "公账"),
        (7, "会员卡"),
        (8, "其他"),
    )
    paid_type = models.SmallIntegerField(verbose_name="付款方式", choices=paid_type_choices)
    vip = models.ForeignKey(verbose_name="会员卡编号", to="Vip", on_delete=models.DO_NOTHING, null=True, blank=True)
    comment = models.CharField(verbose_name="特别备注", max_length=255, null=True, blank=True)
    resource_choices = (
        (0, "上门客"),
        (1, "微信"),
        (2, "美团"),
        (3, "大众点评"),
        (4, "美团外卖"),
        (5, "饿了么"),
        (6, "小程序"),
        (7, "地图"),
        (8, "其他"),
    )
    resource = models.SmallIntegerField(verbose_name="订单来源", choices=resource_choices)
    receiver = models.ForeignKey(verbose_name="接单员工", to='Employee', on_delete=models.DO_NOTHING, related_name="receiver")
    maker = models.ForeignKey(verbose_name="制作员工", to='Employee', on_delete=models.DO_NOTHING, related_name="maker")
    add_wechat_choices = ((0, "未添加"), (1, "已添加"),)
    add_wechat = models.SmallIntegerField(verbose_name="是否添加微信", choices=add_wechat_choices)
    wechat_nickname = models.CharField(verbose_name="微信名称", max_length=32, null=True, blank=True)
    rate_choices = (
        (0, "未评价"),
        (1, "好评"),
        (2, "一般"),
        (3, "差评"),
    )
    rate = models.SmallIntegerField(verbose_name="订单评价", choices=rate_choices)
    goods_image = models.ImageField(verbose_name="订单照片", upload_to='goods/', null=True, blank=True)
    product_image = models.ImageField(verbose_name="成品照片", upload_to='product/', null=True, blank=True)


class MeiTuan(models.Model):
    """外卖数据表"""
    store = models.ForeignKey(verbose_name="门店", to="Store", on_delete=models.DO_NOTHING)
    date = models.DateField(verbose_name="日期")
    comming_num = models.IntegerField(verbose_name="进店人数", default=0, null=True, blank=True)
    order_num = models.IntegerField(verbose_name="下单人数", default=0, null=True, blank=True)
    transform_rate = models.FloatField(verbose_name="入店转化率", default=0, null=True, blank=True)
    total_num = models.IntegerField(verbose_name="总流量", default=0, null=True, blank=True)
    click_num = models.IntegerField(verbose_name="点金次数", default=0, null=True, blank=True)
    auto_click_num = models.IntegerField(verbose_name="一站式点击", default=0, null=True, blank=True)
    natural_num = models.IntegerField(verbose_name="自然流量", default=0, null=True, blank=True)
    total_order = models.IntegerField(verbose_name="所有订单", default=0, null=True, blank=True)
    real_order = models.IntegerField(verbose_name="真实订单", default=0, null=True, blank=True)
    refound_order = models.IntegerField(verbose_name="退款订单", default=0, null=True, blank=True)
    false_order = models.IntegerField(verbose_name="刷单订单", default=0, null=True, blank=True)
    comment_num = models.IntegerField(verbose_name="评价总数", default=0, null=True, blank=True)
    click_amount = models.DecimalField(verbose_name="点金推广费", max_digits=10, decimal_places=2, default=0, null=True,
                                       blank=True)
    auto_click_amount = models.DecimalField(verbose_name="一站式推广费", max_digits=10, decimal_places=2, default=0,
                                            null=True, blank=True)
    turnover = models.DecimalField(verbose_name="营业额", max_digits=10, decimal_places=2, default=0, null=True,
                                   blank=True)


class DianPing(models.Model):
    """点评数据表"""
    store = models.ForeignKey(verbose_name="门店", to="Store", on_delete=models.DO_NOTHING)
    date = models.DateField(verbose_name="日期")
    Subtract_amount = models.DecimalField(verbose_name="减20后的总金额", max_digits=10, decimal_places=2, default=0,
                                          null=True, blank=True)
    video_num = models.IntegerField(verbose_name="网友视频数量(app查看)", default=0, null=True, blank=True)
    first_2_choices = (
        (0, "差评"),
        (1, "好评"),
    )
    rate_of_first_2 = models.SmallIntegerField(verbose_name="前两条评价是否是好评(app查看)", default=0, null=True,
                                               blank=True, choices=first_2_choices)
    reply_timely_choices = (
        (0, "慢"),
        (1, "快"),
        (2, "无咨询"),
    )
    reply_timely = models.SmallIntegerField(verbose_name="主观判断:咨询回复快不快(咨询必须以我方聊天为结束语)",
                                            default=2, null=True, blank=True, choices=reply_timely_choices)
    reply_manner_choices = (
        (0, "否"),
        (1, "是"),
        (2, "无咨询"),
    )
    reply_manner = models.SmallIntegerField(verbose_name="主观判断:咨询服务态度（让客户感受到热情填是或不是）", default=2,
                                            null=True, blank=True, choices=reply_manner_choices)
    meituan_order_num = models.IntegerField(verbose_name="美团订单数", default=0, null=True, blank=True)
    commented_order_num = models.IntegerField(verbose_name="点评订单数", default=0, null=True, blank=True)
    replenish_order_num = models.IntegerField(verbose_name="补单数量", default=0, null=True, blank=True)
    promotion_balance = models.DecimalField(verbose_name="推广余额", max_digits=10, decimal_places=2, default=0,
                                            null=True, blank=True)
    today_expend = models.DecimalField(verbose_name="今日花费", max_digits=10, decimal_places=2, default=0, null=True,
                                       blank=True)
    expend_every_click = models.DecimalField(verbose_name="点击均价", max_digits=10, decimal_places=2, default=0,
                                             null=True, blank=True)
    click_num = models.IntegerField(verbose_name="点击数量", default=0, null=True, blank=True)
    comment_num = models.IntegerField(verbose_name="评论数量", default=0, null=True, blank=True)
    collect_num = models.IntegerField(verbose_name="收藏数量", default=0, null=True, blank=True)
    get_discounts = models.IntegerField(verbose_name="优惠领取", default=0, null=True, blank=True)
    exposure_num = models.IntegerField(verbose_name="曝光人数", default=0, null=True, blank=True)
    visit_num = models.IntegerField(verbose_name="访问人数", default=0, null=True, blank=True)
    start_of_comment = models.DecimalField(verbose_name="点评星级", max_digits=10, decimal_places=2, default=0,
                                           null=True, blank=True)
    start_of_meituan = models.DecimalField(verbose_name="美团星级", max_digits=10, decimal_places=2, default=0,
                                           null=True, blank=True)
    online_consult_num = models.IntegerField(verbose_name="在线咨询人数", default=0, null=True, blank=True)
    exposure_transform_rate = models.FloatField(verbose_name="曝光访问转化率", default=0, null=True, blank=True)
    exposure_transform_rate_industry_mean = models.FloatField(verbose_name="曝光访问转化率(同行均值)", default=0,
                                                              null=True, blank=True)
    exposure_transform_rate_industry_max = models.FloatField(verbose_name="曝光访问转化率(同行优秀值)", default=0,
                                                             null=True, blank=True)
    intention_transform_rate = models.FloatField(verbose_name="意向转化率", default=0, null=True, blank=True)
    intention_transform_rate_industry_mean = models.FloatField(verbose_name="意向转化率(同行均值)", default=0,
                                                               null=True, blank=True)
    intention_transform_rate_industry_max = models.FloatField(verbose_name="意向转化率(同行优秀值)", default=0,
                                                              null=True, blank=True)
    new_collect_num = models.IntegerField(verbose_name="新增收藏人数", default=0, null=True, blank=True)
    total_collect_num = models.IntegerField(verbose_name="累计收藏人数", default=0, null=True, blank=True)
    new_comment_num = models.IntegerField(verbose_name="新增评价人数", default=0, null=True, blank=True)
    total_comment_num = models.IntegerField(verbose_name="累计评价人数", default=0, null=True, blank=True)
    online_consult_num_2 = models.IntegerField(verbose_name="在线咨询人数2", default=0, null=True, blank=True)
    reply_in_30_seconds_rate = models.FloatField(verbose_name="30秒回复率", default=0, null=True, blank=True)
    visit_rank_dzdp = models.IntegerField(verbose_name="访客数排名-大众点评", default=0, null=True, blank=True)
    cost_in_store_rank_dzdp = models.IntegerField(verbose_name="到店消费排名-大众点评", default=0, null=True,
                                                  blank=True)
    good_reputation_rank_dzdp = models.IntegerField(verbose_name="好评数排名-大众点评", default=0, null=True,
                                                    blank=True)
    visit_rank_mt = models.IntegerField(verbose_name="访客数排名-美团", default=0, null=True, blank=True)
    cost_in_store_rank_mt = models.IntegerField(verbose_name="到店消费排名-美团", default=0, null=True,
                                                blank=True)
    good_reputation_rank_mt = models.IntegerField(verbose_name="好评数排名-美团", default=0, null=True,
                                                  blank=True)


class Attendance(models.Model):
    """考勤记录表"""
    employee = models.ForeignKey(verbose_name="员工", to="Employee", on_delete=models.DO_NOTHING)
    store = models.ForeignKey(verbose_name="门店", to="Store", on_delete=models.DO_NOTHING)
    date = models.DateField(verbose_name="日期")
    work = models.DecimalField(verbose_name="上班时长", max_digits=4, decimal_places=2, default=0)
    status_choices = (
        (0, "全勤"),
        (1, "请假"),
        (2, "迟到"),
        (3, "旷工"),
    )
    status = models.SmallIntegerField(verbose_name="考勤状态", choices=status_choices)
    time = models.DecimalField(verbose_name="时长", max_digits=4, decimal_places=2, default=0)
    comment = models.CharField(verbose_name="备注", max_length=100, null=True, blank=True)

