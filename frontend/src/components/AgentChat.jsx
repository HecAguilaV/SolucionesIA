import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../services/api';

export default function AgentChat({ setIsOfflineMode }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hola, soy tu Agente de Gestión de Inventario OmniRetail. ¿En qué te puedo ayudar hoy?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const data = await sendChatMessage(userMessage);
      
      // Si la respuesta indica offline fallback
      if (data.response.includes('[OFFLINE FALLBACK]')) {
        setIsOfflineMode(true);
      } else {
        setIsOfflineMode(false);
      }

      setMessages((prev) => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev, 
        { role: 'assistant', content: `⚠️ Error de comunicación: ${error.message}. Se activará el soporte offline si el servidor está caído.` }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-history">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-bubble ${msg.role}`}>
            {msg.content.split('\n').map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>
        ))}
        {isLoading && (
          <div className="typing-indicator">
            <span className="typing-dot"></span>
            <span className="typing-dot"></span>
            <span className="typing-dot"></span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Pregúntale al agente sobre quiebres de stock o clima..."
          className="chat-input"
          disabled={isLoading}
        />
        <button type="submit" className="send-button" disabled={isLoading || !input.trim()}>
          Enviar
        </button>
      </form>
    </div>
  );
}
