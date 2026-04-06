/**
 * Secure Authentication Service
 * 
 * Diese Service-Klasse implementiert die sichere Kommunikation mit dem Backend-API
 * und ersetzt die vorherige clientseitige Authentifizierung.
 * 
 * @author Wellux Development Team
 * @version 1.1.0 (Bugfix: Korrigierte API-Endpunkte und verbesserte Fehlerbehandlung)
 */
class AuthService {
  constructor() {
    // Korrigierte API-Basis-URL
    this.apiBaseUrl = 'http://localhost:3001/api';
    this.currentUser = null;
    this.tokenKey = 'wellux_auth_token';
    this.userKey = 'wellux_user';
    this.cookieName = 'auth_token';
    
    // Debugging aktivieren
    this.debug = true;
    
    // Bei Initialisierung versuchen, den gespeicherten Benutzer zu laden
    this.loadUserFromStorage();
    
    this.log('AuthService initialisiert mit API-URL:', this.apiBaseUrl);
  }

  /**
   * Protokolliert Debug-Informationen in der Konsole
   * @private
   */
  log(...args) {
    if (this.debug) {
      console.log('[AuthService]', ...args);
    }
  }

  /**
   * Protokolliert Fehler in der Konsole
   * @private
   */
  error(...args) {
    console.error('[AuthService ERROR]', ...args);
  }

  /**
   * Versucht, den aktuellen Benutzer aus dem Local Storage zu laden
   * @private
   */
  loadUserFromStorage() {
    try {
      const token = localStorage.getItem(this.tokenKey);
      const userJson = localStorage.getItem(this.userKey);
      
      if (token && userJson) {
        this.currentUser = JSON.parse(userJson);
        this.log('Benutzer aus LocalStorage geladen:', this.currentUser);
        return true;
      }
    } catch (error) {
      this.error('Fehler beim Laden des Benutzers aus dem Speicher:', error);
      this.logout(); // Beim Fehler ausloggen
    }
    
    this.log('Kein Benutzer im LocalStorage gefunden');
    return false;
  }

  /**
   * Speichert den aktuellen Benutzer und Token im Local Storage
   * @param {Object} userData - Die Benutzerdaten
   * @param {string} token - Das JWT-Token
   * @private
   */
  saveUserToStorage(userData, token) {
    if (!userData || !token) {
      this.error('Ungültige Daten für LocalStorage', { userData: !!userData, token: !!token });
      return;
    }
    
    localStorage.setItem(this.tokenKey, token);
    localStorage.setItem(this.userKey, JSON.stringify(userData));
    this.log('Benutzerdaten im LocalStorage gespeichert');
  }

  /**
   * Sendet eine Anfrage an die API
   * @param {string} endpoint - Der API-Endpunkt
   * @param {Object} options - Die Fetch-Optionen
   * @returns {Promise<Object>} Die API-Antwort
   * @private
   */
  async fetchApi(endpoint, options = {}) {
    const url = `${this.apiBaseUrl}${endpoint}`;
    
    // Standard-Header
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };
    
    // Token hinzufügen, wenn vorhanden
    const token = localStorage.getItem(this.tokenKey);
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
    
    // Credentials für Cookies setzen
    if (!options.credentials) {
      options.credentials = 'include';
    }
    
