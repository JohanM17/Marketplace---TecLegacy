# 📚 GUÍA COMPLETA DE ESTUDIO - PROYECTO TECLEGACY

## 🎯 ÍNDICE
1. [¿Qué es este proyecto?](#qué-es-este-proyecto)
2. [Comandos para iniciar el proyecto](#comandos-para-iniciar-el-proyecto)
3. [Entornos Virtuales - ¿Qué es .venv o env_django?](#entornos-virtuales)
4. [Fundamentos de Python](#fundamentos-de-python)
5. [Fundamentos de Django](#fundamentos-de-django)
6. [Arquitectura del Proyecto TecLegacy](#arquitectura-del-proyecto)
7. [Explicación del Código](#explicación-del-código)
8. [¿Qué le falta al proyecto?](#qué-le-falta-al-proyecto)
9. [Mejoras para tu portafolio](#mejoras-para-tu-portafolio)

---

## 🎮 ¿QUÉ ES ESTE PROYECTO?

**TecLegacy** es un e-commerce (tienda online) de productos tecnológicos gaming desarrollado con Django 5.1 y Python 3.12.

### Funcionalidades principales:
- 🛒 Carrito de compras (para usuarios autenticados e invitados)
- 👤 Sistema de usuarios (registro, login, perfiles)
- 📦 Catálogo de productos con categorías
- 🤖 Chatbot inteligente para buscar productos
- 💳 Sistema de órdenes y pagos
- 🔐 Panel de administración

---

## 🚀 COMANDOS PARA INICIAR EL PROYECTO

### **Paso 1: Abrir PowerShell y navegar al proyecto**
```powershell
cd C:\Users\CODEBOOK\PycharmProjects\TecLegacy
```

### **Paso 2: Activar el entorno virtual**
```powershell
.\env_django\Scripts\Activate.ps1
```
**Verás** `(env_django)` al inicio de la línea cuando esté activado.

**Si da error de permisos:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Paso 3: Asegurarte de que MySQL esté corriendo**
- Abre XAMPP/WAMP o inicia el servicio MySQL
- El proyecto necesita que MySQL esté encendido

### **Paso 4: Crear la base de datos (solo la primera vez)**
```sql
-- Entra a MySQL
mysql -u root -p

-- Crea la base de datos
CREATE DATABASE teclegacy_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Sal
exit;
```

### **Paso 5: Aplicar migraciones (crear tablas)**
```powershell
python manage.py migrate
```

### **Paso 6: Crear superusuario (solo la primera vez)**
```powershell
python manage.py createsuperuser
```
Te pedirá: username, email, password

### **Paso 7: Ejecutar el servidor**
```powershell
python manage.py runserver
```

### **Paso 8: Abrir en el navegador**
- Página principal: http://127.0.0.1:8000/
- Panel admin: http://127.0.0.1:8000/admin/

### **Para detener el servidor:**
```
Ctrl + C
```

---

## 📦 ENTORNOS VIRTUALES

### ¿Qué es un entorno virtual?
Es una carpeta (en tu caso `env_django/`) que contiene:
- Una copia de Python
- Todas las librerías instaladas con `pip` (Django, Pillow, etc.)
- Está **aislado** del Python del sistema

### ¿Por qué usar entornos virtuales?
```
❌ SIN entorno virtual:
   - Proyecto A necesita Django 3.2
   - Proyecto B necesita Django 5.1
   - CONFLICTO: Solo puedes tener una versión instalada

✅ CON entorno virtual:
   - Proyecto A tiene su propio env con Django 3.2
   - Proyecto B tiene su propio env con Django 5.1
   - Sin problemas, cada uno usa su versión
```

### Estructura del entorno virtual:
```
env_django/
├── Scripts/           # Ejecutables (Windows)
│   ├── activate       # Para Bash
│   ├── Activate.ps1   # Para PowerShell ← Usas este
│   ├── python.exe     # Python del entorno
│   └── pip.exe        # Para instalar paquetes
├── Lib/
│   └── site-packages/ # Aquí se instalan Django, Pillow, etc.
└── pyvenv.cfg         # Configuración
```

### Comandos útiles:
```powershell
# Activar
.\env_django\Scripts\Activate.ps1

# Desactivar
deactivate

# Ver paquetes instalados
pip list

# Instalar paquetes
pip install nombre_paquete

# Instalar desde requirements.txt
pip install -r requirements.txt

# Guardar paquetes instalados
pip freeze > requirements.txt
```

---

## 🐍 FUNDAMENTOS DE PYTHON

### 1. Variables y Tipos de Datos
```python
# Python es tipado dinámico (no declaras el tipo)
nombre = "TecLegacy"         # str - cadena de texto
precio = 99.99               # float - decimal
stock = 10                   # int - entero
disponible = True            # bool - booleano
productos = []               # list - lista
configuracion = {}           # dict - diccionario
nulo = None                  # NoneType - nulo
```

### 2. Funciones
```python
# Función básica
def saludar(nombre):
    return f"Hola {nombre}"

# Función con parámetros por defecto
def calcular_precio(precio, descuento=0):
    return precio - (precio * descuento / 100)

# Llamar función
total = calcular_precio(100, 10)  # 90.0
```

**En tu proyecto (cart/views.py):**
```python
def _get_or_create_cart(request):
    """Función auxiliar para obtener o crear un carrito."""
    # El _ al inicio indica función "privada" (convención)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart
```

### 3. Clases y Objetos (POO)
```python
class Producto:
    # Constructor
    def __init__(self, nombre, precio):
        self.nombre = nombre    # Atributo
        self.precio = precio
    
    # Método
    def calcular_total(self, cantidad):
        return self.precio * cantidad
    
    # Método especial
    def __str__(self):
        return self.nombre

# Crear objeto
p = Producto("Teclado", 50)
print(p)  # "Teclado"
total = p.calcular_total(2)  # 100
```

### 4. Listas
```python
productos = ["Teclado", "Mouse", "Monitor"]

# Acceder
print(productos[0])  # "Teclado"

# Agregar
productos.append("Auriculares")

# Iterar
for producto in productos:
    print(producto)

# List comprehension (Pythónico)
precios = [100, 200, 300]
con_iva = [p * 1.19 for p in precios]  # [119.0, 238.0, 357.0]
```

### 5. Diccionarios
```python
usuario = {
    'nombre': 'Johan',
    'edad': 22,
    'ciudad': 'Bogotá'
}

# Acceder
print(usuario['nombre'])        # "Johan"
print(usuario.get('edad'))      # 22

# Agregar/modificar
usuario['email'] = 'johan@example.com'

# Iterar
for clave, valor in usuario.items():
    print(f"{clave}: {valor}")
```

**En tu proyecto (chatbot/views.py):**
```python
category_keywords = {
    'portatil': 'Portátiles Gaming',
    'laptop': 'Portátiles Gaming',
    'teclado': 'Periféricos',
    'mouse': 'Periféricos',
}
```

### 6. Condicionales
```python
if precio > 1000:
    print("Producto caro")
elif precio > 500:
    print("Precio medio")
else:
    print("Económico")

# Operador ternario
mensaje = "Caro" if precio > 1000 else "Económico"
```

### 7. Importaciones
```python
# Importar módulo completo
import os

# Importar función específica
from django.shortcuts import render

# Importar con alias
from django.db import models as m

# Importar todo (no recomendado)
from django.shortcuts import *
```

---

## 🌐 FUNDAMENTOS DE DJANGO

### ¿Qué es Django?
Django es un **framework web** de Python que sigue el patrón **MVT** (Model-View-Template):

```
┌─────────────────────────────────────┐
│        PATRÓN MVT DE DJANGO         │
├─────────────────────────────────────┤
│                                     │
│  MODEL (models.py)                  │
│  ↓ Define estructura de datos      │
│  ↓ Interactúa con la BD             │
│                                     │
│  VIEW (views.py)                    │
│  ↓ Lógica de negocio                │
│  ↓ Procesa peticiones HTTP          │
│                                     │
│  TEMPLATE (.html)                   │
│  ↓ Interfaz de usuario              │
│  ↓ HTML con sintaxis Django         │
│                                     │
│  URL (urls.py)                      │
│  ↓ Enrutamiento                     │
│  ↓ Conecta URLs con vistas          │
└─────────────────────────────────────┘
```

### Flujo de una petición:
```
1. Usuario visita: http://localhost:8000/products/teclado-gaming/
                                ↓
2. Django busca en urls.py
   TecLegacy/urls.py → include('products.urls')
                                ↓
3. products/urls.py encuentra la ruta
   path('<slug:product_slug>/', views.product_detail)
                                ↓
4. Ejecuta la vista: products/views.py → product_detail()
   - Consulta la BD (Model)
   - Prepara datos (context)
                                ↓
5. Renderiza template: product_detail.html
   - Reemplaza {{ variables }} con datos
                                ↓
6. Retorna HTML al navegador
```

### ORM de Django (Mapeo Objeto-Relacional)
El ORM traduce código Python a SQL automáticamente:

```python
# Python (ORM)
Product.objects.filter(price__lt=1000)

# SQL generado
SELECT * FROM products_product WHERE price < 1000;
```

**Operaciones CRUD:**
```python
# CREATE - Crear
Product.objects.create(name="Teclado", price=50)

# READ - Leer
Product.objects.all()                  # Todos
Product.objects.get(id=1)              # Uno (debe existir)
Product.objects.filter(price__gte=100) # Filtrar
Product.objects.exclude(stock=0)       # Excluir

# UPDATE - Actualizar
product = Product.objects.get(id=1)
product.price = 75
product.save()

# DELETE - Eliminar
product.delete()
```

**Lookups (filtros):**
```python
__exact       # Exacto
__iexact      # Exacto (sin importar mayúsculas)
__contains    # Contiene
__icontains   # Contiene (case-insensitive)
__gt          # Mayor que (>)
__gte         # Mayor o igual (>=)
__lt          # Menor que (<)
__lte         # Menor o igual (<=)
__in          # En una lista
__startswith  # Empieza con
```

**Ejemplos de tu proyecto:**
```python
# products/views.py
products = Product.objects.filter(is_available=True)

# Filtrar por categoría
products = Product.objects.filter(category__slug='laptops')

# Búsqueda
from django.db import models
products = Product.objects.filter(
    models.Q(name__icontains='gaming') |
    models.Q(description__icontains='gaming')
)
```

### Relaciones entre Modelos

**1. ForeignKey (Muchos a Uno)**
```python
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Un producto pertenece a UNA categoría
    # Una categoría puede tener MUCHOS productos
```

**Uso:**
```python
product.category           # Obtener la categoría del producto
category.products.all()    # Todos los productos de la categoría
```

**2. OneToOneField (Uno a Uno)**
```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Un perfil pertenece a UN usuario
    # Un usuario tiene UN perfil
```

**Uso:**
```python
user.profile              # Perfil del usuario
profile.user              # Usuario del perfil
```

**3. on_delete opciones:**
```python
CASCADE      # Si se elimina el padre, elimina el hijo
PROTECT      # Impide eliminar si tiene hijos
SET_NULL     # Establece NULL (requiere null=True)
SET_DEFAULT  # Valor por defecto
```

---

## 🏗️ ARQUITECTURA DEL PROYECTO

### Estructura de carpetas:
```
TecLegacy/
│
├── manage.py              # CLI de Django (comandos)
│
├── TecLegacy/             # Configuración del proyecto
│   ├── settings.py        # Configuración (BD, apps, etc.)
│   ├── urls.py            # URLs principales
│   ├── wsgi.py            # Servidor para producción
│   └── asgi.py            # Servidor asíncrono
│
├── products/              # App de productos
│   ├── models.py          # Product, Category
│   ├── views.py           # Lógica de negocio
│   ├── urls.py            # Rutas de productos
│   ├── admin.py           # Config del admin
│   └── templates/         # HTML de productos
│
├── cart/                  # App de carrito
│   ├── models.py          # Cart, Order, etc.
│   ├── views.py           # Lógica del carrito
│   └── context_processors.py # Variables globales
│
├── users/                 # App de usuarios
│   ├── models.py          # Profile
│   ├── views.py           # Login, registro
│   └── forms.py           # Formularios
│
├── chatbot/               # App de chatbot
│   ├── models.py          # ChatbotQuery
│   └── views.py           # Lógica del chatbot
│
├── templates/             # Templates globales
│   ├── base.html          # Plantilla base
│   ├── navbar.html        # Navegación
│   └── footer.html        # Pie de página
│
├── static/                # CSS, JS, imágenes
├── media/                 # Archivos subidos
├── env_django/            # Entorno virtual
├── requirements.txt       # Dependencias
└── archivo.env            # Variables de entorno
```

### ¿Qué es una App en Django?
```
PROYECTO (TecLegacy)
└─ Contiene múltiples APPS
   ├─ products (catálogo)
   ├─ cart (carrito)
   ├─ users (usuarios)
   └─ chatbot (asistente)
```

**Filosofía Django**: "Una app debería hacer una cosa y hacerla bien"

---

## 📝 EXPLICACIÓN DEL CÓDIGO

### 1. MODELS.PY - Estructura de Datos

#### Product Model (products/models.py)
```python
class Product(models.Model):
    # ForeignKey: Relación muchos a uno
    category = models.ForeignKey(
        Category,                    # Modelo relacionado
        related_name='products',     # category.products.all()
        on_delete=models.CASCADE     # Si se elimina categoría, elimina productos
    )
    
    # CharField: Texto corto
    name = models.CharField(max_length=200)
    
    # SlugField: URL amigable (teclado-gaming-rgb)
    slug = models.SlugField(max_length=200, unique=True)
    
    # ImageField: Para subir imágenes
    image = models.ImageField(upload_to='products/')
    
    # TextField: Texto largo
    description = models.TextField(blank=True)  # blank=True: opcional
    
    # DecimalField: Para dinero (mejor que Float)
    price = models.DecimalField(
        max_digits=10,      # Total de dígitos
        decimal_places=2    # Decimales (12345678.99)
    )
    
    # PositiveIntegerField: Solo positivos
    stock = models.PositiveIntegerField(default=1)
    
    # BooleanField: True/False
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # DateTimeField
    created_at = models.DateTimeField(auto_now_add=True)  # Al crear
    updated_at = models.DateTimeField(auto_now=True)      # Al actualizar
    
    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['-created_at']  # Orden descendente
    
    def __str__(self):
        # Cómo se muestra el objeto
        return self.name
    
    def get_absolute_url(self):
        # URL del producto
        return reverse('products:product_detail', 
                      args=[self.category.slug, self.slug])
```

#### Cart Models (cart/models.py)
```python
class Cart(models.Model):
    # Para usuarios autenticados
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                            null=True, blank=True)
    
    # Para usuarios invitados
    session_id = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_total_price(self):
        # sum() con expresión generadora
        return sum(item.get_cost() for item in self.items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', 
                            on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_cost(self):
        return self.product.price * self.quantity
```

#### Order Model con Choices
```python
class Order(models.Model):
    # Choices: Opciones limitadas
    STATUS_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendiente'
    )
    # En el admin aparecerá un dropdown
```

#### Profile con Signals (users/models.py)
```python
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    # ...

# Signal: Ejecutar código automáticamente
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Solo cuando se crea el usuario
        Profile.objects.create(user=instance)

# Flujo:
# 1. Se crea un User
# 2. Django guarda el User
# 3. Signal post_save se dispara
# 4. Se ejecuta create_user_profile
# 5. Se crea el Profile automáticamente
```

---

### 2. VIEWS.PY - Lógica de Negocio

#### Function-Based View (products/views.py)
```python
def product_list(request, category_slug=None):
    """
    Lista de productos, opcionalmente filtrados por categoría.
    
    Args:
        request: HttpRequest (contiene GET, POST, user, etc.)
        category_slug: Parámetro de la URL (opcional)
    
    Returns:
        HttpResponse con HTML renderizado
    """
    category = None
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_available=True)
    
    # Filtrar por categoría si hay slug
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Paginación
    paginator = Paginator(products, 12)  # 12 por página
    page_number = request.GET.get('page')  # ?page=2
    products_page = paginator.get_page(page_number)
    
    # Context: Datos para el template
    context = {
        'category': category,
        'categories': categories,
        'products': products_page,
    }
    
    # Renderizar template con datos
    return render(request, 'products/product_list.html', context)
```

**Objeto request:**
```python
request.method          # 'GET', 'POST', 'PUT', 'DELETE'
request.GET             # Parámetros URL (?search=teclado)
request.POST            # Datos de formulario
request.FILES           # Archivos subidos
request.user            # Usuario actual
request.session         # Sesión del usuario
request.headers         # Headers HTTP
```

#### Búsqueda con Q Objects
```python
from django.db import models

def search_products(request):
    query = request.GET.get('q', '')
    
    if query:
        products = Product.objects.filter(is_available=True).filter(
            # Q permite OR lógico
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(category__name__icontains=query)
        ).distinct()  # Eliminar duplicados
    
    # ...
```

**Q Objects:**
```python
Q(name='Teclado')                          # Igual a
Q(price__gte=100) & Q(price__lte=500)     # AND (entre 100 y 500)
Q(stock=0) | Q(is_available=False)        # OR
~Q(category__name='Ofertas')              # NOT
```

#### AJAX en Views (cart/views.py)
```python
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_or_create_cart(request)
    
    # Detectar si es petición AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        quantity = int(request.GET.get('quantity', 1))
        
        # ...lógica...
        
        # Retornar JSON
        return JsonResponse({
            'success': True,
            'message': f'{product.name} añadido',
            'cart_items_count': cart.get_total_items(),
        })
    else:
        # Petición normal (formulario HTML)
        # ...lógica...
        return redirect('cart:cart_detail')
```

#### Decoradores
```python
from django.contrib.auth.decorators import login_required

@login_required  # Solo usuarios autenticados
def checkout(request):
    # Si no está autenticado, redirige a LOGIN_URL
    pass

@csrf_exempt  # Desactiva protección CSRF (¡cuidado!)
def api_endpoint(request):
    pass
```

---

### 3. URLS.PY - Enrutamiento

#### URLs principales (TecLegacy/urls.py)
```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),      # /
    path('users/', include('users.urls')),   # /users/...
    path('cart/', include('cart.urls')),     # /cart/...
    path('chatbot/', include('chatbot.urls')),
]

# include(): Incluye URLs de otra app (modularidad)
```

#### URLs de app (products/urls.py - ejemplo)
```python
from django.urls import path
from . import views

app_name = 'products'  # Namespace

urlpatterns = [
    path('', views.index, name='index'),
    # URL: /
    # Vista: products.views.index
    # Nombre: products:index
    
    path('search/', views.search_products, name='search'),
    # URL: /search/
    
    path('<slug:category_slug>/', views.product_list, name='category'),
    # URL: /laptops/
    # Captura 'laptops' en category_slug
    
    path('<slug:category_slug>/<slug:product_slug>/', 
         views.product_detail, name='product_detail'),
    # URL: /laptops/macbook-pro/
]
```

**Tipos de captura:**
```python
<int:id>          # Solo enteros
<slug:slug>       # Letras, números, guiones
<str:name>        # Cualquier string
<uuid:uuid>       # UUID
<path:path>       # Ruta completa (con /)
```

**Generar URLs:**
```python
# En views.py
from django.urls import reverse
url = reverse('products:product_detail', 
             args=['laptops', 'macbook-pro'])
# Resultado: /laptops/macbook-pro/

# En templates
{% url 'products:product_detail' category.slug product.slug %}
```

---

### 4. TEMPLATES - Interfaz HTML

#### Herencia de Templates
**base.html:**
```django
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}TecLegacy{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    {% include 'navbar.html' %}
    
    <main>
        {% block content %}
        <!-- Contenido por defecto -->
        {% endblock %}
    </main>
    
    {% include 'footer.html' %}
</body>
</html>
```

**product_list.html:**
```django
{% extends 'base.html' %}

{% block title %}Productos - TecLegacy{% endblock %}

{% block content %}
    <h1>Productos</h1>
    
    {% for product in products %}
        <div class="product-card">
            <img src="{{ product.image.url }}" alt="{{ product.name }}">
            <h3>{{ product.name }}</h3>
            <p>${{ product.price }}</p>
            
            <a href="{% url 'products:product_detail' product.category.slug product.slug %}">
                Ver detalles
            </a>
        </div>
    {% empty %}
        <p>No hay productos.</p>
    {% endfor %}
    
    <!-- Paginación -->
    {% if products.has_other_pages %}
        {% if products.has_previous %}
            <a href="?page={{ products.previous_page_number }}">Anterior</a>
        {% endif %}
        
        Página {{ products.number }} de {{ products.paginator.num_pages }}
        
        {% if products.has_next %}
            <a href="?page={{ products.next_page_number }}">Siguiente</a>
        {% endif %}
    {% endif %}
{% endblock %}
```

**Template Tags:**
```django
{# Comentario #}

{{ variable }}                    # Imprimir
{{ product.name }}                # Atributo
{{ product.get_total_price }}     # Método

{% if condicion %}...{% endif %}
{% for item in lista %}...{% endfor %}
{% url 'name' arg1 arg2 %}
{% static 'path' %}
{% csrf_token %}                  # Token CSRF en forms

# Filtros
{{ text|lower }}                  # Minúsculas
{{ price|floatformat:2 }}         # 2 decimales
{{ date|date:"d/m/Y" }}           # Formatear fecha
{{ html|safe }}                   # Renderizar HTML
{{ text|truncatewords:30 }}       # Truncar
```

---

### 5. SETTINGS.PY - Configuración

#### Variables de entorno
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Carga archivo.env

SECRET_KEY = os.getenv("SECRET_KEY", "default-key")
DEBUG = os.getenv("DEVELOPMENT", "False") == "True"
```

**archivo.env:**
```env
SECRET_KEY=clave-secreta-larga
DEVELOPMENT=True
DB_NAME=teclegacy_db
DB_USER=root
DB_PASSWORD=mipassword
```

#### Apps instaladas
```python
INSTALLED_APPS = [
    # Django por defecto
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Terceros
    'django_extensions',
    
    # Propias
    'users',
    'products',
    'cart',
    'chatbot',
]
```

#### Base de datos
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("DB_NAME", "teclegacy_db"),
        'USER': os.getenv("DB_USER", "root"),
        'PASSWORD': os.getenv("DB_PASSWORD", ""),
        'HOST': os.getenv("DB_HOST", "127.0.0.1"),
        'PORT': os.getenv("DB_PORT", "3306"),
    }
}
```

#### Archivos estáticos y media
```python
# STATIC: CSS, JS, imágenes del diseño
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Producción

# MEDIA: Archivos subidos por usuarios
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

**Diferencia:**
```
STATIC:
- Parte del código (CSS, JS, logos)
- No cambian frecuentemente
- Se recopilan: python manage.py collectstatic

MEDIA:
- Subidos por usuarios (fotos productos, avatares)
- Cambian constantemente
- Se guardan directamente
```

#### Context Processors
```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart_processor',  # ← Custom
            ],
        },
    },
]
```

**cart/context_processors.py:**
```python
def cart_processor(request):
    """Hace el carrito disponible en TODOS los templates."""
    cart = _get_or_create_cart(request)
    return {
        'cart': cart,
        'cart_items_count': cart.get_total_items(),
    }
```

Ahora en cualquier template:
```django
<span>Carrito ({{ cart_items_count }})</span>
```

---

## 🚧 ¿QUÉ LE FALTA AL PROYECTO?

### 1. **Sistema de Reseñas/Valoraciones**
Permitir a usuarios calificar productos con estrellas y comentarios.

### 2. **Wishlist (Lista de Deseos)**
Guardar productos favoritos para comprar después.

### 3. **Comparador de Productos**
Comparar características de varios productos lado a lado.

### 4. **Cupones de Descuento**
Sistema de códigos promocionales.

### 5. **Notificaciones por Email**
- Confirmación de pedido
- Cambio de estado del pedido
- Recuperación de contraseña

### 6. **Historial de Pedidos**
Vista de usuario con todos sus pedidos anteriores.

### 7. **Filtros Avanzados**
- Por rango de precio
- Por marca
- Por características
- Ordenamiento múltiple

### 8. **Búsqueda Mejorada**
- Autocompletado
- Búsqueda por voz
- Corrección de typos

### 9. **Sistema de Pagos Real**
Integración con:
- PayPal
- Stripe
- Mercado Pago
- Nequi/Daviplata

### 10. **Dashboard de Usuario**
- Estadísticas de compras
- Productos vistos recientemente
- Recomendaciones personalizadas

### 11. **Chatbot Mejorado**
- Integración con IA (OpenAI, Gemini)
- Respuestas más naturales
- Historial de conversaciones

### 12. **Panel de Vendedor/Admin Mejorado**
- Estadísticas de ventas
- Gráficos
- Reportes exportables (PDF, Excel)

### 13. **Sistema de Stock Automático**
- Reducir stock al confirmar pedido
- Alertas de stock bajo
- Productos agotados automáticamente

### 14. **Multi-idioma (i18n)**
Soporte para español e inglés.

### 15. **PWA (Progressive Web App)**
Funcionar como app móvil.

### 16. **Tests Automatizados**
Pruebas unitarias y de integración.

### 17. **Seguridad Mejorada**
- Rate limiting
- Verificación de email
- 2FA (autenticación de dos factores)

### 18. **SEO Optimización**
- Meta tags dinámicos
- Sitemap
- Robots.txt
- Open Graph tags

### 19. **Sistema de Ofertas/Flash Sales**
Descuentos por tiempo limitado.

### 20. **Programa de Fidelidad**
Puntos por compras.

---

## 🎯 MEJORAS PARA TU PORTAFOLIO

### PRIORIDAD ALTA (Hacer primero)

#### 1. **Corregir Problemas de Seguridad**

**settings.py línea 13:**
```python
# ❌ ACTUAL:
DEBUG = "True"  # Siempre es True (string)

# ✅ CORRECTO:
DEBUG = os.getenv("DEVELOPMENT", "False") == "True"
```

**settings.py línea 15:**
```python
# ❌ ACTUAL:
ALLOWED_HOSTS = ['*']  # Inseguro

# ✅ CORRECTO:
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
```

#### 2. **Validación de Stock**

**cart/views.py - add_to_cart:**
```python
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # ✅ AGREGAR: Verificar stock
    if quantity > product.stock:
        messages.error(request, f'Solo hay {product.stock} unidades disponibles')
        return redirect('products:product_detail', product.category.slug, product.slug)
    
    # ...resto del código...
```

#### 3. **Reducir Stock al Confirmar Pedido**

```python
def create_order(request):
    # Después de crear la orden
    for item in order.items.all():
        product = item.product
        product.stock -= item.quantity
        if product.stock <= 0:
            product.is_available = False
        product.save()
```

#### 4. **README.md Completo**
- Descripción del proyecto
- Screenshots
- Tecnologías usadas
- Instrucciones de instalación
- Features principales

#### 5. **.gitignore Completo**
```gitignore
*.pyc
__pycache__/
db.sqlite3
*.env
archivo.env
env_django/
media/
staticfiles/
.vscode/
.idea/
```

#### 6. **Sistema de Reseñas Básico**

**products/models.py:**
```python
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i,i) for i in range(1,6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['product', 'user']
```

**Agregar al Product:**
```python
def get_average_rating(self):
    from django.db.models import Avg
    result = self.reviews.aggregate(Avg('rating'))
    return result['rating__avg'] or 0
```

#### 7. **Perfil de Usuario Completo**

**users/views.py:**
```python
@login_required
def profile_view(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.save()
        messages.success(request, 'Perfil actualizado')
        return redirect('users:profile')
    
    return render(request, 'users/profile.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'users/order_history.html', {'orders': orders})
```

---

### PRIORIDAD MEDIA

#### 8. **Filtros de Búsqueda**
```python
def search_products(request):
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category = request.GET.get('category')
    
    products = Product.objects.filter(is_available=True)
    
    if query:
        products = products.filter(name__icontains=query)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if category:
        products = products.filter(category_id=category)
    
    # ...
```

#### 9. **Paginación Mejorada**
Con números de página y navegación completa.

#### 10. **Emails de Notificación**

**settings.py:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

**Enviar email:**
```python
from django.core.mail import send_mail

send_mail(
    subject='Confirmación de Pedido',
    message=f'Tu pedido #{order.id} ha sido confirmado',
    from_email='noreply@teclegacy.com',
    recipient_list=[order.email],
)
```

---

### PRIORIDAD BAJA (Opcional)

#### 11. **API REST**
Con Django REST Framework para apps móviles.

#### 12. **Tests Automatizados**
```python
from django.test import TestCase

class ProductModelTest(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(
            name='Test',
            price=100
        )
        self.assertEqual(product.name, 'Test')
```

#### 13. **Caché**
Para mejorar performance.

#### 14. **Dockerización**
Para fácil despliegue.

---

## 📚 RECURSOS DE APRENDIZAJE

### Documentación Oficial
- Django: https://docs.djangoproject.com/
- Python: https://docs.python.org/3/

### Tutoriales Recomendados
- Django Girls Tutorial
- Real Python (realrython.com)
- Corey Schafer en YouTube
- Traversy Media

### Deploy Gratuito
- Railway.app
- Render.com
- PythonAnywhere
- Heroku (con limitaciones)

---

## 🎓 EJERCICIOS PRÁCTICOS

### Nivel Básico
1. Agrega un campo `discount_percentage` al modelo Product
2. Crea una vista que muestre solo productos en oferta
3. Agrega un filtro por precio en la búsqueda

### Nivel Intermedio
1. Implementa el sistema de reseñas completo
2. Crea historial de pedidos del usuario
3. Agrega validación de stock en el carrito

### Nivel Avanzado
1. Implementa búsqueda full-text
2. Crea sistema de recomendaciones
3. Agrega autenticación con Google/Facebook

---

## 📖 GLOSARIO

- **ORM**: Object-Relational Mapping - Convierte Python a SQL
- **Migration**: Archivo que describe cambios en BD
- **QuerySet**: Conjunto de resultados de BD
- **Slug**: URL amigable (teclado-gaming vs id=123)
- **Context**: Datos que se pasan al template
- **Middleware**: Capa de procesamiento de requests
- **Signal**: Evento automático en Django
- **CSRF**: Protección contra ataques web
- **WSGI**: Servidor web para Python

---

¡Éxito con tu proyecto! 🚀
