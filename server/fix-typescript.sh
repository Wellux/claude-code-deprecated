#!/bin/bash

# TypeScript-Fehler Behebungsskript
echo "🔍 Installiere fehlende Typdeklarationen für das Projekt..."

# Installiere alle benötigten @types Pakete
npm install --save-dev \
  @types/node \
  @types/express \
  @types/cors \
  @types/helmet \
  @types/morgan \
  @types/cookie-parser \
  @types/jsonwebtoken \
  @types/bcrypt \
  @types/express-rate-limit

echo "✅ Typdeklarationen wurden installiert."
echo "🚀 Jetzt TSC ausführen, um zu prüfen, ob alle Fehler behoben sind:"
echo "   npx tsc --noEmit"
