# Teiva Backend - CRM Inteligente para Agentes de Seguros

Estructura de backend desarrollada utilizando **FastAPI** y aplicando principios de **Clean Architecture / Hexagonal Architecture**.

## Arquitectura de Capas

La estructura del código está organizada de la siguiente manera:

- **`app/domain/` (Capa 1: Dominio):**
  Lógica de negocio pura y aislada. No tiene dependencias de bases de datos ni frameworks externos.
  - `models/`: Entidades de negocio (`tenant`, `user`, `client`).
  - `exceptions/`: Excepciones de negocio personalizadas.

- **`app/application/` (Capa 2: Aplicación):**
  Casos de uso y orquestación de la lógica de negocio.
  - `ports/inputs/`: Interfaces de los casos de uso que expone la aplicación.
  - `ports/outputs/`: Interfaces de SPI (Service Provider Interface) que la infraestructura debe implementar (ej. repositorios, cachés).
  - `use_cases/`: Implementaciones de los flujos de trabajo del sistema (auth, client).

- **`app/infrastructure/` (Capa 3: Infraestructura):**
  Adaptadores externos e implementaciones de los puertos de salida.
  - `adapters/database/`: Adaptador para Supabase / PostgreSQL utilizando Row Level Security (RLS).
  - `adapters/cache/`: Adaptador de Redis para colas y límites de peticiones (Rate Limiting).
  - `adapters/ai/`: Adaptadores para APIs de modelos de lenguaje (Groq, OpenAI).
  - `config/`: Configuración global y variables de entorno (`settings.py`).

- **`app/api/` (Capa de Entrada):**
  Controladores y adaptadores HTTP externos que exponen la funcionalidad.
  - `v1/endpoints/`: Routers de FastAPI (`auth.py`, `clients.py`).
  - `v1/api_router.py`: Enrutador unificado v1.
  - `middlewares/`: Middleware para extraer el `tenant_id` a partir del token JWT para soporte multi-inquilino (multi-tenant).

## Desarrollo Local

### Requisitos Previos
- Python 3.11+
- Redis (opcional para desarrollo local si se deshabilita la caché)

### Instrucciones
1. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar el servidor de desarrollo:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

## Pruebas
Ejecutar las pruebas unitarias y de integración utilizando `pytest`:
```bash
pytest
```
