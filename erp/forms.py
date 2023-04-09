from django import forms
from .models import *


# 제품 form
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'code', 'size', 'inbound_price', 'price', 'description']


# 입고 form
class InboundForm(forms.ModelForm):
    class Meta:
        model = Inbound
        fields = ['product', 'quantity']


# 출고 form
class OutboundForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = ['product', 'quantity']