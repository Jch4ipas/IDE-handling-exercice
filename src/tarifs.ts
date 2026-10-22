// Tarifs de livraison par canton (exercices 2.4, 2.6 et révision 2)

export const WEEKEND_SURCHARGE = 4.5; // supplément du samedi
export const HOLIDAY_SURCHARGE = 6;

export function tarifArgovie(): number {
  return 11;
}

export function tarifBerne(): number {
  return 10;
}

export function tarifFribourg(): number {
  return 9;
}

export function tarifGeneve(): number {
  return 14;
}

export function tarifJura(): number {
  return 8;
}

export function tarifLucerne(): number {
  return 10;
}

// Montant minimum d'une commande (exercice 2.4 : mets 20)
export const MINIMUM_ORDER = 0;

export function tarifNeuchatel(): number {
  return 9;
}

export function tarifSoleure(): number {
  return 9;
}

export function tarifValais(): number {
  return 10;
}

export function tarifVaud(): number {
  return 12;
}

export function tarifZoug(): number {
  return 13;
}

export function tarifZurich(): number {
  return 13;
}

// Tessin : ancien tarif, cette fonction doit être la première de la liste
export function tarifTessin(): number {
  return 13
}

export function weekendTotal(base: number): number {
  // Remplace 0 par la valeur de WEEKEND_SURCHARGE (le nombre, pas le nom)
  return base + 0;
}
