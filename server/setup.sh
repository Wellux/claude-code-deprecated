#!/bin/bash

# WelluxAI Backend Setup Script
echo "🚀 WelluxAI Backend Setup wird gestartet..."

# 1. Node-Module installieren
echo "📦 Installiere Node-Module..."
npm install

# 2. TypeScript-Typdefinitionen installieren
echo "🔍 Installiere TypeScript-Typdefinitionen..."
npm install --save-dev @types/node @types/express @types/cors @types/helmet @types/morgan @types/cookie-parser @types/bcrypt @types/jsonwebtoken @types/express-rate-limit

# 3. .env Datei erstellen, falls nicht vorhanden
if [ ! -f .env ]; then
  echo "🔐 Erstelle .env Datei..."
  cp .env.example .env
  echo "⚠️ Bitte passe die Werte in der .env Datei an deine Umgebung an."
fi

# 4. TypeScript kompilieren
echo "🔨 Kompiliere TypeScript..."
npm run build

echo "✅ Setup abgeschlossen!"
echo "🌐 Starte den Server mit 'npm run dev' für die Entwicklung oder 'npm start' für die Produktion."
