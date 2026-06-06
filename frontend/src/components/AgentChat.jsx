import { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../services/api';

export default function AgentChat({ setIsOfflineMode, messages, setMessages, input, setInput }) {
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);
    
    // Mantener el cursor enfocado
    setTimeout(() => {
      inputRef.current?.focus();
    }, 0);

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
      setTimeout(() => {
        inputRef.current?.focus();
      }, 0);
    }
  };

  const renderMessageContent = (content) => {
    const trimmed = content.trim();
    // Detectar si es un bloque JSON y formatearlo
    if ((trimmed.startsWith('{') && trimmed.endsWith('}')) || (trimmed.startsWith('[') && trimmed.endsWith(']'))) {
      try {
        const parsed = JSON.parse(trimmed);
        return (
          <pre className="json-block">
            <code>{JSON.stringify(parsed, null, 2)}</code>
          </pre>
        );
      } catch {
        // Ignorar e ir al renderizado por línea
      }
    }

    const lines = content.split('\n');
    let inList = false;
    const elements = [];
    let listItems = [];

    const parseInlineStyles = (text) => {
      const parts = [];
      let currentIndex = 0;
      const regex = /(\*\*|`)(.*?)\1/g;
      let match;

      while ((match = regex.exec(text)) !== null) {
        const matchIndex = match.index;
        if (matchIndex > currentIndex) {
          parts.push(text.substring(currentIndex, matchIndex));
        }
        
        const type = match[1];
        const innerContent = match[2];
        if (type === '**') {
          parts.push(<strong key={matchIndex}>{innerContent}</strong>);
        } else if (type === '`') {
          parts.push(<code key={matchIndex} className="inline-code">{innerContent}</code>);
        }
        
        currentIndex = regex.lastIndex;
      }
      
      if (currentIndex < text.length) {
        parts.push(text.substring(currentIndex));
      }
      
      return parts.length > 0 ? parts : text;
    };

    lines.forEach((line, index) => {
      const trimmedLine = line.trim();

      if (trimmedLine.startsWith('### ')) {
        if (inList) {
          elements.push(<ul key={`list-${index}`} className="chat-list">{listItems}</ul>);
          inList = false;
          listItems = [];
        }
        elements.push(<h4 key={index} className="chat-title-h4">{parseInlineStyles(trimmedLine.substring(4))}</h4>);
      } else if (trimmedLine.startsWith('## ')) {
        if (inList) {
          elements.push(<ul key={`list-${index}`} className="chat-list">{listItems}</ul>);
          inList = false;
          listItems = [];
        }
        elements.push(<h3 key={index} className="chat-title-h3">{parseInlineStyles(trimmedLine.substring(3))}</h3>);
      } else if (trimmedLine.startsWith('# ')) {
        if (inList) {
          elements.push(<ul key={`list-${index}`} className="chat-list">{listItems}</ul>);
          inList = false;
          listItems = [];
        }
        elements.push(<h2 key={index} className="chat-title-h2">{parseInlineStyles(trimmedLine.substring(2))}</h2>);
      } else if (trimmedLine.startsWith('- ') || trimmedLine.startsWith('* ')) {
        inList = true;
        listItems.push(<li key={index}>{parseInlineStyles(trimmedLine.substring(2))}</li>);
      } else if (trimmedLine === '') {
        if (inList) {
          elements.push(<ul key={`list-${index}`} className="chat-list">{listItems}</ul>);
          inList = false;
          listItems = [];
        }
        elements.push(<div key={index} className="chat-spacer"></div>);
      } else {
        if (inList) {
          elements.push(<ul key={`list-${index}`} className="chat-list">{listItems}</ul>);
          inList = false;
          listItems = [];
        }
        elements.push(<p key={index} className="chat-paragraph">{parseInlineStyles(line)}</p>);
      }
    });

    if (inList) {
      elements.push(<ul key="list-end" className="chat-list">{listItems}</ul>);
    }

    return elements;
  };

  return (
    <div className="chat-container">
      <div className="chat-history">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-bubble ${msg.role}`}>
            {renderMessageContent(msg.content)}
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
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Pregúntale al agente sobre quiebres de stock o clima..."
          className="chat-input"
        />
        <button type="submit" className="send-button" disabled={isLoading || !input.trim()}>
          Enviar
        </button>
      </form>
    </div>
  );
}
