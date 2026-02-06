import React, { useState, useEffect, useRef } from 'react';
import { CHARACTERS, ERROR_MESSAGES } from '../constants/config';
import { logHints, ENCRYPTED_FLAG } from '../utils/crypto';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const [error, setError] = useState('');
  const [isDecrypting, setIsDecrypting] = useState(false);
  const errorRef = useRef<HTMLDivElement>(null);
  const mainContentRef = useRef<HTMLElement>(null);

  // Focus management for error messages
  useEffect(() => {
    if (error && errorRef.current) {
      errorRef.current.focus();
    }
  }, [error]);

  // Initial setup
  useEffect(() => {
    // Konsol ipuçlarını başlat
    logHints();
    
    // Jake'in "profesyonel" debug mesajı
    console.log("🔧 Jake: Sistem başlatıldı!");
    console.log("🔐 Şifrelenmiş veri:", ENCRYPTED_FLAG);

    // Focus main content for screen readers
    if (mainContentRef.current) {
      mainContentRef.current.focus();
    }
  }, []);

  // Bu fonksiyon KASITLI olarak bozuk - kullanıcı konsol üzerinden çözecek
  const handleDecrypt = () => {
    setIsDecrypting(true);
    setError('');
    
    // Fake loading animation
    setTimeout(() => {
      setError(ERROR_MESSAGES.DECRYPT_ERROR);
      setIsDecrypting(false);
      console.log("❌ Server bağlantısı kopuk! Manual decrypt gerekiyor...");
    }, 2000);
  };

  // Keyboard navigation for the decrypt button
  const handleDecryptKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      if (!error && !isDecrypting) {
        handleDecrypt();
      }
    }
  };

  return (
    <div className="dashboard-container">
      {/* Skip link for keyboard navigation */}
      <a href="#main-content" className="skip-link sr-only">
        Skip to main content
      </a>

      <header className="vault-header">
        <h1>🏛️ HAMAM KASA</h1>
        <h2>Captain Holt's Digital Vault</h2>
        <div 
          className="status-indicator" 
          role="status" 
          aria-live="polite"
          aria-label={`System status: ${error ? 'Connection Lost' : 'Active'}`}
        >
          <span 
            className={`status-dot ${error ? 'error' : 'active'}`}
            aria-hidden="true"
          ></span>
          <span id="status-text">
            Status: {error ? 'Connection Lost' : 'Active'}
          </span>
        </div>
      </header>

      <main 
        id="main-content"
        ref={mainContentRef}
        className="main-content"
        tabIndex={-1}
      >
        <section className="captain-section" aria-labelledby="captain-info">
          <div className="character-card" role="banner">
            <div className="character-avatar" aria-hidden="true">👨‍💼</div>
            <div className="character-info">
              <h3 id="captain-info">{CHARACTERS.HOLT.name}</h3>
              <p>{CHARACTERS.HOLT.title}</p>
              <blockquote cite="Brooklyn Nine-Nine">
                "{CHARACTERS.HOLT.quote}"
              </blockquote>
            </div>
          </div>

          <article className="mission-briefing" aria-labelledby="mission-title">
            <h3 id="mission-title">
              <span aria-hidden="true">🎯</span>
              Mission: The Ultimate Heist
            </h3>
            <p>
              Hedef: <strong>"Kutsal 41AT Otobüs Kartı"</strong>
            </p>
            <p>
              Son konumu: Tarihi Fırın'ın altındaki gizli laboratuvar
            </p>
            <div className="urgency" role="alert">
              <span className="sr-only">Urgent:</span>
              {CHARACTERS.TERRY.quote}
            </div>
          </article>
        </section>

        <section className="evidence-locker" aria-labelledby="vault-title">
          <div className="vault-door">
            <h3 id="vault-title">
              <span aria-hidden="true">🔐</span>
              Digital Evidence Vault
            </h3>
            
            <div className="encrypted-data">
              <label htmlFor="encrypted-evidence">
                Şifrelenmiş Kanıt:
              </label>
              <div 
                id="encrypted-evidence"
                className="ciphertext-display"
                role="textbox"
                aria-readonly="true"
                aria-describedby="encryption-info"
              >
                <code aria-label="Encrypted evidence data">
                  {ENCRYPTED_FLAG}
                </code>
              </div>
              <small id="encryption-info">
                <span aria-hidden="true">🔒</span>
                AES-256 ile şifrelendi (Jake'in iddiası)
              </small>
            </div>

            {error && (
              <div 
                ref={errorRef}
                className="error-display"
                role="alert"
                aria-live="assertive"
                tabIndex={-1}
                aria-describedby="error-description"
              >
                <p id="error-description">{error}</p>
                <small>Konsol'u kontrol edin veya network bağlantısını yeniden deneyin</small>
              </div>
            )}

            <button 
              onClick={handleDecrypt}
              onKeyDown={handleDecryptKeyDown}
              className={`decrypt-btn ${isDecrypting ? 'loading' : ''}`}
              disabled={!!error || isDecrypting}
              aria-describedby="decrypt-status"
              aria-label="Decrypt evidence data"
            >
              <span aria-hidden="true">
                {isDecrypting ? '🔄' : '🔓'}
              </span>
              <span id="decrypt-status">
                {isDecrypting ? 'Decrypting...' : 'Decrypt Evidence'}
              </span>
            </button>
          </div>
        </section>
      </main>

      {/* Debug panel for accessibility */}
      <aside className="debug-panel" role="complementary" aria-labelledby="debug-title">
        <h4 id="debug-title">
          <span aria-hidden="true">💻</span>
          System Debug Information
        </h4>
        <div className="debug-info">
          <p>Sistem durumu analiz ediliyor...</p>
          <ul>
            <li>Encryption status: <code aria-label="Active">ACTIVE</code></li>
            <li>Network connection: <code aria-label={error ? "Failed" : "Connected"}>{error ? 'FAILED' : 'OK'}</code></li>
            <li>Evidence integrity: <code aria-label="Verified">VERIFIED</code></li>
          </ul>
        </div>
      </aside>
    </div>
  );
};

export default Dashboard;