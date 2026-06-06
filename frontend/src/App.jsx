import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import KPICards from './components/KPICards';
import AgentChat from './components/AgentChat';
import { fetchHealth, fetchCriticalInventory } from './services/api';

function App() {
  const [health, setHealth] = useState(null);
  const [criticalInventory, setCriticalInventory] = useState([]);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isOfflineMode, setIsOfflineMode] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    try {
      setLoading(true);
      const [healthData, inventoryData] = await Promise.all([
        fetchHealth().catch(() => ({ status: 'error', database: 'disconnected', chromadb: 'disconnected' })),
        fetchCriticalInventory().catch(() => [])
      ]);
      
      setHealth(healthData);
      setCriticalInventory(inventoryData);
      
      if (healthData.status === 'error') {
        setIsOfflineMode(true);
      } else {
        setIsOfflineMode(false);
      }
      
      setError(null);
    } catch (err) {
      setError(err.message);
      setIsOfflineMode(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    // Auto-refresh every 30 seconds
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app-container">
      <Sidebar 
        health={health} 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
      />

      <main className="main-content">
        <header className="header">
          <div className="header-title">
            <h1>Copiloto de Logística OmniRetail</h1>
            <p>Monitoreo inteligente de stock en tiempo real y asistente logístico</p>
          </div>
          <button onClick={loadData} className="send-button" style={{ padding: '0.65rem 1.25rem' }}>
            🔄 Actualizar Datos
          </button>
        </header>

        <KPICards 
          criticalCount={criticalInventory.length} 
          isOffline={isOfflineMode} 
        />

        {activeTab === 'dashboard' ? (
          <div className="content-grid">
            <div className="dashboard-panel">
              <div className="panel-title">
                <span>Alertas Críticas de Stock (Stock ≤ 10)</span>
                <span className="badge red">Stock Crítico</span>
              </div>
              
              {loading && criticalInventory.length === 0 ? (
                <div className="loading-wrapper">
                  <div className="spinner"></div>
                  <p>Recuperando inventario...</p>
                </div>
              ) : criticalInventory.length > 0 ? (
                <div className="table-wrapper">
                  <table className="modern-table">
                    <thead>
                      <tr>
                        <th>Producto</th>
                        <th>SKU</th>
                        <th>Stock Actual</th>
                        <th>En Tránsito</th>
                        <th>Ubicación</th>
                      </tr>
                    </thead>
                    <tbody>
                      {criticalInventory.map((item, index) => (
                        <tr key={index}>
                          <td style={{ fontWeight: 600 }}>{item.product}</td>
                          <td><code>{item.sku}</code></td>
                          <td>
                            <span className="badge red" style={{ fontSize: '0.8rem' }}>
                              {item.stock} uds
                            </span>
                          </td>
                          <td>{item.transit} uds</td>
                          <td>📍 {item.location}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="loading-wrapper">
                  <span style={{ fontSize: '2.5rem' }}>✅</span>
                  <p style={{ color: 'var(--secondary-color)', fontWeight: 600 }}>
                    ¡Todo al día! No hay productos con stock crítico.
                  </p>
                </div>
              )}
            </div>

            <div className="dashboard-panel">
              <div className="panel-title">
                <span>Asistente conversacional</span>
                <span className="badge green">IA Activa</span>
              </div>
              <AgentChat setIsOfflineMode={setIsOfflineMode} />
            </div>
          </div>
        ) : (
          <div className="dashboard-panel" style={{ flexGrow: 1 }}>
            <div className="panel-title">
              <span>Chat de Consulta de Inventario</span>
              <span className="badge green">Copiloto</span>
            </div>
            <AgentChat setIsOfflineMode={setIsOfflineMode} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
