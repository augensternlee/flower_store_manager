# Generated by Django 4.0.6 on 2023-03-26 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flower', '0012_alter_attendance_comment_alter_dianping_store_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to='flower.store', verbose_name='门店'),
        ),
    ]