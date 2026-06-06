# Frontend — Agente de Logística Inteligente (ALI)

Este directorio contiene el frontend de la aplicación **ALI (Agente de Logística Inteligente)**, desarrollado como una interfaz moderna, responsiva y de alto rendimiento utilizando **React + Vite**.

---

## Características Principales

El panel visual está diseñado para ofrecer una experiencia de usuario premium con microinteracciones fluidas y componentes modulares:

*   **Dashboard Consolidado:**
    *   **Tarjetas de KPIs en Tiempo Real:** Muestra de forma inmediata alertas críticas de stock, modo de operación (Online LLM u Offline Fallback) y la cantidad de bodegas activas.
    *   **Grilla de Stock Crítico:** Tabla dinámica que lista todos los productos con stock crítico (menor o igual a 10 unidades), indicando su SKU, stock actual, unidades en tránsito y ubicación.
*   **Chat y Copiloto Persistente:**
    *   **Estado Centralizado:** La conversación y el borrador del input se mantienen intactos al alternar entre la vista reducida del Dashboard y la vista expandida a pantalla completa del Copiloto ALI.
    *   **UX de Escritura Fluida:** El campo de texto mantiene el cursor enfocado permanentemente (incluso tras presionar Enter o enviar un mensaje), permitiendo redactar la siguiente consulta de manera inmediata.
*   **Monitor del Sistema (Sidebar):**
    *   Indicadores visuales del estado de conexión de la API del Backend, la base de datos relacional (SQLite) y la base de datos vectorial (ChromaDB).

---

## Tecnologías Utilizadas

*   **Core:** React 19 + Vite 8
*   **Estilos:** Vanilla CSS moderno (con variables personalizadas, efectos de desenfoque de fondo y transiciones suaves).
*   **Gestor de Paquetes:** `pnpm`
*   **Calidad de Código:** ESLint para mantener estándares limpios y evitar variables no utilizadas.

---

## Inicio Rápido

Asegúrate de contar con [pnpm](https://pnpm.io/) instalado en tu sistema.

### 1. Instalación de Dependencias

Ejecuta el siguiente comando dentro de la carpeta `frontend`:
```bash
pnpm install
```

### 2. Variables de Entorno

Por defecto, el frontend se conectará al backend en `http://localhost:18050`. Si necesitas cambiar la dirección, crea un archivo `.env` en este directorio:
```env
VITE_API_BASE_URL=http://tu-servidor-backend:puerto
```

### 3. Servidor de Desarrollo

Inicia el entorno de desarrollo local con soporte de recarga rápida (HMR):
```bash
pnpm run dev
```
La aplicación estará disponible en `http://localhost:19051` (o en el puerto configurado por el script de arranque global).

### 4. Construcción para Producción

Compila y optimiza el frontend para despliegue:
```bash
pnpm run build
```
Los archivos optimizados se generarán en la carpeta `dist/`.

### 5. Linter y Estilo de Código

Verifica que el código cumpla con las reglas definidas en el proyecto:
```bash
pnpm run lint
```

---

## Estructura del Código

```text
src/
├── assets/          # Recursos estáticos e imágenes.
├── components/      # Componentes de React (Sidebar, KPICards, AgentChat).
├── services/        # Capa de servicio e integración con APIs externas (api.js).
├── App.jsx          # Componente principal que coordina el estado global del chat y las vistas.
├── App.css          # Estilos específicos del layout general de la aplicación.
├── index.css        # Sistema de diseño global (paleta de colores, tipografía, variables CSS).
└── main.jsx         # Punto de entrada de la aplicación.
```
