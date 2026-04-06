/**
 * Benutzerverwaltungssystem für WelluxAI
 * 
 * Dies ist eine clientseitige Simulation eines Benutzerverwaltungssystems.
 * In einer Produktionsumgebung würde dies durch ein echtes Backend mit Datenbank ersetzt werden.
 * 
 * Erweitert mit OAuth-Authentifizierung (Google) und verbesserten Funktionen.
 */

class UserSystem {
    constructor() {
        this.users = this.loadUsers();
        this.currentUser = this.loadCurrentUser();
        this.savedPrompts = this.loadSavedPrompts();
        this.oauthSessions = this.loadOAuthSessions();
    }
    
    // Benutzer aus dem LocalStorage laden
    loadUsers() {
        const savedUsers = localStorage.getItem('wellux_users');
        if (savedUsers) {
            try {
                return JSON.parse(savedUsers);
            } catch (e) {
                console.error('Fehler beim Laden der Benutzerdaten:', e);
                return {};
            }
        }
        return this.getInitialUsers();
    }
    
    // OAuth-Sitzungen aus dem LocalStorage laden
    loadOAuthSessions() {
        const sessions = localStorage.getItem('wellux_oauth_sessions');
        if (sessions) {
            try {
                return JSON.parse(sessions);
            } catch (e) {
                console.error('Fehler beim Laden der OAuth-Sitzungen:', e);
                return {};
            }
        }
        return {};
    }
    
    // Aktuellen Benutzer aus dem LocalStorage laden
    loadCurrentUser() {
        const currentUser = localStorage.getItem('wellux_current_user');
        if (currentUser) {
            try {
                return JSON.parse(currentUser);
            } catch (e) {
                console.error('Fehler beim Laden des aktuellen Benutzers:', e);
                return null;
            }
        }
        return null;
    }
    
    // Gespeicherte Prompts aus dem LocalStorage laden
    loadSavedPrompts() {
        const savedPrompts = localStorage.getItem('wellux_saved_prompts');
        if (savedPrompts) {
            try {
                return JSON.parse(savedPrompts);
            } catch (e) {
                console.error('Fehler beim Laden der gespeicherten Prompts:', e);
                return {};
            }
        }
        return {};
    }
    
    // Benutzer im LocalStorage speichern
    saveUsers() {
        localStorage.setItem('wellux_users', JSON.stringify(this.users));
    }
    
    // Aktuellen Benutzer im LocalStorage speichern
    saveCurrentUser() {
        if (this.currentUser) {
            localStorage.setItem('wellux_current_user', JSON.stringify(this.currentUser));
        } else {
            localStorage.removeItem('wellux_current_user');
        }
    }
    
    // Gespeicherte Prompts im LocalStorage speichern
    saveSavedPrompts() {
        localStorage.setItem('wellux_saved_prompts', JSON.stringify(this.savedPrompts));
    }
    
    // OAuth-Sitzungen im LocalStorage speichern
    saveOAuthSessions() {
        localStorage.setItem('wellux_oauth_sessions', JSON.stringify(this.oauthSessions));
    }
    
    // Neuen Benutzer registrieren
    register(name, email, password) {
        // Prüfen, ob die E-Mail bereits verwendet wird
        if (this.findUserByEmail(email)) {
            return { success: false, message: 'Diese E-Mail-Adresse wird bereits verwendet.' };
        }
        
        // Neuen Benutzer erstellen
        const userId = this.generateId();
        const newUser = {
            id: userId,
            name: name,
            email: email,
            password: this.hashPassword(password), // In einer echten Anwendung würde ein sicherer Hash verwendet werden
            created: new Date().toISOString(),
            authType: 'local', // Standardmäßige Authentifizierungsmethode
            preferences: {
                theme: 'light',
                language: 'de'
            }
        };
        
        // Benutzer speichern
        this.users[userId] = newUser;
        this.saveUsers();
        
        // Gespeicherte Prompts für den Benutzer initialisieren
        this.savedPrompts[userId] = [];
        this.saveSavedPrompts();
        
        // Automatisch einloggen
        this.currentUser = { ...newUser };
        delete this.currentUser.password; // Passwort aus dem aktuellen Benutzer entfernen
        this.saveCurrentUser();
        
        return { success: true, user: this.currentUser };
    }
    
