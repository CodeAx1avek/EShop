from django import template

register = template.Library()


@register.filter(name = 'currency_rupeee')
def currency_rupeee(number):
            return "₹" +str(number)
