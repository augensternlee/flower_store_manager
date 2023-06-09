# Generated by Django 4.0.6 on 2023-03-25 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flower', '0008_alter_order_send'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='goods_image',
            field=models.ImageField(blank=True, null=True, upload_to='goods/', verbose_name='订单照片'),
        ),
        migrations.AlterField(
            model_name='order',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to='product/', verbose_name='成品照片'),
        ),
        migrations.CreateModel(
            name='MeiTuan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日期')),
                ('comming_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='进店人数')),
                ('order_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='下单人数')),
                ('transform_rate', models.FloatField(blank=True, default=0, null=True, verbose_name='入店转化率')),
                ('total_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='总流量')),
                ('click_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='点金次数')),
                ('auto_click_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='一站式点击')),
                ('natural_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='自然流量')),
                ('total_order', models.IntegerField(blank=True, default=0, null=True, verbose_name='所有订单')),
                ('real_order', models.IntegerField(blank=True, default=0, null=True, verbose_name='真实订单')),
                ('refound_order', models.IntegerField(blank=True, default=0, null=True, verbose_name='退款订单')),
                ('false_order', models.IntegerField(blank=True, default=0, null=True, verbose_name='刷单订单')),
                ('comment_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='评价总数')),
                ('click_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='点金推广费')),
                ('auto_click_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='一站式推广费')),
                ('turnover', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='营业额')),
                ('store_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='flower.store', verbose_name='门店编号')),
            ],
        ),
        migrations.CreateModel(
            name='DianPing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日期')),
                ('Subtract_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='减20后的总金额')),
                ('video_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='网友视频数量(app查看)')),
                ('rate_of_first_2', models.SmallIntegerField(blank=True, choices=[(0, '差评'), (1, '好评')], default=0, null=True, verbose_name='前两条评价是否是好评(app查看)')),
                ('reply_timely', models.SmallIntegerField(blank=True, choices=[(0, '慢'), (1, '快'), (2, '无咨询')], default=2, null=True, verbose_name='主观判断:咨询回复快不快(咨询必须以我方聊天为结束语)')),
                ('reply_manner', models.SmallIntegerField(blank=True, choices=[(0, '否'), (1, '是'), (2, '无咨询')], default=2, null=True, verbose_name='主观判断:咨询服务态度（让客户感受到热情填是或不是）')),
                ('meituan_order_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='美团订单数')),
                ('commented_order_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='点评订单数')),
                ('replenish_order_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='补单数量')),
                ('promotion_balance', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='推广余额')),
                ('today_expend', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='今日花费')),
                ('expend_every_click', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='点击均价')),
                ('click_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='点击数量')),
                ('comment_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='评论数量')),
                ('collect_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='收藏数量')),
                ('get_discounts', models.IntegerField(blank=True, default=0, null=True, verbose_name='优惠领取')),
                ('exposure_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='曝光人数')),
                ('visit_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='访问人数')),
                ('start_of_comment', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='点评星级')),
                ('start_of_meituan', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='美团星级')),
                ('online_consult_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='在线咨询人数')),
                ('exposure_transform_rate', models.FloatField(blank=True, default=0, null=True, verbose_name='曝光访问转化率')),
                ('exposure_transform_rate_industry_mean', models.FloatField(blank=True, default=0, null=True, verbose_name='曝光访问转化率(同行均值)')),
                ('exposure_transform_rate_industry_max', models.FloatField(blank=True, default=0, null=True, verbose_name='曝光访问转化率(同行优秀值)')),
                ('intention_transform_rate', models.FloatField(blank=True, default=0, null=True, verbose_name='意向转化率')),
                ('intention_transform_rate_industry_mean', models.FloatField(blank=True, default=0, null=True, verbose_name='意向转化率(同行均值)')),
                ('intention_transform_rate_industry_max', models.FloatField(blank=True, default=0, null=True, verbose_name='意向转化率(同行优秀值)')),
                ('new_collect_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='新增收藏人数')),
                ('total_collect_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='累计收藏人数')),
                ('new_comment_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='新增评价人数')),
                ('total_comment_num', models.IntegerField(blank=True, default=0, null=True, verbose_name='累计评价人数')),
                ('online_consult_num_2', models.IntegerField(blank=True, default=0, null=True, verbose_name='在线咨询人数2')),
                ('reply_in_30_seconds_rate', models.FloatField(blank=True, default=0, null=True, verbose_name='30秒回复率')),
                ('visit_rank_dzdp', models.IntegerField(blank=True, default=0, null=True, verbose_name='访客数排名-大众点评')),
                ('cost_in_store_rank_dzdp', models.IntegerField(blank=True, default=0, null=True, verbose_name='到店消费排名-大众点评')),
                ('good_reputation_rank_dzdp', models.IntegerField(blank=True, default=0, null=True, verbose_name='好评数排名-大众点评')),
                ('visit_rank_mt', models.IntegerField(blank=True, default=0, null=True, verbose_name='访客数排名-美团')),
                ('cost_in_store_rank_mt', models.IntegerField(blank=True, default=0, null=True, verbose_name='到店消费排名-美团')),
                ('good_reputation_rank_mt', models.IntegerField(blank=True, default=0, null=True, verbose_name='好评数排名-美团')),
                ('store_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='flower.store', verbose_name='门店编号')),
            ],
        ),
    ]
