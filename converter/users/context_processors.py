
from converter_app.views import menu

def get_menu_context(request):
    return {'mainmenu': menu}