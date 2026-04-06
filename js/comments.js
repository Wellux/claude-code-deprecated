/**
 * Kommentarsystem für den WelluxAI Blog
 * 
 * Dies ist eine clientseitige Simulation eines Kommentarsystems.
 * In einer Produktionsumgebung würden diese Daten in einer Datenbank gespeichert.
 */

// Kommentare im LocalStorage speichern
class CommentSystem {
    constructor() {
        this.comments = this.loadComments();
    }
    
    // Lade Kommentare aus dem LocalStorage
    loadComments() {
        const savedComments = localStorage.getItem('wellux_comments');
        if (savedComments) {
            try {
                return JSON.parse(savedComments);
            } catch (e) {
                console.error('Fehler beim Laden der Kommentare:', e);
                return {};
            }
        }
        return this.getInitialComments();
    }
    
    // Speichere Kommentare im LocalStorage
    saveComments() {
        localStorage.setItem('wellux_comments', JSON.stringify(this.comments));
    }
    
    // Füge einen neuen Kommentar hinzu
    addComment(postId, name, email, content) {
        if (!this.comments[postId]) {
            this.comments[postId] = [];
        }
        
        const newComment = {
            id: this.generateId(),
            name: name,
            email: email,
            content: content,
            date: new Date().toISOString(),
            approved: true // In einer echten Implementierung würde dies standardmäßig auf false gesetzt werden
        };
        
        this.comments[postId].unshift(newComment);
        this.saveComments();
        
        return newComment;
    }
    
    // Generiere eine einfache ID für Kommentare
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
    
    // Hole alle Kommentare für einen bestimmten Blogbeitrag
    getCommentsForPost(postId) {
        return this.comments[postId] || [];
    }
    
    // Entferne einen Kommentar
    removeComment(postId, commentId) {
        if (this.comments[postId]) {
            this.comments[postId] = this.comments[postId].filter(comment => comment.id !== commentId);
            this.saveComments();
            return true;
        }
        return false;
    }
    
    // Anfängliche Beispielkommentare (nur für Demozwecke)
    getInitialComments() {
        return {
            'handwerk-ki': [
                {
                    id: 'demo1',
                    name: 'Thomas Schmidt',
                    email: 'thomas.schmidt@example.com',
                    content: 'Sehr interessanter Artikel! Ich arbeite selbst in einer Schreinerei und bin überrascht, wie viel Potential KI auch in unserem Handwerk bietet.',
                    date: '2025-05-20T15:23:42.000Z',
                    approved: true
                },
                {
                    id: 'demo2',
                    name: 'Maria Berger',
                    email: 'maria@example.com',
                    content: 'Gibt es auch Beispiele für den Einsatz in kleineren Betrieben mit weniger als 5 Mitarbeitern? Ich frage mich, ob sich die Investition für uns lohnen würde.',
                    date: '2025-05-19T09:15:30.000Z',
                    approved: true
                }
            ],
            'prompt-engineering': [
                {
                    id: 'demo3',
                    name: 'Michael Weber',
                    email: 'michael@example.com',
                    content: 'Danke für die praktischen Tipps! Habe gleich mit meinem Team ein paar der vorgeschlagenen Prompt-Strukturen ausprobiert und die Ergebnisse sind deutlich besser.',
                    date: '2025-05-22T11:42:15.000Z',
                    approved: true
                }
            ]
        };
    }
}

// Globale Instanz erstellen
window.WelluxComments = new CommentSystem();
