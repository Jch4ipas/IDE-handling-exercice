// Petites fonctions de texte (exercices 1.1 et 1.2)

export const VERSION = "0.9";
export const SUPPORT_EMAIL = "aide@petite-boutique.ch";

export function capitalize(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1);
}
