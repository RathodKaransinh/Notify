from django import template

VIEW_NAMES = {
    1: ['view_keywords'],
    2: ['list_notices', 'upload'],
    3: ['add_items'],
    4: ['dashboard'],
}

register = template.Library()


@register.simple_tag
def get_menu_active_status(request, *keys):
    resolver_match = request.resolver_match
    view_name = resolver_match.view_name

    view_names_list = []
    for key in keys:
        view_names_list += VIEW_NAMES[key]

    if view_name in view_names_list:
        return 'active'

    return ''
