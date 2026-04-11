import json
import os
import google.generativeai as genai
from django.http import JsonResponse
from products.models import Product, Category
from .models import ChatbotQuery

# --- CAPA DE ABSTRACCIÓN (IA) ---
def get_ai_response(user_query, catalog_context):
    """
    Función modular para obtener respuestas de la IA.
    Diseñada para ser escalable: si quieres cambiar de IA en el futuro,
    solo tienes que modificar este bloque.
    """
    try:
        # Cargar API Key desde el entorno
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "Error de configuración: GEMINI_API_KEY no encontrada."

        # Configurar y llamar al modelo
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-flash-latest')

        # Instrucciones de comportamiento para la IA
        system_instruction = f"""
        Eres 'TecBot', el asistente virtual experto de 'TecLegacy'. 
        Tu personalidad es amable, profesional y gamer.
        
        CATÁLOGO ACTUAL DE PRODUCTOS (Usa esto como única referencia):
        {catalog_context}
        
        REGLAS:
        - Responde de forma amable y concisa.
        - Evita saludar y presentarte repetitivamente en cada respuesta. Ve directo al grano manteniendo el tono amable solo saluda al inicio de la conversación o en caso de que el usuario lo requiera.
        - NUNCA uses Markdown (como ** para negritas). Usa SÓLO etiquetas HTML si necesitas resaltar algo (ejemplo: <b>texto</b>).
        - Solo recomienda productos que existan en el catálogo de arriba.
        - Cuando menciones un producto, crea un enlace HTML usando este formato: <a href="/products/SLUG_CATEGORIA/SLUG_PRODUCTO/">NOMBRE_PRODUCTO</a>.
        - Si el usuario pregunta por algo que no tenemos, sugiere ver las categorías generales.
        """

        # Enviar el contexto y la duda del usuario
        response = model.generate_content(f"{system_instruction}\n\nCliente: {user_query}")
        return response.text

    except Exception as e:
        # Detectar si es un error de cuota (Rate Limit / Quota Exceeded)
        error_msg = str(e).lower()
        if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:
            return "Lo siento, he superado mi límite de consultas gratuitas por este momento. Por favor, inténtalo de nuevo en unos minutos."
        
        return f"Interferencia en el sistema: {str(e)}"


# --- VISTA PRINCIPAL (Django) ---
def chatbot_query(request):
    """Punto de entrada de la API del Chatbot."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '')

            # 1. Extraer catálogo real de la DB (Datos vivos con Slugs para links)
            products = Product.objects.filter(is_available=True)
            catalog_summary = ""
            for p in products:
                catalog_summary += f"- {p.name}: ${p.price} | Cat: {p.category.name} | URL: /products/{p.category.slug}/{p.slug}/\n"

            # 2. Obtener respuesta inteligente
            bot_response = get_ai_response(query, catalog_summary)

            # 3. Guardar en el historial
            ChatbotQuery.objects.create(query=query, response=bot_response)

            return JsonResponse({
                'success': True,
                'response': bot_response
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})