    this.log(`API-Anfrage an ${url}`, { 
      method: options.method || 'GET',
      headers 
    });
    
    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });
      
      let data;
      try {
        data = await response.json();
      } catch (error) {
        this.error('Fehler beim Parsen der API-Antwort:', error);
        throw new Error('Ungültiges Antwortformat vom Server');
      }
      
      this.log(`API-Antwort von ${url}:`, data);
      
      if (!response.ok) {
        throw new Error(data.message || `HTTP-Fehler: ${response.status}`);
      }
      
      return data;
    } catch (error) {
      this.error(`API-Fehler bei ${url}:`, error);
      throw error;
    }
  }

  /**
   * Registriert einen neuen Benutzer
   * @param {Object} userData - Die Benutzerdaten
   * @returns {Promise<Object>} Die Antwort des Servers
   */
  async register(userData) {
    try {
      this.log('Registrierungsversuch mit:', { ...userData, password: '***' });
      
      const response = await this.fetchApi('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData)
      });
      
      return response;
    } catch (error) {
      this.error('Registrierungsfehler:', error);
      throw error;
    }
  }

  /**
   * Meldet einen Benutzer an
   * @param {string} email - Die E-Mail-Adresse
   * @param {string} password - Das Passwort
   * @returns {Promise<Object>} Die Antwort des Servers mit Token und Benutzerdaten
   */
  async login(email, password) {
    try {
      this.log('Login-Versuch mit:', { email });
      
      const response = await this.fetchApi('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
        credentials: 'include', // Wichtig für Cookies
      });
      
      this.log('Login-Antwort erhalten:', response);
      
      if (response.success && response.data) {
        const { user, token } = response.data;
        this.currentUser = user;
        this.saveUserToStorage(user, token);
        
        // Event auslösen
        document.dispatchEvent(new CustomEvent('userLoggedIn', { detail: user }));
        this.log('Benutzer erfolgreich angemeldet:', user);
      } else {
        this.error('Login fehlgeschlagen:', response.message || 'Unbekannter Fehler');
      }
      
      return response;
    } catch (error) {
      this.error('Login-Fehler:', error);
      throw error;
    }
  }

  /**
   * Meldet einen Benutzer ab
   * @returns {Promise<void>}
   */
  async logout() {
    try {
      this.log('Logout-Versuch');
      // API-Anfrage zum Ausloggen
      await this.fetchApi('/auth/logout', {
        method: 'POST',
        credentials: 'include',
      });
      
      this.log('Logout erfolgreich durchgeführt');
    } catch (error) {
      this.error('Fehler beim Ausloggen:', error);
    } finally {
      // Lokale Daten immer löschen, auch wenn die API-Anfrage fehlschlägt
      localStorage.removeItem(this.tokenKey);
      localStorage.removeItem(this.userKey);
      this.currentUser = null;
      
      // Event auslösen
      document.dispatchEvent(new CustomEvent('userLoggedOut'));
      this.log('Benutzer lokal ausgeloggt');
    }
  }

  /**
   * Ruft die Daten des aktuellen Benutzers ab
   * @returns {Promise<Object>} Die Benutzerdaten
   */
  async getCurrentUser() {
    try {
      if (!this.isLoggedIn()) {
        this.log('Kein Benutzer angemeldet, getCurrentUser() abgebrochen');
        return null;
      }
      
      this.log('Aktuelle Benutzerdaten abrufen...');
      // Aktualisierte Benutzerdaten vom Server holen
      const response = await this.fetchApi('/auth/me', {
        credentials: 'include'
      });
      
      if (response.success && response.data) {
        this.log('Benutzerdaten erfolgreich aktualisiert:', response.data);
        this.currentUser = response.data;
        this.saveUserToStorage(this.currentUser, localStorage.getItem(this.tokenKey));
      } else {
        this.error('Keine gültigen Benutzerdaten erhalten');
      }
      
      return this.currentUser;
    } catch (error) {
      this.error('Fehler beim Abrufen des aktuellen Benutzers:', error);
      // Bei Authentifizierungsfehlern ausloggen
      if (error.message?.includes('Token') || error.message?.includes('Authentifizierung')) {
        this.log('Authentifizierungsfehler, Benutzer wird ausgeloggt');
        this.logout();
      }
      return null;
    }
  }

  /**
   * Überprüft, ob ein Benutzer angemeldet ist
   * @returns {boolean} True, wenn ein Benutzer angemeldet ist
   */
  isLoggedIn() {
    const isLoggedIn = !!this.currentUser && !!localStorage.getItem(this.tokenKey);
    this.log('isLoggedIn() =>', isLoggedIn);
    return isLoggedIn;
  }

  /**
   * Aktualisiert die Benutzereinstellungen
   * @param {Object} preferences - Die zu aktualisierenden Einstellungen
   * @returns {Promise<Object>} Die Antwort des Servers
   */
  async updatePreferences(preferences) {
    if (!this.isLoggedIn()) {
      throw new Error('Benutzer nicht angemeldet');
    }
    
    // Hier würde die API-Anfrage zur Aktualisierung der Einstellungen erfolgen
    // In diesem Beispiel implementieren wir die Endpunkte noch nicht
    this.log('API-Endpunkt für Präferenz-Aktualisierung noch nicht implementiert');
    return { success: true };
  }
}

// Globale Instanz erstellen
window.WelluxAuth = new AuthService();