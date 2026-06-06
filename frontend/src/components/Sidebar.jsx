import React from 'react';

export default function Sidebar({ health, activeTab, setActiveTab }) {
  const isBackendOk = health && health.status === 'ok';
  const isDbOk = health && health.database === 'connected';
  const isChromaOk = health && health.chromadb === 'connected';

  return (
    <aside className="sidebar">
      <div>
        <div className="logo-container">
          <div className="logo-icon">O</div>
          <span className="logo-text">OmniRetail</span>
        </div>

        <ul className="menu-items">
          <li 
            className={`menu-item ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            📊 Dashboard
          </li>
          <li 
            className={`menu-item ${activeTab === 'copiloto' ? 'active' : ''}`}
            onClick={() => setActiveTab('copiloto')}
          >
            💬 Copiloto Inventario
          </li>
        </ul>
      </div>

      <div className="status-panel">
        <h4 className="status-title">Estado del Sistema</h4>
        <div className="status-item">
          <span className="status-label">Servidor API</span>
          <span className="status-value">
            <span className={`status-dot ${isBackendOk ? 'green' : 'red'}`}></span>
            {isBackendOk ? 'Online' : 'Offline'}
          </span>
        </div>
        <div className="status-item">
          <span className="status-label">Base de Datos</span>
          <span className="status-value">
            <span className={`status-dot ${isDbOk ? 'green' : 'red'}`}></span>
            {isDbOk ? 'Conectado' : 'Desconectado'}
          </span>
        </div>
        <div className="status-item">
          <span className="status-label">ChromaDB (RAG)</span>
          <span className="status-value">
            <span className={`status-dot ${isChromaOk ? 'green' : 'red'}`}></span>
            {isChromaOk ? 'Conectado' : 'Desconectado'}
          </span>
        </div>
      </div>
    </aside>
  );
}
