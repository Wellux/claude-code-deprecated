# WelluxAI Secure Backend

Ein sicheres Backend für die WelluxAI-Plattform mit modernen Best Practices und JWT-Authentifizierung.

## Features

- [✅] Sichere JWT-Authentifizierung
- [✅] TypeScript mit Strict Mode
- [✅] Zod-Validierung für Eingabedaten
- [✅] Rate-Limiting für Sicherheit
- [✅] Helmet für HTTP-Header-Sicherheit
- [✅] CORS-Konfiguration
- [✅] Strukturierte Fehlerbehandlung

## Installation

Folge diesen Schritten, um das Backend einzurichten:

```bash
# 1. In das Verzeichnis wechseln
cd server

# 2. Abhängigkeiten installieren
npm install

# 3. Typdeklarationen installieren (behebt TypeScript-Fehler)
npm install --save-dev @types/node @types/express @types/cors @types/helmet @types/morgan @types/cookie-parser @types/jsonwebtoken @types/bcrypt @types/express-rate-limit

# 4. Entwicklungsserver starten
npm run dev
```

## API-Endpunkte

- **POST /api/register** - Benutzerregistrierung
- **POST /api/login** - Benutzeranmeldung
- **POST /api/logout** - Benutzerabmeldung
- **GET /api/me** - Aktuelle Benutzerinformationen (authentifiziert)

## Umgebungsvariablen

Erstelle eine `.env`-Datei im Stammverzeichnis des Servers mit folgenden Variablen:

```env
NODE_ENV=development
PORT=3001
JWT_SECRET=dein_sehr_sicheres_geheimnis_mindestens_32_zeichen
JWT_EXPIRES_IN=1d
CORS_ORIGIN=http://localhost:5000
```

## Hinweise zur Entwicklung

- **Strict TypeScript**: Alle Typen müssen explizit definiert werden
- **TDD-Ansatz**: Tests sind mit Jest implementiert
- **API-Validierung**: Zod wird für die Eingabevalidierung verwendet

## Integration mit dem Frontend

Die Frontend-Anwendung wurde bereits aktualisiert, um mit diesem Backend zu kommunizieren. Die Auth-Services im Frontend nutzen den Endpunkt auf Port 3001.
