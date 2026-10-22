// Client de l'API de la boutique (exercices 1.1, 1.2 et révision 1)

export const VERSION = "0.9";
export const TIMEOUT = 10;
export const RETRIES = 3;

// Adresse de contact envoyée avec chaque requête
export const CONTACT = "à remplir";

export function headers(): Record<string, string> {
  return { "User-Agent": `petite-boutique/${VERSION}`, From: CONTACT };
}
