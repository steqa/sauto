from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django import forms
from .models import Seller, Announcement


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
        label='Имя пользователя телеграм',
        max_length=32,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя телеграм',
            'autofocus': 'true',
        }))

    class Meta:
        model = Seller
        fields = ('telegram_username', 'phone_number')
        widgets = {
            'phone_number': CustomPhoneNumberPrefixWidget(initial='RU'),
        }


class AnnouncementCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-select form-control'})
        self.fields['condition'].widget.attrs.update({'class': 'form-select form-control'})
        self.fields['type_announcement'].widget.attrs.update({'class': 'form-select form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'max': 99999999999.99})
        self.fields['description'] = forms.CharField(label='Описание', max_length=3000, widget=forms.Textarea({'class': 'form-control', 'rows': 5}))

    latitude = forms.FloatField(
        label='Широта',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'hidden'
        }))

    longitude = forms.FloatField(
        label='Долгота',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'hidden'
        }))

    class Meta:
        model = Announcement
        fields = ('category', 'condition', 'type_announcement', 'name', 'price', 'description')