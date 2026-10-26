# TechStore - Sistema de Logica de Negocios

Proyecto desarrollado para la Actividad 4 de Componentes de Logica de Negocio, enfocada en la administracion de pedidos mediante la arquitectura de Aggregate Roots, Specification Pattern y Maquina de Estados.

**Instalacion**
1. Clona este repositorio en tu equipo local.
2. Abre una terminal y verifica que cuentas con Python 3.11 o superior.
3. Crea un entorno virtual ejecutando: `python -m venv .venv`
4. Activa el entorno virtual:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
5. Instala las dependencias requeridas:
   `pip install fastapi uvicorn pytest httpx`

**Ejecucion**
- Para cargar los datos CSV y procesarlos por consola:
  `python cargar_csv.py`
- Para iniciar la API REST:
  `uvicorn app.api:app --reload`
- Para correr las pruebas automatizadas:
  `python -m pytest -q`

**Reglas de Negocio Implementadas**
- **Validacion de Datos:** Los montos (Money) no pueden ser negativos. Las cantidades de articulos deben ser estrictamente positivas.
- **Limite de Inventario:** Un pedido no puede superar un maximo de 20 unidades en total.
- **Descuentos (Specification Pattern):** 
  - Descuento VIP (10%): Exige que el cliente sea VIP, el total supere $500 MXN, tenga minimo 4 unidades y no existan promociones activas.
  - Descuento por volumen (5%): Aplica si el total supera los $5000 MXN y no hay promociones activas.
- **Transiciones de Estado y Eventos:** El pedido debe seguir un flujo estricto (`DRAFT` -> `CONFIRMED` -> `SHIPPED` -> `DELIVERED`/`RETURNED` o `CANCELLED`). Toda transicion valida registra un Evento de Dominio con su fecha en UTC.

**Endpoints Disponibles**
- `GET /orders/{id}`: Consulta el estado, unidades y total de un pedido.
- `POST /orders/{id}/confirm`: Cambia el pedido a estado CONFIRMED. Retorna 404 si no existe, 409 si la transicion es invalida y 422 si hay problemas con los datos.
- `POST /orders/{id}/ship`: Avanza el pedido a SHIPPED requiriendo un numero de guia.
- `POST /orders/{id}/cancel`: Cancela el pedido exigiendo un motivo escrito (Solo valido desde estado CONFIRMED).