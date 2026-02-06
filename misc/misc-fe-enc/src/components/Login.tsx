import React, { useState, useRef, useEffect } from 'react';
import { LOGIN_CONFIG, CHARACTERS, ERROR_MESSAGES } from '../constants/config';
import './Login.css';

interface LoginProps {
  onLoginSuccess: () => void;
}

const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const passwordInputRef = useRef<HTMLInputElement>(null);
  const errorRef = useRef<HTMLDivElement>(null);

  // Focus password input on mount
  useEffect(() => {
    if (passwordInputRef.current) {
      passwordInputRef.current.focus();
    }
  }, []);

  // Focus error message when error appears
  useEffect(() => {
    if (error && errorRef.current) {
      errorRef.current.focus();
    }
  }, [error]);

  // Boyle'un "güvenli" şifre kontrol fonksiyonu (tamamen client-side!)
  const checkPassword = (inputPassword: string): boolean => {
    const decodedPassword = atob(LOGIN_CONFIG.encodedPassword);
    return inputPassword === decodedPassword;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Fake loading animation (çok profesyonel!)
    setTimeout(() => {
      if (checkPassword(password)) {
        console.log('🎉 Boyle Gate bypassed! Giriş başarılı!');
        onLoginSuccess();
      } else {
        setError(ERROR_MESSAGES.WRONG_PASSWORD);
      }
      setLoading(false);
    }, 1000);
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
    // Clear error when user starts typing again
    if (error) {
      setError('');
    }
  };

  return (
    <div className="login-container">
      {/* Skip link for keyboard navigation */}
      <a href="#login-form" className="skip-link sr-only">
        Skip to login form
      </a>

      <div className="login-card fade-in">
        <header className="precinct-header">
          <h1>🚔 HAMAM KASA</h1>
          <h2>Davutpaşa Login Terminali</h2>
          <div className="subtitle">YTÜ Değişim Programı 2026</div>
        </header>

        <section className="character-info" role="banner" aria-labelledby="character-name">
          <div className="character-avatar" aria-hidden="true">👨‍🍳</div>
          <div className="character-details">
            <h3 id="character-name">{CHARACTERS.BOYLE.name}</h3>
            <p>{CHARACTERS.BOYLE.title}</p>
            <blockquote cite="Brooklyn Nine-Nine">"{CHARACTERS.BOYLE.quote}"</blockquote>
          </div>
        </section>

        <main>
          <form 
            id="login-form"
            onSubmit={handleSubmit} 
            className="login-form"
            noValidate
            aria-describedby="security-note"
          >
            <div className="form-group">
              <label htmlFor="password">
                Güvenlik Şifresi:
                <span className="hint">
                  Gizli şifreyi bulup sisteme giriş yapın
                </span>
              </label>
              <input
                ref={passwordInputRef}
                type="password"
                id="password"
                name="password"
                value={password}
                onChange={handlePasswordChange}
                placeholder="Şifreyi girin..."
                className={error ? 'error' : ''}
                disabled={loading}
                required
                aria-invalid={error ? 'true' : 'false'}
                aria-describedby={error ? 'password-error' : undefined}
                autoComplete="current-password"
              />
            </div>

            {error && (
              <div 
                ref={errorRef}
                id="password-error"
                className="error-message"
                role="alert"
                aria-live="polite"
                tabIndex={-1}
              >
                {error}
              </div>
            )}

            <button 
              type="submit" 
              className={`submit-btn ${loading ? 'loading' : ''}`}
              disabled={loading || !password.trim()}
              aria-describedby="submit-status"
            >
              <span aria-hidden="true">
                {loading ? '🔄' : '🔐'}
              </span>
              <span id="submit-status">
                {loading ? 'Güvenlik kontrolleri yapılıyor...' : 'Sisteme Giriş'}
              </span>
            </button>
          </form>
        </main>

        <aside className="security-note" id="security-note" role="complementary">
          <p>
            <span aria-hidden="true">🛡️</span>
            Bu sistem Boyle'un patentli "Multi-Layer Security" teknolojisi ile korunmaktadır.
          </p>
          <p>
            <small>
              Sistem kararlılığı: %99.9 (Davutpaşa rüzgar koşullarında)
            </small>
          </p>
        </aside>

        <div className="pizza-easter-egg" aria-hidden="true" role="img" aria-label="Pizza decoration">
          🍕🍕🍕🍕🍕
        </div>
      </div>
    </div>
  );
};

export default Login;