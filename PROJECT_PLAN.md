# Project Plan - WelluxAI

## Status: 🟢 ON_TRACK

**Aktualisiert**: 25.05.2025 22:45

## Meilensteine

- [x] Phase 1: Grundstruktur (Fertig: 05.05.2025)
- [x] Phase 2: KI-Tools Integration (Fertig: 15.05.2025)
- [x] Phase 3: Content & Blog (Fertig: 20.05.2025)
- [x] Phase 4: Mehrsprachigkeit & UX (Fertig: 22.05.2025)
- [ ] Phase 5: Erweiterte Features (Deadline: 01.06.2025)
  - [x] Kommentarsystem für Blog (Fertig: 23.05.2025)
  - [x] Benutzerkonto & OAuth (Fertig: 24.05.2025)
  - [ ] KI-Chat Integration (30% fertig)
- [ ] Phase 6: Testing & Launch (Deadline: 15.06.2025)
- [ ] **NEU - Phase 7: Technische Schulden & Optimierung** (Deadline: 30.06.2025)
  - [ ] Migration zu modernem Framework (React/Next.js)
  - [x] Sicherheitsoptimierung mit JWT-Backend (Fertig: 24.05.2025)
  - [ ] Performance-Verbesserung (Initiale Optimierungen implementiert am 28.05.2025, weitere geplant)
  - [ ] Barrierefreiheit (WCAG AA)
  - [x] README.md Überarbeitung & Linting-Fix (Fertig: 25.05.2025)
  - [x] README.md: Detaillierte Seitenstruktur und Inhalte hinzugefügt (Landingpage, Wireframe, etc.) (Fertig: 28.05.2025)
  - [x] sitemap.xml aktualisiert und an README.md Seitenstruktur angepasst (Fertig: 25.05.2025)

## Sprint 10 (22.05.2025 - 28.05.2025) - Abgeschlossen

- **Velocity**: 30 Story Points
- **Abgeschlossen**:
  - OAuth-Integration für Benutzerkonten (Google)
  - Benutzer-Dashboard für gespeicherte Inhalte
  - Verbessertes Mobile-Menü
  - Design- und Kontrast-Probleme behoben (Accessibility)
  - Unterseiten-Design vereinheitlicht und optimiert
  - Login-Funktionalität repariert (25.05.2025)
  - Blog und KI-Tools Directory für Dark & Light Mode optimiert (26.05.2025)
  - Design der Überschriften modernisiert (26.05.2025)
  - Lesbarkeit in beiden Themes verbessert (26.05.2025)
  - Navigation mit Dropdown-Menüs optimiert (27.05.2025)
  - Landingpage verschlankt und Inhalte auf Unterseiten ausgelagert (27.05.2025)
  - CSS für Dropdown-Navigation implementiert (28.05.2025)
  - Standardisierte Header- und Footer-Einbindung auf allen Seiten implementiert (28.05.2025)
  - Header- und Footer-Standardisierung auf 100% der Seiten abgeschlossen (28.05.2025)
  - Performance-Optimierung implementiert (Lazy-Loading, Core Web Vitals, Font-Loading) (28.05.2025)
  - README.md vollständig überarbeitet und neu strukturiert (28.05.2025)
  - README.md: Seitenstruktur und Inhalte (Landingpage, Wireframe) detailliert (28.05.2025)
- **In Arbeit**: -
- **Blocker**: -

## Sprint 11 (29.05.2025 - 05.06.2025) - Geplant

- **Ziele**:
    - Finalisierung KI-Chat Integration
    - Vorbereitung Phase 6: Testing-Plan erstellen
- **Geplante Tasks**:
    - [ ] Task: KI-Chatbot UI-Integration abschließen
    - [ ] Task: KI-Chatbot Backend-Anbindung finalisieren
    - [ ] Task: Testfälle für Kernfunktionalitäten definieren
- **Velocity Ziel**: X Story Points
- **Blocker**: (Noch keine bekannt)


## Nächste Schritte

1.  **Finalisierung KI-Chat Integration** (Ziel: 01.06.2025)
2.  **Beginn Phase 6: Testing & Launch** (ab 02.06.2025)
    -   Umfassende Tests aller Funktionalitäten
    -   Erstellung von Testprotokollen
    -   Vorbereitung der Launch-Checkliste
3.  **Weitere Optimierungen Phase 7** (Performance, Barrierefreiheit, ggf. Framework-Migration)

## Coding Standards & Best Practices (Auszug)

### TypeScript-Richtlinien

```typescript
// ✅ RICHTIG: Strikte Typisierung und Zod für Validierung
import { z } from "zod";

interface UserData {
  id: string;
  email: string;
  preferences?: {
    theme: "light" | "dark";
    notifications: boolean;
  };
}

const userSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  preferences: z
    .object({
      theme: z.enum(["light", "dark"]),
      notifications: z.boolean(),
    })
    .optional(),
});

const validateUser = (data: unknown): UserData => {
  return userSchema.parse(data);
};
```

### CSS-Richtlinien

```css
/* ✅ RICHTIG: Komponentenbasierter Ansatz mit CSS-Variablen */
.button {
  /* Basisstil für alle Buttons */
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  font-weight: var(--font-weight-medium);
  transition: all 0.3s ease;
}

.button--primary {
  background-color: var(--color-primary);
  color: var(--color-white);
}

.button--secondary {
  background-color: var(--color-secondary);
  color: var(--color-white);
}

/* Accessibility-Verbesserungen */
.button:focus {
  outline: 3px solid var(--color-focus);
  outline-offset: 2px;
}
```

### API-Design-Richtlinien

```typescript
// RESTful Endpoints
// app.get("/api/v1/users", getUsersList); // Liste aller Benutzer
// app.get("/api/v1/users/:id", getUserById); // Einzelner Benutzer
// app.post("/api/v1/users", createUser); // Neuen Benutzer anlegen
// app.put("/api/v1/users/:id", updateUser); // Benutzer aktualisieren
// app.delete("/api/v1/users/:id", deleteUser); // Benutzer löschen

// Standardisierte Antwortstruktur
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
  };
}

// Beispiel für eine erfolgreiche Antwort
// const successResponse: ApiResponse<User> = {
//   success: true,
//   data: user,
//   meta: {
//     // Weitere Metadaten bei Bedarf
//   },
// };

// Beispiel für eine Fehlerantwort
// const errorResponse: ApiResponse<never> = {
//   success: false,
//   error: {
//     code: "USER_NOT_FOUND",
//     message: "Der angeforderte Benutzer wurde nicht gefunden",
//     details: { userId: "123" },
//   },
// };
```

## Gesamtfortschritt: ca. 90%

(Kernfunktionalitäten implementiert, UI/UX-Verbesserungen und Dokumentation weitgehend abgeschlossen. Nächste Schritte: KI-Chat Integration, umfassendes Testing und Launch-Vorbereitung.)
