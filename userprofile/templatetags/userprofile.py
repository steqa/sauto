from django import template

register = template.Library()

@register.filter(name='idna_decode')
def idna_decode(value):
    return value.encode().decode('idna')