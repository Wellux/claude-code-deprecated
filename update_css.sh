#!/bin/bash

# Dieses Skript fügt die contrast-fixes.css zu allen HTML-Dateien hinzu, falls sie noch nicht enthalten ist

for html_file in *.html; do
  # Überprüfen, ob die Datei bereits contrast-fixes.css enthält
  if ! grep -q "contrast-fixes.css" "$html_file"; then
    echo "Aktualisiere $html_file..."
    
    # Finde die letzte CSS-Einbindung vor der Font-Awesome CSS und füge contrast-fixes.css danach ein
    sed -i '' 's#<link rel="stylesheet" href="css/language-switcher.css">#<link rel="stylesheet" href="css/language-switcher.css">\n    <link rel="stylesheet" href="css/contrast-fixes.css">#' "$html_file"
    
    echo "✅ $html_file aktualisiert"
  else
    echo "⏭️ $html_file bereits aktualisiert, überspringe..."
  fi
done

echo "🎉 Alle HTML-Dateien wurden aktualisiert!"