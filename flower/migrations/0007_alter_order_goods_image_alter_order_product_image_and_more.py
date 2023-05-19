# Generated by Django 4.0.6 on 2023-03-24 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flower', '0006_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='goods_image',
            field=models.FileField(blank=True, null=True, upload_to='media/goods/', verbose_name='订单照片'),
        ),
        migrations.AlterField(
            model_name='order',
            name='product_image',
            field=models.FileField(blank=True, null=True, upload_to='media/product/', verbose_name='成品照片'),
        ),
        migrations.AlterField(
            model_name='order',
            name='vip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='flower.vip', verbose_name='会员卡编号'),
        ),
    ]
