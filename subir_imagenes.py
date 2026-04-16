import os
import django

# Conectar al ecosistema de tu proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TecLegacy.settings')
django.setup()

from django.core.files.base import ContentFile
from products.models import Product, Category

def subir():
    print("Iniciando conexión. Preparando fotos...")
    
    # Repasamos todos los productos de tu Base de Datos actual
    for prod in Product.objects.all():
        if prod.image:
            # 1. Buscamos en tu disco duro si existe la imagen en tu carpeta media/
            # Ej: Buscamos "C:/Users/.../media/products/mouse.jpg"
            ruta_local = os.path.join('media', str(prod.image).replace('\\', '/').split('/')[-1])
            if not os.path.exists(ruta_local):
                 ruta_local = os.path.join('media', 'products', str(prod.image).replace('\\', '/').split('/')[-1])

            if os.path.exists(ruta_local):
                print(f"Subiendo a Cloudinary el archivo real: {prod.name}")
                with open(ruta_local, 'rb') as archivo:
                    # 2. Si Django cree que está en modo Cloudinary (DEBUG=False), 
                    # esto volará por internet y guardará su URL.
                    prod.image.save(os.path.basename(ruta_local), ContentFile(archivo.read()), save=True)
            else:
                print(f"No hallé en disco duro la de: {prod.name}")

if __name__ == '__main__':
    subir()
    print("El código ha terminado.")
