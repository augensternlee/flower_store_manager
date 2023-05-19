# Generated by Django 4.0.6 on 2023-03-22 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flower', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('level', models.SmallIntegerField(choices=[(0, 'boss'), (1, '店长'), (2, '员工')], verbose_name='级别')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flower.store', verbose_name='所属门店')),
            ],
        ),
    ]