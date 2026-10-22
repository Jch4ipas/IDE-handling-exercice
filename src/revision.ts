// Révision 5 : édition et refactoring

export const COULEURS = [
  "rouge",
  "vert",
  "bleu",
  "jaune",
];

export function prix(article: string): number {
  return article.length;
}

export const PRIX_CAFE = prix("café");
export const PRIX_THE = prix("thé");