    // Registrierung mit OAuth-Anbieter
    registerWithOAuth(data) {
        if (!data || !data.provider || !data.email) {
            return { success: false, message: 'Unvollständige OAuth-Daten.' };
        }
        
        // Prüfen, ob die E-Mail bereits verwendet wird
        const existingUser = this.findUserByEmail(data.email);
        if (existingUser && existingUser.authType === 'local') {
            return { success: false, message: 'Diese E-Mail-Adresse wird bereits mit einem lokalen Konto verwendet.' };
        }
        
        // Neuen Benutzer erstellen
        const userId = this.generateId();
        const newUser = {
            id: userId,
            name: data.name || data.email.split('@')[0],
            email: data.email,
            created: new Date().toISOString(),
            authType: 'oauth',
            oauthProvider: data.provider,
            oauthId: data.id,
            profilePicture: data.picture || null,
            preferences: {
                theme: 'light',
                language: 'de'
            }
        };
        
        // Benutzer speichern
        this.users[userId] = newUser;
        this.saveUsers();
        
        // OAuth-Sitzung speichern
        this.oauthSessions[`${data.provider}_${data.id}`] = {
            userId: userId,
            token: data.token,
            timestamp: new Date().toISOString()
        };
        this.saveOAuthSessions();
        
        // Gespeicherte Prompts für den Benutzer initialisieren
        this.savedPrompts[userId] = [];
        this.saveSavedPrompts();
        
        // Automatisch einloggen
        this.currentUser = { ...newUser };
        this.saveCurrentUser();
        
        return { success: true, user: this.currentUser };
    }
    
    // Benutzer einloggen
    login(email, password) {
        const user = this.findUserByEmail(email);
        
        if (!user) {
            return { success: false, message: 'Benutzerkonto mit dieser E-Mail-Adresse nicht gefunden.' };
        }
        
        if (user.authType === 'oauth') {
            return { success: false, message: 'Dieses Konto verwendet Social Login. Bitte nutzen Sie die entsprechende Anmeldeoption.' };
        }
        
        if (user.password !== this.hashPassword(password)) {
            return { success: false, message: 'Falsches Passwort.' };
        }
        
        // Benutzer einloggen
        this.currentUser = { ...user };
        delete this.currentUser.password; // Passwort aus dem aktuellen Benutzer entfernen
        this.saveCurrentUser();
        
        return { success: true, user: this.currentUser };
    }
    
    // Einloggen mit OAuth
    loginWithOAuth(data) {
        if (!data || !data.provider || !data.email) {
            return { success: false, message: 'Unvollständige OAuth-Daten.' };
        }
        
        // Benutzer suchen
        const user = this.findUserByEmail(data.email);
        
        if (!user) {
            return { success: false, message: 'Kein Benutzerkonto mit dieser E-Mail-Adresse gefunden. Bitte registrieren Sie sich zuerst.' };
        }
        
        // OAuth-Sitzung speichern oder aktualisieren
        this.oauthSessions[`${data.provider}_${data.id}`] = {
            userId: user.id,
            token: data.token,
            timestamp: new Date().toISOString()
        };
        this.saveOAuthSessions();
        
        // Benutzer einloggen
        this.currentUser = { ...user };
        this.saveCurrentUser();
        
        return { success: true, user: this.currentUser };
    }
    
    // Benutzer ausloggen
    logout() {
        this.currentUser = null;
        this.saveCurrentUser();
        return { success: true };
    }
    
    // Benutzer anhand der E-Mail-Adresse finden
    findUserByEmail(email) {
        return Object.values(this.users).find(user => user.email === email);
    }
    
    // Benutzer anhand der ID finden
    findUserById(id) {
        return this.users[id];
    }
    
    // Prüfen, ob ein Benutzer eingeloggt ist
    isLoggedIn() {
        return this.currentUser !== null;
    }
    
    // Aktuellen Benutzer abrufen
    getCurrentUser() {
        return this.currentUser;
    }
    
    // Prompt für den aktuellen Benutzer speichern
    savePrompt(prompt) {
        if (!this.isLoggedIn()) {
            return { success: false, message: 'Sie müssen eingeloggt sein, um Prompts zu speichern.' };
        }
        
        const userId = this.currentUser.id;
        if (!this.savedPrompts[userId]) {
            this.savedPrompts[userId] = [];
        }
        
        const promptId = this.generateId();
        const newPrompt = {
            id: promptId,
            text: prompt.text,
            title: prompt.title || 'Gespeicherter Prompt',
            category: prompt.category || 'Allgemein',
            created: new Date().toISOString()
        };
        
        this.savedPrompts[userId].push(newPrompt);
        this.saveSavedPrompts();
        
        return { success: true, prompt: newPrompt };
    }
    
