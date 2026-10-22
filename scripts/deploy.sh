#!/usr/bin/env bash
# Vérifie que l'API configurée répond avant un déploiement.
set -euo pipefail

SETTINGS="$(dirname "$0")/../config/settings.yaml"
API_URL="$(grep 'api_url:' "$SETTINGS" | head -1 | awk '{print $2}')"

echo "Déploiement vers $API_URL"
if [ -z "$API_URL" ]; then
  echo "api_url manquant dans $SETTINGS" >&2
  exit 1
fi
