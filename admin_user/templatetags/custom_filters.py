# Importa el módulo template de Django para crear filtros de plantilla personalizados
from django import template

# Registra una instancia de la biblioteca de plantillas
register = template.Library()

# Filtro de plantilla personalizado para obtener el valor de una clave en un diccionario
@register.filter
def dict_key(value, key):
    return value.get(key)

# Filtro de plantilla personalizado para contar la cantidad de elementos en una fase específica dentro de los datos del mes
@register.filter
def get_phase_count(month_data, phase):
    for item in month_data:
        if item['phase'] == phase:
            return item['count']
    return 0