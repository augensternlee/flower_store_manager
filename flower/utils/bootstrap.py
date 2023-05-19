from django import forms


class Boostrap():
    exclude_field_list = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # 字段中有属性，保留原来的属性，没有属性，才增加。
            if name in self.exclude_field_list:
                continue
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }


class BootstrapModelForm(Boostrap, forms.ModelForm):
    pass


class BootstrapForm(Boostrap, forms.Form):
    pass
