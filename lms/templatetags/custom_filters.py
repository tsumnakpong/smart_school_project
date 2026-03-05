# lms/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='dict_get')
def dict_get(dictionary, key):
    """ดึงค่าจาก dictionary ด้วย key ใน template"""
    return dictionary.get(key)