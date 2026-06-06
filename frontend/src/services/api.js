const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || `${window.location.protocol}//${window.location.hostname}:18050`;

export async function fetchHealth() {
  const response = await fetch(`${API_BASE_URL}/api/health`);
  if (!response.ok) {
    throw new Error('Error al conectar con el servidor backend');
  }
  return response.json();
}

export async function fetchCriticalInventory() {
  const response = await fetch(`${API_BASE_URL}/api/inventory/critical`);
  if (!response.ok) {
    throw new Error('Error al recuperar inventario crítico');
  }
  return response.json();
}

export async function sendChatMessage(message) {
  const response = await fetch(`${API_BASE_URL}/api/agent/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message }),
  });
  
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || 'Error en el agente conversacional');
  }
  return response.json();
}
