import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_number
from django import template

register = template.Library()

@register.filter(name='phone_number_country_code')
def phone_number_country_code(number):
    phone_number = phonenumbers.parse(str(number))
    return region_code_for_number(phone_number)


@register.filter(name='phone_number_without_country_code')
def phone_number_without_country_code(number):
    phone_number = phonenumbers.parse(str(number))
    return phone_number.national_number


@register.filter(name='phone_number_ru_or_international')
def phone_number_ru_or_international(number):
    phone_number = phonenumbers.parse(str(number))
    if phone_number.country_code == 7:
        ru_phone = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        ru_phone = ru_phone.split()
        ru_phone[0] = '+7'
        ru_phone = ' '.join(ru_phone)
        return ru_phone
    else:
        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)