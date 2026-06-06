#!/bin/bash

# =====================================================================
# Script de Inicio Automático para ALI (Backend + Frontend + Jupyter)
# OmniRetail S.A. - Soluciones IA
# =====================================================================

# Colores para mensajes de consola
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # Sin color

echo -e "${BLUE}=== Iniciando Entorno de ALI (Agente de Logística Inteligente) ===${NC}\n"

# Puertos fijos del proyecto (local + acceso por Tailscale/LAN)
BACKEND_PORT=18050
FRONTEND_PORT=19051
APP_HOST="0.0.0.0"
TAILSCALE_IP=$(tailscale ip -4 2>/dev/null | head -n 1 || true)

# 1. Validar entorno virtual
if [ ! -d ".venv" ]; then
    echo -e "${RED}[ERROR] No se encontró el entorno virtual (.venv).${NC}"
    echo -e "Por favor, ejecutá: ${YELLOW}python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt${NC}"
    exit 1
fi

# 2. Activar entorno virtual
echo -e "${GREEN}[INFO] Activando entorno virtual (.venv)...${NC}"
source .venv/bin/activate

# 3. Registrar kernel de Jupyter por si acaso
echo -e "${GREEN}[INFO] Registrando kernel de Jupyter para notebooks...${NC}"
python -m ipykernel install --user --name=solucionesia_venv --display-name "Python (SolucionesIA Venv)" &> /dev/null

# Variables para guardar PIDs de los procesos
BACKEND_PID=""
FRONTEND_PID=""

# Función para limpiar y matar procesos en segundo plano al salir
cleanup() {
    echo -e "\n\n${YELLOW}[INFO] Deteniendo servicios en segundo plano...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        echo -e "Deteniendo Backend FastAPI (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        echo -e "Deteniendo Frontend React (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null
    fi
    echo -e "${GREEN}=== Servicios detenidos correctamente. ¡Hasta luego! ===${NC}"
    exit 0
}

# Capturar Ctrl+C (SIGINT) y SIGTERM para apagar todo limpio
trap cleanup SIGINT SIGTERM

# 4. Iniciar Backend (FastAPI)
echo -e "${GREEN}[INFO] Iniciando servidor Backend FastAPI en puerto ${BACKEND_PORT}...${NC}"
.venv/bin/python -m uvicorn main:app --app-dir backend --host "${APP_HOST}" --port "${BACKEND_PORT}" --reload &
BACKEND_PID=$!

# Esperar un par de segundos a que levante el backend
sleep 2

# 5. Iniciar Frontend (Vite/React)
echo -e "${GREEN}[INFO] Iniciando servidor Frontend React en puerto ${FRONTEND_PORT}...${NC}"
if [ -d "frontend" ]; then
    cd frontend
    pnpm run dev --host "${APP_HOST}" --port "${FRONTEND_PORT}" &
    FRONTEND_PID=$!
    cd ..
else
    echo -e "${RED}[WARNING] No se encontró la carpeta 'frontend'. Solo se iniciará el Backend.${NC}"
fi

echo -e "\n${BLUE}=== ¡Todos los servicios están arriba! ===${NC}"
echo -e "👉 Backend API local: ${YELLOW}http://127.0.0.1:${BACKEND_PORT}${NC} (Docs en /docs)"
echo -e "👉 Frontend local:    ${YELLOW}http://127.0.0.1:${FRONTEND_PORT}${NC}"
if [ ! -z "$TAILSCALE_IP" ]; then
    echo -e "👉 Backend Tailscale: ${YELLOW}http://${TAILSCALE_IP}:${BACKEND_PORT}${NC} (Docs en /docs)"
    echo -e "👉 Frontend Tailscale:${YELLOW}http://${TAILSCALE_IP}:${FRONTEND_PORT}${NC}"
fi
echo -e "👉 Jupyter Kernel:   ${YELLOW}Python (SolucionesIA Venv)${NC} (Ya registrado para tu notebook)"
echo -e "\n${YELLOW}Presioná CTRL+C para detener todos los servidores a la vez.${NC}\n"

# Mantener el script corriendo y volcar logs en tiempo real
wait
