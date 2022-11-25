from django.utils.translation import gettext_lazy as _
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django import forms
from .models import Seller, AnnouncementSale


class CustomPhoneNumberPrefixWidget(PhoneNumberPrefixWidget):
    def subwidgets(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        return context['widget']['subwidgets']


class SellerCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        phone_number_widgets = self.fields['phone_number'].widget.widgets
        phone_number_widgets[0].attrs.update({'class': 'form-select'})
        phone_number_widgets[1].attrs.update({'class': 'form-control', 'placeholder': 'Номер телефона',})
    
    telegram_username = forms.EmailField(
        label=_("Telegram username"),
        max_length=32,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя Telegram',
            'autofocus': 'true',
        }))
    
    class Meta:
        model = Seller
        fields = ('telegram_username', 'phone_number')
        widgets = {
            'phone_number': CustomPhoneNumberPrefixWidget(initial='RU'),
        }


class AnnouncementSaleCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['condition'].widget.attrs.update({'class': 'form-select'})
        self.fields['type_announcement'].widget.attrs.update({'class': 'form-select'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'max': 99999999999.99})
        self.fields['description'] = forms.CharField(label='Описание', max_length=3000, widget=forms.Textarea({'class': 'form-control', 'rows': 5}))
    
    class Meta:
        model = AnnouncementSale
        fields = ('category', 'condition', 'type_announcement', 'name', 'price', 'description')