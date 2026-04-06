# WelluxAI - KI-Lösungen & Digitalisierungsberatung

![Version](https://img.shields.io/badge/Version-2.1.0-blue) ![Status](https://img.shields.io/badge/Status-Beta-orange) ![Last Updated](https://img.shields.io/badge/Last%20Updated-25.05.2025-green)

## 📋 Projekt-Übersicht

WelluxAI bietet moderne KI-Lösungen und Digitalisierungsberatung für Unternehmen aller Größen mit Schwerpunkt auf dem bayerischen Mittelstand. Die Plattform ermöglicht eine nahtlose KI-Integration in bestehende Geschäftsprozesse durch spezialisierte Tools, branchenspezifische Lösungen und umfassende Ressourcen zur Geschäftsprozessoptimierung.

### 🎯 Hauptziele

- Demokratisierung von KI-Technologien für Unternehmen jeder Größe.
- Beschleunigung der digitalen Transformation durch maßgeschneiderte Lösungen.
- Optimierung von Geschäftsprozessen durch intelligente Automatisierung.
- Steigerung der Wettbewerbsfähigkeit durch datengestützte Entscheidungsfindung.

### 🔑 Alleinstellungsmerkmale

- Branchenspezifische KI-Lösungen mit Fokus auf lokale Märkte.
- Integrierte ROI-Berechnung für KI-Investitionen.
- Umfassende Prompt-Bibliothek für verschiedene Anwendungsfälle.
- KI-Readiness Assessment für individualisierte Transformationspläne.

## 🚀 Quick Start

### Voraussetzungen

- Node.js v20.x oder höher
- npm v10.x oder höher
- MongoDB v6.0 oder höher (für Backend-Funktionalitäten)

### Installation & Lokaler Start

1. **Repository klonen:**

    ```bash
    git clone https://github.com/welluxai/website.git
    cd website
    ```

2. **Frontend starten:**
    Stellt die statischen Webseiten-Inhalte bereit.

    ```bash
    npm install -g live-server
    live-server --port=5000
    ```

    Das Frontend ist nun unter `http://localhost:5000` erreichbar.

3. **Backend starten (optional, für dynamische Features):**
    Wird für Benutzerauthentifizierung, Datenbankinteraktionen und API-Endpunkte benötigt.
    Öffnen Sie ein neues Terminalfenster:

    ```bash
    cd server
    npm install
    # Umgebungsvariablen konfigurieren (siehe Abschnitt '⚙️ Konfiguration')
    cp .env.example .env 
    # .env anpassen
    npm run dev
    ```

    Das Backend läuft standardmäßig auf Port `3001`.

### Zugangsdaten für Demo-Bereich

| Rolle     | Benutzername      | Passwort    |
|-----------|-------------------|-------------|
| Admin     | [admin@wellux.ai](mailto:admin@wellux.ai)   | WelluxDemo1 |
| Benutzer  | [demo@wellux.ai](mailto:demo@wellux.ai)    | Demo2025!   |

## ✨ Features

Eine detaillierte Übersicht über implementierte und geplante Features.

### Implementierte Features (Stand 25.05.2025)

| Feature-Bereich                | Feature                                                       | Status | Beschreibung                                                                          | Fertigstellung |
|--------------------------------|---------------------------------------------------------------|--------|---------------------------------------------------------------------------------------|----------------|
| **Landing Page**               | Dynamische Haupt-Überschrift                                  | ✅     | Anpassbare Hero-Section-Texte.                                                        | 20.05.2025     |
|                                | Call-to-Action Buttons                                        | ✅     | Klare Handlungsaufforderungen.                                                        | 01.05.2025     |
|                                | Service-Übersicht (Teaser)                                    | ✅     | Kurze Vorstellung der Hauptdienstleistungen.                                         | 10.05.2025     |
|                                | Use Case Teaser                                               | ✅     | Anreißer für Erfolgsgeschichten/Anwendungsbeispiele.                                  | 15.05.2025     |
|                                | Newsletter-Anmeldung                                          | ✅     | Einfache Anmeldung für Updates.                                                       | 01.05.2025     |
|                                | Trust Elemente (Placeholder)                                  | 🚧     | Bereich für Kundenlogos/Partnerlogos vorbereitet.                                     | Laufend        |
| **Allgemeine UI/UX & Navigation**| Responsives Design (Mobile-First)                             | ✅     | Optimale Darstellung auf allen Geräten.                                               | 05.05.2025     |
|                                | Dark Mode & Light Mode                                        | ✅     | Theme-Auswahl für bessere Lesbarkeit.                                                 | 26.05.2025     |
|                                | Modernisierte Überschriften-Designs                           | ✅     | Verbessertes visuelles Erscheinungsbild.                                              | 26.05.2025     |
|                                | Optimierte Navigation mit Dropdown-Menüs                      | ✅     | Verbesserte Menüführung für komplexe Inhalte.                                         | 27.05.2025     |
|                                | Standardisierte Header/Footer Einbindung                      | ✅     | Konsistentes Erscheinungsbild auf allen Seiten.                                       | 28.05.2025     |
|                                | Optimiertes Mobile-Menü                                       | ✅     | Verbesserte Benutzerfreundlichkeit auf mobilen Geräten.                               | 22.05.2025     |
|                                | Design- und Kontrast-Probleme behoben                         | ✅     | Erhöhte Lesbarkeit und Zugänglichkeit gemäß WCAG-Richtlinien.                         | 22.05.2025     |
|                                | Unterseiten-Design vereinheitlicht und optimiert              | ✅     | Konsistentes Erscheinungsbild über alle Unterseiten hinweg.                           | 22.05.2025     |
|                                | Blog und KI-Tools Directory für Dark & Light Mode optimiert   | ✅     | Optimale Darstellung der Inhalte in beiden Themes.                                    | 26.05.2025     |
|                                | Lesbarkeit in beiden Themes verbessert                        | ✅     | Anpassung von Schriftgrößen und Kontrasten für bessere Lesbarkeit.                    | 26.05.2025     |
|                                | Landingpage verschlankt                                       | ✅     | Reduktion von Inhalten auf der Startseite, Auslagerung auf dedizierte Unterseiten.    | 27.05.2025     |
| **Kernfunktionalität & Inhalt**| Mehrsprachigkeit (DE/EN)                                      | ✅     | Inhalte in Deutsch und Englisch verfügbar.                                            | 10.05.2025     |
|                                | Blog-System mit Kategorien & Tags                             | ✅     | Artikel erstellen, verwalten und filtern.                                             | 15.05.2025     |
|                                | KI-Tools Verzeichnis                                          | ✅     | Übersicht und Detailseiten für KI-Anwendungen.                                        | 18.05.2025     |
|                                | Kontaktformular & Interaktive Karte                           | ✅     | Standard-Kontaktmöglichkeiten und Anfahrtsplan.                                       | 05.05.2025     |
| **Benutzer & Sicherheit**      | Benutzerregistrierung & Login (E-Mail/Passwort & OAuth Google)| ✅     | Sichere Kontoerstellung und Anmeldung.                                                | 24.05.2025     |
|                                | Login-Funktionalität repariert                                | ✅     | Behebung von Fehlern im Anmeldeprozess.                                               | 25.05.2025     |
|                                | Benutzer-Dashboard                                            | ✅     | Verwaltung persönlicher Daten und gespeicherter Inhalte.                               | 24.05.2025     |
|                                | JWT-Authentifizierung (Backend)                               | ✅     | Sichere API-Kommunikation.                                                            | 24.05.2025     |
|                                | Input-Validierung                                             | ✅     | Schutz vor ungültigen Eingaben.                                                       | 15.05.2025     |
| **Performance**                | Lazy-Loading für Bilder                                       | ✅     | Bilder werden erst bei Bedarf geladen.                                                | 28.05.2025     |
|                                | Core Web Vitals Optimierungen (LCP, FID, CLS)                 | ✅     | Verbesserte Ladezeiten und Nutzererfahrung.                                           | 28.05.2025     |
|                                | Integrierte Performance-Messung                               | ✅     | Überwachung der Web Vitals.                                                           | 28.05.2025     |

### Geplante Features & Verbesserungen

| Feature                               | Status | Beschreibung                                                                      | Geplant bis |
|---------------------------------------|--------|-----------------------------------------------------------------------------------|-------------|
| KI-Chatbot Integration                | 🚧 30% | Integration eines interaktiven Chatbots für Support und Informationsbeschaffung.    | 01.06.2025  |
| Erweiterte Filter im KI-Tools Verzeichnis | 📅     | Detailliertere Filteroptionen nach Anwendungsbereich, Preismodell etc.            | 10.06.2025  |
| Kommentarfunktion für Blogartikel     | ✅     | (Ursprünglich geplant, bereits umgesetzt am 23.05.2025)                           | --          |
| Personalisierte Content-Empfehlungen  | 📅     | Vorschläge basierend auf Nutzerverhalten und Interessen.                           | 15.07.2025  |
| Admin-Bereich Erweiterungen           | 🚧 10% | Umfassendere Verwaltungsfunktionen für Inhalte und Benutzer.                      | 30.07.2025  |
| Barrierefreiheit (WCAG AA)            | 📅     | Weitere Optimierungen zur Erreichung des WCAG AA Standards.                       | 30.06.2025  |
| Migration zu modernem Framework       | 📅     | Evaluierung und potenzielle Migration (z.B. Next.js) für bessere Performance/DX. | 30.06.2025  |

## 🛠️ Tech Stack

Die WelluxAI Plattform nutzt eine Kombination aus bewährten und modernen Technologien:

- **Frontend**:
  - HTML5, CSS3, JavaScript (ES6+)
  - `live-server` für die lokale Entwicklung statischer Seiten
  - Diverse JavaScript-Bibliotheken für UI-Komponenten und Interaktivität
- **Backend**:
  - Node.js (v20.x)
  - Express.js (als gängiges Node.js Framework)
  - MongoDB (v6.0+) als Datenbank
  - JWT (JSON Web Tokens) für Authentifizierung
- **Entwicklungstools & Umgebung**:
  - Git & GitHub für Versionskontrolle
  - npm (v10.x) für Paketmanagement
  - Visual Studio Code als empfohlene IDE
- **Deployment (Frontend)**:
  - Netlify (CI/CD konfiguriert)
  - Alternative Optionen: Vercel, GitHub Pages
- **Deployment (Backend)**:
  - Empfohlene Optionen: Railway, DigitalOcean App Platform, Heroku

## 📁 Projektstruktur

Die Codebasis ist in Frontend- und Backend-Komponenten unterteilt.

### Frontend (`/`)

Der Hauptordner enthält alle clientseitigen Dateien und Assets.

```text
/ (Root-Verzeichnis der Webseite)
├── index.html                  # Startseite (Landing Page)
├── about.html                  # Über Uns Seite
├── solutions.html              # KI-Lösungen Seite
├── consulting.html             # Digitalisierungsberatung Seite
├── blog.html                   # Blog-Übersichtsseite
├── contact.html                # Kontaktseite
├── css/                        # CSS-Stylesheets
│   ├── style.css               # Haupt-Stylesheet
│   └── responsive.css          # Styles für Responsive Design
├── js/                         # JavaScript-Dateien
│   ├── main.js                 # Haupt-Skript für allgemeine Interaktionen
│   └── auth.js                 # Skripte für Authentifizierung
├── assets/                     # Bilder, Icons und andere Medien
│   ├── images/
│   └── icons/
├── templates/                  # (Optional) HTML-Templates oder Partials
│   ├── header.html
│   └── footer.html
└── ...                         # Weitere HTML-Seiten und Ressourcen
```

### Backend (`/server`)

Der `/server`-Ordner beinhaltet die serverseitige Logik, API-Endpunkte und Datenbankintegration.

```text
/server
├── node_modules/             # NPM-Pakete
├── src/                      # Quellcode des Backends
│   ├── config/               # Konfigurationsdateien (DB, JWT etc.)
│   │   └── db.config.ts      # Datenbankverbindungseinstellungen
│   ├── controllers/          # API-Endpunkt-Controller (Logik für Requests)
│   ├── middleware/           # Express-Middleware (z.B. für Authentifizierung, Logging)
│   ├── models/               # Datenmodelle (z.B. Mongoose-Schemata für MongoDB)
│   ├── routes/               # API-Routen-Definitionen
│   ├── services/             # Geschäftslogik, Interaktion mit Datenbanken
│   └── types/                # TypeScript-Typdefinitionen (falls verwendet)
├── .env                      # Umgebungsvariablen (lokal, nicht versioniert)
├── .env.example              # Beispiel für Umgebungsvariablen
├── package.json              # Projektdefinition und Abhängigkeiten
├── tsconfig.json             # TypeScript-Konfiguration (falls verwendet)
└── server.js                 # Haupteinstiegspunkt der Backend-Anwendung
```

## 📄 Seitenstruktur und Inhalte

Die WelluxAI-Webseite ist darauf ausgelegt, Besuchern einen klaren und informativen Weg zu KI-Lösungen und Digitalisierungsberatung zu bieten.

### Landing Page (`index.html`)

- **Zweck**: Dient als zentraler Einstiegspunkt und Schaufenster von WelluxAI. Ziel ist es, die Kernkompetenzen prägnant zu kommunizieren und Besucher gezielt zu spezialisierten Informationen und interaktiven Tools wie dem ROI-Kalkulator, dem KI-Assessment, branchenspezifischen Lösungen und dem Blog zu führen.
- **Kern-Elemente (basierend auf `index.html` vom 25.05.2025)**:
  - **Hero Section**: Dynamische Hauptüberschrift "KI-Lösungen für kleine und mittelständische Unternehmen", unterstützender Text und primärer Call-to-Action (z.B. "Mehr erfahren" oder "Kostenloses Erstgespräch").
  - **"Warum WelluxAI?" Sektion**: Präsentation der Alleinstellungsmerkmale und Vorteile einer Zusammenarbeit.
  - **"Unsere Lösungen" Teaser**: Vorstellung der verschiedenen Lösungsbereiche (KMU, Enterprise, Startup, Handwerk) mit Verlinkung zur Übersichtsseite `loesungen.html`.
  - **ROI-Kalkulator Teaser**: Interaktives Element oder Verlinkung zum `roi-calculator.html` zur Berechnung potenzieller Einsparungen.
  - **KI-Assessment Teaser**: Hinweis und Link zum `assessment.html` zur Selbsteinschätzung der KI-Reife.
  - **Erfolgsgeschichten Teaser**: Anreißer ausgewählter Kundenprojekte mit Link zu `erfolgsgeschichten.html`.
  - **Aktuelles aus dem Blog Teaser**: Anzeige der neuesten Blogartikel mit Link zu `blog.html`.
  - **Haupt-Call-to-Action**: Prominenter Button, z.B. "Kostenloses Erstgespräch vereinbaren", der zu `termin.html` oder `kontakt.html` führt.
  - **Newsletter-Anmeldung**: Formular zur Aufnahme in den E-Mail-Verteiler (oft im Footer integriert).
  - **Footer**: Enthält Standardinformationen wie Copyright, Links zu Impressum, Datenschutz und Social Media.
- **Wireframe-Logik**: Die Seite ist so strukturiert, dass sie den Nutzer von einer allgemeinen Einführung in die Thematik ("Warum WelluxAI?") über spezifische Lösungsansätze und interaktive Tools (ROI-Kalkulator, KI-Assessment) bis hin zu konkreten Erfolgsbeispielen und direkten Kontaktmöglichkeiten führt. Jeder Abschnitt dient dazu, Vertrauen aufzubauen und den Mehrwert der WelluxAI-Angebote zu demonstrieren, kulminierend in klaren Handlungsaufforderungen.

### Weitere wichtige Seiten

- **`assessment.html`**: Interaktives KI-Readiness Assessment zur Einschätzung der KI-Reife von Unternehmen.
- **`blog.html`**: Blog-Übersichtsseite mit Fachartikeln, Neuigkeiten und Fallstudien rund um KI und Digitalisierung.
- **`dashboard.html`**: Persönlicher Bereich für registrierte Benutzer zur Verwaltung von Daten und Einstellungen.
- **`demo.html`**: Seite zur Präsentation von Demo-Versionen oder zur Vereinbarung von Demo-Terminen.
- **`enterprise.html`**: Spezifische KI-Lösungen und Beratungsangebote für Großunternehmen.
- **`erfolgsgeschichten.html`**: Sammlung von Case Studies und Erfolgsbeispielen von Kundenprojekten.
- **`handwerk.html`**: Maßgeschneiderte KI-Lösungen und Digitalisierungsstrategien für Handwerksbetriebe.
- **`kmu.html`**: KI-Lösungen und Beratungsangebote, zugeschnitten auf die Bedürfnisse kleiner und mittlerer Unternehmen.
- **`kontakt.html`**: Kontaktformular, Adressdaten und weitere Möglichkeiten zur Kontaktaufnahme.
- **`loesungen.html`**: Detaillierte Übersicht über das gesamte Lösungsportfolio von WelluxAI.
- **`login.html`**: Anmeldeseite für Benutzerkonten.
- **`prompts.html`**: Sammlung oder Informationen zu effektiven Prompts für verschiedene KI-Anwendungen (Prompt Engineering).
- **`referenzen.html`**: Übersicht über Referenzkunden und Partner.
- **`roi-calculator.html`**: Interaktiver Rechner zur Abschätzung des Return on Investment von KI-Projekten.
- **`startup.html`**: KI-Lösungen und Unterstützungsprogramme speziell für Startups.
- **`termin.html`**: Seite zur einfachen Online-Terminvereinbarung für Beratungsgespräche.
- **`tools.html`**: Verzeichnis und Beschreibung der von WelluxAI angebotenen oder empfohlenen KI-Tools.
    *(Hinweis: `about.html`, `consulting.html`, `imprint.html`, `privacy.html` und `resources.html` waren im vorherigen Stand genannt, aber nicht in der aktuellen Dateiliste vom 25.05.2025. Falls diese existieren oder geplant sind, sollten sie ergänzt werden.)*

### Navigationsstruktur (Burger-Menü)

- **Ziel**: Eine klare, intuitive und responsive Navigation, die Nutzern schnellen Zugriff auf alle relevanten Bereiche der WelluxAI-Plattform bietet. Das Burger-Menü passt sich an, je nachdem, ob ein Benutzer angemeldet ist oder nicht.

- **Ansicht für nicht angemeldete Benutzer (Öffentlich):**
  - Startseite (`index.html`)
  - Lösungen (`loesungen.html`)
    - Für KMU (`kmu.html`)
    - Für Enterprise (`enterprise.html`)
    - Für Startups (`startup.html`)
    - Für Handwerk (`handwerk.html`)
  - Tools & Ressourcen
    - KI-Tools Verzeichnis (`tools.html`)
    - ROI-Kalkulator (`roi-calculator.html`)
    - KI-Assessment (`assessment.html`)
    - Prompt-Bibliothek (`prompts.html`)
  - Erfolgsgeschichten (`erfolgsgeschichten.html`)
  - Blog (`blog.html`)
  - Kontakt (`kontakt.html`)
  - Login (`login.html`)

- **Ansicht für angemeldete Benutzer (Authentifiziert):**
  - Startseite (`index.html`)
  - Lösungen (`loesungen.html`)
    - Für KMU (`kmu.html`)
    - Für Enterprise (`enterprise.html`)
    - Für Startups (`startup.html`)
    - Für Handwerk (`handwerk.html`)
  - Tools & Ressourcen
    - KI-Tools Verzeichnis (`tools.html`)
    - ROI-Kalkulator (`roi-calculator.html`)
    - KI-Assessment (`assessment.html`)
    - Prompt-Bibliothek (`prompts.html`)
  - Erfolgsgeschichten (`erfolgsgeschichten.html`)
  - Blog (`blog.html`)
  - **Mein Dashboard (`dashboard.html`)**
  - Kontakt (`kontakt.html`)
  - **Logout** (Funktion, kein direkter Seitenlink)

> *Hinweis:* Diese Struktur ist ein Vorschlag basierend auf den vorhandenen Seiten und gängigen Praktiken. Die tatsächliche Implementierung kann abweichen und sollte bei Bedarf hier aktualisiert werden.

## ⚙️ Konfiguration

### Umgebungsvariablen (`/server/.env`)

Die Backend-Anwendung wird über Umgebungsvariablen konfiguriert. Eine `.env.example`-Datei im `/server`-Verzeichnis dient als Vorlage. Kopieren Sie diese zu `.env` und passen Sie die Werte an Ihre lokale Umgebung an.

Wichtige Variablen:

- `NODE_ENV`: Umgebung (z.B. `development`, `production`)
- `PORT`: Server-Port für das Backend (default: `3001`)
- `MONGO_URI`: Verbindungsstring für die MongoDB-Datenbank.
- `JWT_SECRET`: Geheimer Schlüssel für die Generierung und Verifizierung von JSON Web Tokens.
- `CORS_ORIGIN`: Erlaubte Ursprünge für Cross-Origin Resource Sharing (wichtig für die Kommunikation zwischen Frontend und Backend).
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`: Für die Google OAuth 2.0 Authentifizierung.

## 🚀 Deployment

Dieser Abschnitt beschreibt die Schritte und Optionen für das Deployment des Frontends und Backends.

### Frontend Deployment

Das Frontend besteht aus statischen Dateien und kann auf verschiedenen Plattformen gehostet werden.

```bash
# Build-Prozess (falls vorhanden, z.B. für Optimierungen oder bei Einsatz eines Frameworks)
# npm run build 
```

**Empfohlene Hosting-Optionen:**

- **Netlify**: (Bereits konfiguriert)
  - Automatisches Deployment bei Push zu `main`.
  - Netlify Forms für Kontaktformular integriert.
  - Netlify Functions für serverless API-Endpunkte (falls benötigt).
- **Vercel**: Alternative für schnelles Frontend-Hosting, unterstützt Edge-Funktionen.
- **GitHub Pages**: Kostenloses Hosting für statische Inhalte direkt aus dem Repository.

### Backend Deployment

Das Node.js-Backend muss auf einer Plattform gehostet werden, die serverseitige Anwendungen unterstützt.

```bash
# Build für Produktion (falls TypeScript oder Build-Schritte nötig)
# cd server
# npm run build

# Starten in Produktionsumgebung (typischerweise über einen Prozessmanager wie PM2)
# npm start 
```

**Empfohlene Hosting-Optionen:**

- **Railway**: PaaS mit einfacher CI/CD-Integration und automatischem Scaling.
- **DigitalOcean App Platform**: Managed Hosting mit Auto-Deploys und integriertem Monitoring.
- **Heroku**: Beliebte PaaS-Lösung mit einfacher Skalierung und Management.

Stellen Sie sicher, dass alle notwendigen Umgebungsvariablen auf der Hosting-Plattform konfiguriert sind.

## 📊 Projekt-Status (Stand: 25.05.2025)

- **Fortschritt**: ca. 90% (Kernfunktionalitäten implementiert, UI/UX-Verbesserungen weitgehend abgeschlossen)
- **Nächster Meilenstein**: "Phase 5: Erweiterte Features" - insbesondere "KI-Chat Integration" (Deadline: 01.06.2025)
- **Aktuelle Blocker**: Keine kritischen Blocker. Fokus liegt auf der Fertigstellung der verbleibenden Features aus Phase 5 und der Vorbereitung für Phase 6 (Testing & Launch).

## 🔄 Letzte Änderungen

- 2025-05-25: `sitemap.xml` aktualisiert, um die aktuelle Seitenstruktur gemäß README.md widerzuspiegeln.
- 2025-05-25: Diverse Linting-Fehler in `README.md` behoben (MD036, MD012, MD032).
*(Für Details siehe Git Commit History)*

## 🤝 Contributing

Derzeit sind keine externen Beiträge vorgesehen. Bei Interesse an einer Mitarbeit kontaktieren Sie bitte WelluxAI direkt.

## 👤 Autor

### Marco Mengele

- Geschäftsführer Wellux
- Meister SHK & Energieberater

## 📄 Lizenz

Alle Rechte vorbehalten - Wellux 2025
