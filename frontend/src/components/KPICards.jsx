import React from 'react';

export default function KPICards({ criticalCount, isOffline, activeWarehouses }) {
  return (
    <div className="kpi-container">
      <div className="kpi-card critical">
        <div className="kpi-info">
          <h3>Alertas de Stock</h3>
          <p>{criticalCount}</p>
        </div>
        <div className="kpi-icon">🚨</div>
      </div>

      <div className={`kpi-card ${isOffline ? 'warning' : 'success'}`}>
        <div className="kpi-info">
          <h3>Modo de Operación</h3>
          <p>{isOffline ? 'Offline (Local)' : 'Online (LLM)'}</p>
        </div>
        <div className="kpi-icon">⚙️</div>
      </div>

      <div className="kpi-card info">
        <div className="kpi-info">
          <h3>Bodegas Activas</h3>
          <p>{activeWarehouses || 0}</p>
        </div>
        <div className="kpi-icon">📍</div>
      </div>
    </div>
  );
}
