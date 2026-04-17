# TecLegacy Marketplace

TecLegacy es una plataforma de comercio electrónico (E-commerce) enfocada en el nicho del gaming y la tecnología. Desarrollada con arquitectura MVC/MVT, esta aplicación ofrece una experiencia de compra completa, desde la exploración de productos hasta el procesamiento de pagos, complementada con un asistente virtual inteligente.

## 🚀 Arquitectura y Tecnologías

El proyecto fue construido utilizando herramientas robustas y escalables, orientadas a estándares de la industria:

- **Backend / Framework:** Django 6 (Python)
- **Base de Datos (Producción):** PostgreSQL alojada en **Neon**
- **Almacenamiento de Archivos (Imágenes):** **Cloudinary** (MediaCloudinaryStorage)
- **Despliegue (Hosting):** **Render**
- **Frontend:** HTML5, Vanilla CSS, Vanilla JS y Bootstrap 5
- **Integraciones:** 
  - **Stripe:** Para el procesamiento seguro de pagos.
  - **Google Gemini:** Para el motor de inteligencia artificial del Chatbot asistente.
  - **Resend:** Para el envío de correos transaccionales.

## ✨ Características Principales

* **Autenticación Segura:** Sistema de login tradicional y acceso mediante OAuth (Google) vía `django-allauth`.
* **Gestor de Carrito de Compras:** Lógica transaccional para agregar, modificar y eliminar productos.
* **Asistente Inteligente (Chatbot):** Un widget integrado impulsado por IA para ayudar a los clientes a encontrar productos de manera interactiva.
* **Panel de Administración:** Gestión completa de inventario y categorías (CRUD).
* **Diseño Responsivo:** Interfaz adaptativa optimizada tanto para escritorio como para dispositivos móviles.

## ⚙️ Ejecución Local

Para correr este proyecto en tu entorno de desarrollo:

1. Clona el repositorio: `git clone https://github.com/JohanM17/Marketplace---TecLegacy.git`
2. Crea un entorno virtual e instala las dependencias: `pip install -r requirements.txt`
3. Configura tus variables de entorno en un archivo `.env`configurando tus llaves de Stripe, Gemini, etc.
4. Aplica las migraciones locales: `python manage.py migrate`
5. Levanta el servidor: `python manage.py runserver`

## 🤖 Nota sobre el Desarrollo (AI-Assisted)

Este proyecto fue desarrollado bajo un paradigma moderno de ingeniería de software, donde **gran parte de la escritura de código, depuración arquitectónica y orquestación del despliegue en la nube fue asistida activamente por Inteligencia Artificial**. Esto demuestra la capacidad de integrar herramientas de IA de vanguardia en el flujo de trabajo diario para acelerar el desarrollo, resolver bloqueos de infraestructura y mantener buenas prácticas de código limpio y control de versiones.
