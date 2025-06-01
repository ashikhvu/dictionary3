from django import template

register = template.Library()

@register.filter
def range_fn(value,arg):
    return range(value,arg+1)

@register.filter
def add(val,arg):
    print(f"{val} ----{arg}-------{val+arg}")
    return val+arg

@register.filter
def cropfront(val,arg):
    return val[arg:]

@register.filter
def cropback(val,arg):
    return val[:arg]