import React from 'react';
import { Link } from 'react-router-dom';
import { FiAlertTriangle } from 'react-icons/fi';

function NotFoundPage() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '50vh',
      textAlign: 'center',
      padding: '2rem'
    }}>
      <FiAlertTriangle size={80} className="fg-primary" style={{ marginBottom: '1rem' }} />
      <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
        404 - Página não encontrada
      </h1>
      <p style={{ marginBottom: '1.5rem', color: '#666' }}>
        O link que você acessou não existe ou foi removido.
      </p>
      <Link to="/" 
        className="btn card"
        style={{
        padding: '0.5rem 1rem',
        color: '#fff',
        borderRadius: '4px',
        textDecoration: 'none'
      }}>
        Voltar para a página inicial
      </Link>
    </div>
  );
}

export default NotFoundPage;

