import json
from datetime import datetime

from decimal import Decimal
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponse

from django.utils.translation import get_language


# Global Variables

NOMBRE_INSTITUCION = 'HOP Contracting'

DEFAULT_PASSWORD = 'hop'

# USERS GROUPS
USER_GROUP_ADMINISTRATOR_ID = 1
USER_GROUP_PROJECT_MANAGER_ID = 2
USER_GROUP_PROJECT_SUPERVISOR_ID = 3
USER_GROUP_PROJECT_TECHNICIAN_ID = 4

EVALUATION_TYPES = (
    (1, 'Bad'),
    (2, 'Regular'),
    (3, 'Good'),
    (4, 'Very Good'),
    (5, 'Excellent')
)


def generate_file_name(nombre, original):
    ext = ""
    if original.find(".") > 0:
        ext = original[original.rfind("."):]
    fecha = datetime.now().date()
    hora = datetime.now().time()
    return nombre + fecha.year.__str__() + fecha.month.__str__() + fecha.day.__str__() + \
           hora.hour.__str__() + hora.minute.__str__() + hora.second.__str__() + ext


class MiPaginator(Paginator):

    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, range=5):
        super(MiPaginator, self).__init__(object_list,
                                          per_page,
                                          orphans=orphans,
                                          allow_empty_first_page=allow_empty_first_page)
        self.range = range
        self.pages = []
        self.first_page = False
        self.last_page = False

    def pages_range(self, page):
        left = page - self.range
        right = page + self.range
        if left < 1:
            left = 1
        if right > self.num_pages:
            right = self.num_pages
        self.pages = range(left, right + 1)
        self.first_page = True if left > 1 else False
        self.last_page = True if right < self.num_pages else False
        self.ellipsis_left = left - 1
        self.ellipsis_right = right + 1


def convertir_fecha(s):
    try:
        return datetime(int(s[-4:]), int(s[3:5]), int(s[:2]))
    except:
        return datetime.now()


def convertir_fecha_month_first(s):
    try:
        return datetime(int(s[-4:]), int(s[:2]), int(s[3:5]))
    except:
        return datetime.now()


def convertir_time(time):
    """
        t: array of integers 0-hour 1-minute
    """
    d = datetime.now().date()
    t = time.split(':')
    return datetime(d.year, d.month, d.day, int(t[0]), int(t[1]))


def model_to_dict_safe(m, exclude=None):
    if not exclude:
        exclude = []
    d = model_to_dict(m, exclude=exclude)
    for x, y in d.iteritems():
        if type(y) == Decimal:
            d[x] = float(y)
    return d


def url_back(request, mensaje=None):
    url = request.META['HTTP_REFERER'].split('/')[-1:][0]
    if 'mensj=' in url:
        url = url[:(url.find('mensj') - 1)]
    if mensaje:
        if '?' in url:
            url += "&mensj=" + mensaje
        else:
            url += "?mensj=" + mensaje
    return url



def bad_json(message=None, error=None, extradata=None):
    """
        Returns an invalid response on json data
    """
    data = {'result': 'bad'}
    lang = get_language()

    if message:
        data.update({'msg': message})
    if error:
        if error == 0:
            data.update({"msg": bad_request(lang)})
        elif error == 1:
            data.update({"msg": error_saving_data(lang)})
        elif error == 2:
            data.update({"msg": error_updating_data(lang)})
        elif error == 3:
            data.update({"msg": error_deleting_data(lang)})
        elif error == 4:
            data.update({"msg": no_permission(lang)})
        elif error == 5:
            data.update({"msg": error_generating_information(lang)})
        else:
            data.update({"msg": system_error(lang)})
    if extradata:
        data.update(extradata)
    return HttpResponse(json.dumps(data), content_type="application/json")


def ok_json(data=None):
    """
        Returns a valid response on json data
    """
    if data:
        if type(data) == dict and 'result' not in data.keys():
            data.update({"result": "ok"})
    else:
        data = {"result": "ok"}
    return HttpResponse(json.dumps(data), content_type="application/json")


def bad_request(lang='en'):
    if lang == 'en':
        message = 'Bad request'
    elif lang == 'es':
        message = 'Solicitud incorrecta'
    else:
        message = ""
    return message


def error_saving_data(lang='en'):
    if lang == 'en':
        message = 'Error saving data'
    elif lang == 'es':
        message = 'Error al guardar datos'
    else:
        message = ""
    return message


def error_updating_data(lang='en'):
    if lang == 'en':
        message = 'Error updating data'
    elif lang == 'es':
        message = 'Error al actualizar datos'
    else:
        message = ""
    return message


def error_deleting_data(lang='en'):
    if lang == 'en':
        message = 'Error deleting data'
    elif lang == 'es':
        message = 'Error al eliminar datos'
    else:
        message = ""
    return message


def no_permission(lang='en'):
    if lang == 'en':
        message = 'You do not have permission to perform this action'
    elif lang == 'es':
        message = 'Usted no tiene permiso para realizar esta acción'
    else:
        message = ""
    return message


def error_generating_information(lang='en'):
    if lang == 'en':
        message = 'Error generating the information'
    elif lang == 'es':
        message = 'Error al generar la información'
    else:
        message = ""
    return message


def system_error(lang='en'):
    if lang == 'en':
        message = 'System error'
    elif lang == 'es':
        message = 'Error del sistema'
    else:
        message = ""
    return message