    // Alle gespeicherten Prompts des aktuellen Benutzers abrufen
    getUserPrompts() {
        if (!this.isLoggedIn()) {
            return [];
        }
        
        const userId = this.currentUser.id;
        return this.savedPrompts[userId] || [];
    }
    
    // Einen gespeicherten Prompt löschen
    deletePrompt(promptId) {
        if (!this.isLoggedIn()) {
            return { success: false, message: 'Sie müssen eingeloggt sein, um Prompts zu löschen.' };
        }
        
        const userId = this.currentUser.id;
        if (!this.savedPrompts[userId]) {
            return { success: false, message: 'Keine gespeicherten Prompts gefunden.' };
        }
        
        const initialLength = this.savedPrompts[userId].length;
        this.savedPrompts[userId] = this.savedPrompts[userId].filter(prompt => prompt.id !== promptId);
        
        if (this.savedPrompts[userId].length === initialLength) {
            return { success: false, message: 'Prompt nicht gefunden.' };
        }
        
        this.saveSavedPrompts();
        return { success: true };
    }
    
    // Benutzerpräferenzen aktualisieren
    updatePreferences(preferences) {
        if (!this.isLoggedIn()) {
            return { success: false, message: 'Sie müssen eingeloggt sein, um Ihre Präferenzen zu aktualisieren.' };
        }
        
        const userId = this.currentUser.id;
        const user = this.users[userId];
        
        if (!user) {
            return { success: false, message: 'Benutzer nicht gefunden.' };
        }
        
        user.preferences = { ...user.preferences, ...preferences };
        this.users[userId] = user;
        this.saveUsers();
        
        // Aktuellen Benutzer aktualisieren
        this.currentUser.preferences = { ...this.currentUser.preferences, ...preferences };
        this.saveCurrentUser();
        
        return { success: true, preferences: user.preferences };
    }
    
    // Einfacher Hash für Passwörter (NICHT für Produktion verwenden!)
    hashPassword(password) {
        // In einer echten Anwendung würde ein sicherer Hash wie bcrypt verwendet werden
        // Dies ist nur eine einfache Simulation
        let hash = 0;
        for (let i = 0; i < password.length; i++) {
            const char = password.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return hash.toString(16);
    }
    
    // Einfache ID-Generierung
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
    
    // Anfängliche Beispielbenutzer (nur für Demozwecke)
    getInitialUsers() {
        const demoUserId = 'demo123';
        const googleDemoUserId = 'google_demo456';
        const users = {};
        
        users[demoUserId] = {
            id: demoUserId,
            name: 'Demo Benutzer',
            email: 'demo@example.com',
            password: this.hashPassword('password123'),
            created: '2025-01-01T00:00:00.000Z',
            authType: 'local',
            preferences: {
                theme: 'light',
                language: 'de'
            }
        };
        
        users[googleDemoUserId] = {
            id: googleDemoUserId,
            name: 'Google Demo',
            email: 'google.demo@example.com',
            created: '2025-01-01T00:00:00.000Z',
            authType: 'oauth',
            oauthProvider: 'google',
            oauthId: '12345678901234567890',
            profilePicture: 'https://ui-avatars.com/api/?name=Google+Demo&background=0D8ABC&color=fff',
            preferences: {
                theme: 'light',
                language: 'de'
            }
        };
        
        // Gespeicherte Prompts für den Demo-Benutzer
        this.savedPrompts[demoUserId] = [
            {
                id: 'prompt1',
                title: 'KI-Strategie für KMU',
                text: 'Erstelle mir eine KI-Implementierungsstrategie für ein mittelständisches Unternehmen mit 50 Mitarbeitern im Fertigungsbereich. Berücksichtige dabei die begrenzten Ressourcen und fehlende IT-Expertise.',
                category: 'Strategie',
                created: '2025-04-15T10:30:00.000Z'
            },
            {
                id: 'prompt2',
                title: 'Datenqualitäts-Checkliste',
                text: 'Erstelle eine Checkliste zur Überprüfung der Datenqualität vor der Implementierung von Machine Learning Modellen. Die Liste sollte für Nicht-Experten verständlich sein.',
                category: 'Daten',
                created: '2025-04-20T14:45:00.000Z'
            }
        ];
        
        return users;
    }
}

// Globale Instanz erstellen
window.WelluxUsers = new UserSystem();
