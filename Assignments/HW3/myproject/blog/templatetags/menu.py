from typing import Any

from django import template

from blog.models import (
    Category,
)

register: template.Library = template.Library()


@register.inclusion_tag('blog/menu_tpl.html')
def show_menu(menu_class: str = 'menu') -> dict[str, Any]:  # noqa
    categories = Category.objects.all()
    return {"categories": categories, "menu_class": menu_class}