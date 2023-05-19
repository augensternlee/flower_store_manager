import re
from django import forms
from django.core.exceptions import ValidationError
from flower.utils.bootstrap import BootstrapModelForm, BootstrapForm
from flower.utils.encypt import md5
from flower import models


class StoreModelForm(BootstrapModelForm):
    class Meta:
        model = models.Store
        fields = "__all__"


class ManagerModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = models.Manager
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_password(self):
        """密码清理函数"""
        pwd = self.cleaned_data.get("password")
        result = re.fullmatch(r'[1-9a-zA-Z_!@#]{8,12}', pwd)
        if not result:
            raise ValidationError("密码验证失败,只能使用英文字母大小写,数字,_!@#,密码位数为8至12")

        pwd = md5(pwd)
        return pwd

    def clean_confirm_password(self):
        """密码确认"""
        confirm_pwd = md5(self.cleaned_data.get("confirm_password"))
        pwd = self.cleaned_data.get("password")
        if confirm_pwd != pwd:
            raise ValidationError("密码不一致")
        return confirm_pwd


class LoginForm(BootstrapForm):
    user = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = md5(self.cleaned_data.get("password"))
        return pwd


class ManagerEditPasswdModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = models.Manager
        fields = ["user", "name", "password", "confirm_password"]
        widgets = {
            "user": forms.TextInput(attrs={'readonly': 'readonly'}),
            "name": forms.TextInput(attrs={'readonly': 'readonly'}),
            "password": forms.PasswordInput,
        }

    def clean_password(self):
        """密码清理函数"""
        pwd = self.cleaned_data.get("password")
        result = re.fullmatch(r'[1-9a-zA-Z_!@#]{8,12}', pwd)
        if not result:
            raise ValidationError("密码验证失败,只能使用英文字母大小写,数字,_!@#,密码位数为8至12")

        pwd = md5(pwd)
        user_pwd = self.instance.password
        if pwd == user_pwd:
            raise ValidationError("不能设置与之前相同的密码")
        return pwd

    def clean_confirm_password(self):
        """密码确认"""
        confirm_pwd = md5(self.cleaned_data.get("confirm_password"))
        pwd = self.cleaned_data.get("password")
        if confirm_pwd != pwd:
            raise ValidationError("密码不一致")
        return confirm_pwd



class VipAddModelForm(BootstrapModelForm):
    class Meta:
        model = models.Vip
        fields = "__all__"

    def clean_tel(self):
        """验证手机号码"""
        phone_num = self.cleaned_data.get("tel")
        result = re.fullmatch(r"1\d{10}", phone_num)

        if not result:
            raise ValidationError("手机号码验证不通过")
        return phone_num


class VipTopupModelForm(BootstrapModelForm):
    class Meta:
        model = models.VipCost
        fields = "__all__"
        widgets = {
            "vip_num": forms.NumberInput(attrs={'readonly': 'readonly'}),
            "type": forms.NumberInput(attrs={'readonly': 'readonly'})
        }


class DateSelectForm(BootstrapForm):
    start_date = forms.DateField(
        label="",
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'autocomplete': 'off',
                'text-align': 'center',
                'onkeydown': "if (event.keyCode == 8 || event.keyCode == 46) this.value='';"
            }),
        required=False,
    )
    end_date = forms.DateField(
        label="",
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'autocomplete': 'off',
                'onkeydown': "if (event.keyCode == 8 || event.keyCode == 46) this.value='';"
            }),
        required=False,
    )


class OrderAddModelForm(BootstrapModelForm):
    exclude_field_list = ["goods_image", "product_image"]

    class Meta:
        model = models.Order
        fields = "__all__"
        # exclude = ["store"]
        widgets = {
            "send": forms.DateInput(attrs={"type": "datetime-local"}, format="%Y-%m-%d %H:%I:%S"),
        }

    def clean_orderer_tel(self):
        """验证手机号码"""
        phone_num = self.cleaned_data.get("orderer_tel")
        result = re.fullmatch(r"1\d{10}", phone_num)

        if not result:
            raise ValidationError("手机号码验证不通过")
        return phone_num

    def clean_consignee_tel(self):
        """验证手机号码"""
        phone_num = self.cleaned_data.get("consignee_tel")
        result = re.fullmatch(r"1\d{10}", phone_num)

        if not result:
            raise ValidationError("手机号码验证不通过")
        return phone_num

    def clean_amount(self):
        """验证总金额"""
        num = self.cleaned_data.get("amount")
        result = re.fullmatch(r"\d+(\.\d+)?", str(num))

        if not result:
            raise ValidationError("金额错误")
        return num

    def clean_paid(self):
        """验证支付金额"""
        num = self.cleaned_data.get("paid")
        result = re.fullmatch(r"\d+(\.\d+)?", str(num))

        if not result:
            raise ValidationError("金额错误")
        if num > self.cleaned_data.get("amount"):
            raise ValidationError("支付金额不能大于总金额")
        return num

    def clean_unpaid(self):
        """验证未支付金额"""
        num = self.cleaned_data.get("unpaid")
        result = re.fullmatch(r"\d+(\.\d+)?", str(num))

        if not result:
            raise ValidationError("金额错误")
        if num != self.cleaned_data.get("amount") - self.cleaned_data.get("paid"):
            raise ValidationError("未支付金额错误")
        return num


class OrderEditModelForm(OrderAddModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"
        # exclude = ["store", "product_type"]
        widgets = {
            "amount": forms.NumberInput(attrs={"readonly": "readonly"}),
            "send": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%d %H:%I:%S")
        }


class OrderDetailModelForm(BootstrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["goods_image", "product_image"]


class MeiTuanModelForm(BootstrapModelForm):
    class Meta:
        model = models.MeiTuan
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }


class DianPingModelForm(BootstrapModelForm):
    class Meta:
        model = models.DianPing
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }


class AttendanceModelForm(BootstrapModelForm):
    class Meta:
        model = models.Attendance
        fields = "__all__"
        widgets = {
            # "date": forms.DateInput(attrs={"type": "date"}),
            "date": forms.DateTimeInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        store = kwargs.pop('store')
        super().__init__(*args, **kwargs)
        self.fields['store'].initial = store
        # 重写员工选择字段，使用当前部门的员工列表作为选项
        self.fields['employee'] = forms.ModelChoiceField(
            queryset=models.Employee.objects.filter(store_id=store),
            empty_label=None)
        if self.fields['employee'].widget.attrs:
            self.fields['employee'].widget.attrs["class"] = "form-control"
        else:
            self.fields['employee'].widget.attrs = {
                "class": "form-control",
                "placeholder": self.fields['employee'].label
            }
