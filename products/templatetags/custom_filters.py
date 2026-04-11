from django import template

register = template.Library()

@register.filter(name='cop_format')
def cop_format(value):
    """
    Convierte un número (ej: 1500000 o 1500000.00) en un formato 
    visual colombiano (ej: $ 1.500.000 COP).
    """
    try:
        # 1. Convertimos a entero para quitar decimales 
        # y formateamos internamente con comas en los miles (1,500,000)
        formatted_value = "{:,}".format(int(float(value)))
        
        # 2. Reemplazamos la coma por el punto latinoamericano (1.500.000)
        formatted_value = formatted_value.replace(',', '.')
        
        # 3. Concatenamos el símbolo de pesos y la abreviación COP
        return f"$ {formatted_value} COP"
    except (ValueError, TypeError):
        # Si por alguna razón el valor no es un número, lo devuelve tal cual
        return value
