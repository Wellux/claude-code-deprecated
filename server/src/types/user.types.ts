/**
 * User-bezogene Typdefinitionen
 * Gemäß unseren Projektrichtlinien: TypeScript strict mode und klare Typdefinitionen
 */

// Basis-Benutzertyp
export interface User {
  id: string;
  name: string;
  email: string;
  password: string;
  created: string;
  preferences?: UserPreferences;
}

// Benutzereinstellungen
export interface UserPreferences {
  theme: 'light' | 'dark';
  language: 'de' | 'en';
}

// DTO für die Benutzerregistrierung
export interface UserRegistrationDto {
  name: string;
  email: string;
  password: string;
}

// DTO für den Login
export interface UserLoginDto {
  email: string;
  password: string;
}

// Sichere Benutzerinformationen (ohne Passwort) für Antworten
export interface SafeUserInfo {
  id: string;
  name: string;
  email: string;
}

// Login-Antwort mit Token
export interface LoginResponse {
  token: string;
  user: SafeUserInfo;
}
