/**
 * OAuth-Manager für WelluxAI
 * 
 * Diese Datei implementiert OAuth-Authentifizierung mit verschiedenen Anbietern,
 * insbesondere Google Sign-In.
 */

class OAuthManager {
    constructor() {
        // Test-Client-ID für die Entwicklungsumgebung
        // HINWEIS: Diese Client-ID ist nur für Testzwecke und würde in der Produktion ersetzt werden
        this.googleClientId = '735097041062-l3pfg24kl21t4q2s73ftj8k14ti3c0v5.apps.googleusercontent.com';
        this.googleScopes = 'profile email';
        this.isGoogleApiLoaded = false;
        
        // Debug-Modus aktivieren
        this.debug = true;
        
        // Event-Listener für OAuth-Anbieter initialisieren
        this.initOAuthProviders();
        
        this.log('OAuthManager initialisiert mit Client-ID:', this.truncateForLog(this.googleClientId));
    }
    
    /**
     * Protokolliert Debug-Informationen in der Konsole
     * @private
     */
    log(...args) {
        if (this.debug) {
            console.log('[OAuthManager]', ...args);
        }
    }
    
    /**
     * Kürzt lange Strings für die Protokollierung
     * @private
     */
    truncateForLog(str) {
        if (typeof str !== 'string' || str.length <= 10) return str;
        return str.substring(0, 6) + '...' + str.substring(str.length - 4);
    }
    
    /**
     * Initialisiert alle OAuth-Anbieter
     */
    initOAuthProviders() {
        // Google OAuth initialisieren
        this.loadGoogleApi();
        
        // Hier können in Zukunft weitere OAuth-Anbieter hinzugefügt werden
    }
    
    /**
     * Lädt die Google API für OAuth
     */
    loadGoogleApi() {
        // Prüfen, ob das Google API-Skript bereits geladen ist
        if (document.getElementById('google-api-script') || this.isGoogleApiLoaded) {
            return;
        }
        
        // Google API-Skript einfügen
        const script = document.createElement('script');
        script.id = 'google-api-script';
        script.src = 'https://accounts.google.com/gsi/client';
        script.async = true;
        script.defer = true;
        script.onload = () => {
            this.isGoogleApiLoaded = true;
            this.initGoogleSignIn();
        };
        
        document.head.appendChild(script);
    }
    
    /**
     * Initialisiert die Google Sign-In-Funktionalität
     */
    initGoogleSignIn() {
        if (!window.google || this.googleButton) return;
        
        // Google-Anmelde-Buttons initialisieren, wenn sie auf der Seite vorhanden sind
        const googleLoginButtons = document.querySelectorAll('[data-oauth="google"]');
        
        googleLoginButtons.forEach(buttonContainer => {
            // Google Identity Services für One Tap und Sign-In With Google
            google.accounts.id.initialize({
                client_id: this.googleClientId,
                callback: this.handleGoogleSignIn.bind(this),
                auto_select: false,
            });
            
            // Button rendern
            google.accounts.id.renderButton(buttonContainer, {
                type: 'standard',
                theme: 'outline',
                size: 'large',
                text: 'continue_with',
                shape: 'rectangular',
                logo_alignment: 'left',
                width: buttonContainer.offsetWidth
            });
        });
    }
    
    /**
     * Verarbeitet die Anmeldung über Google
     * @param {Object} response - Die Antwort von der Google OAuth API
     */
    handleGoogleSignIn(response) {
        if (!response || !response.credential) {
            console.error('Google Sign-In fehlgeschlagen: Keine gültigen Anmeldedaten.');
            showToast(WelluxTranslations.translate('toast_google_signin_error'), 'error');
            return;
        }
        
        try {
            // JWT-Token dekodieren (in einer Produktionsumgebung sollte dies serverseitig erfolgen)
            const token = response.credential;
            const payload = this.decodeJwt(token);
            
            if (!payload || !payload.email) {
                throw new Error('Ungültiges Token-Format');
            }
            
            // Benutzer mit Google-Daten anmelden oder registrieren
            this.loginWithGoogle(payload, token);
            
        } catch (error) {
            console.error('Fehler bei der Google-Anmeldung:', error);
            showToast(WelluxTranslations.translate('toast_google_signin_error'), 'error');
        }
    }
    
    /**
     * Dekodiert ein JWT-Token
     * @param {string} token - Das zu dekodierende JWT-Token
     * @returns {Object} Die dekodierten Daten
     */
    decodeJwt(token) {
        try {
            // JWT besteht aus drei Teilen: Header, Payload und Signatur, getrennt durch Punkte
            const parts = token.split('.');
            if (parts.length !== 3) {
                throw new Error('Ungültiges JWT-Format');
            }
            
            // Base64Url-decodieren und als JSON parsen
            // Anmerkung: In einer echten Anwendung sollte die Signatur überprüft werden
            const payload = parts[1].replace(/-/g, '+').replace(/_/g, '/');
            const decoded = JSON.parse(atob(payload));
            
            return decoded;
            
        } catch (error) {
            console.error('JWT-Dekodierungsfehler:', error);
            return null;
        }
    }
    
    /**
     * Führt Login oder Registrierung mit Google-Daten durch
     * @param {Object} userData - Benutzerdaten von Google
     * @param {string} token - Das Google-Token für zukünftige API-Anfragen
     */
    async loginWithGoogle(userData, token) {
        if (!window.WelluxAuth) {
            console.error('Authentifizierungssystem nicht geladen.');
            showToast('Authentifizierungssystem nicht verfügbar', 'error');
            return;
        }
        
        try {
            // Google-Token an Backend senden für Authentifizierung
            const response = await fetch(`${window.WelluxAuth.apiBaseUrl}/auth/google`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    token: token,
                    userData: {
                        sub: userData.sub,
                        email: userData.email,
                        name: userData.name,
                        picture: userData.picture
                    }
                }),
                credentials: 'include'
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Benutzer in lokalen Speicher laden
                window.WelluxAuth.saveUserToStorage(result.data.user, result.data.token);
                window.WelluxAuth.currentUser = result.data.user;
                
                // Event auslösen
                document.dispatchEvent(new CustomEvent('userLoggedIn', { detail: result.data.user }));
                
                // Erfolgsnachricht anzeigen
                const message = result.data.isNewUser ? 
                    'Ihr Google-Konto wurde erfolgreich registriert' : 
                    'Sie haben sich erfolgreich mit Google angemeldet';
                    
                showToast(message, 'success');
                
                // Zur Dashboard-Seite weiterleiten
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1000);
            } else {
                throw new Error(result.message || 'Anmeldung mit Google fehlgeschlagen');
            }
        } catch (error) {
            console.error('Google Login/Registrierung fehlgeschlagen:', error);
            showToast(error.message || 'Bei der Anmeldung mit Google ist ein Fehler aufgetreten', 'error');
        }
    }
    
    /**
     * Initialisiert alle OAuth-Elemente auf der aktuellen Seite
     */
    initPage() {
        if (this.isGoogleApiLoaded) {
            this.initGoogleSignIn();
        } else {
            this.loadGoogleApi();
        }
    }
}

// Globale Instanz erstellen
window.WelluxOAuth = new OAuthManager();

// Nach dem Laden der Seite initialisieren
document.addEventListener('DOMContentLoaded', () => {
    window.WelluxOAuth.initPage();
});
