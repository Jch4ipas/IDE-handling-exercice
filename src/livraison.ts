// Livraison : le fichier du chapitre 2 (se déplacer sans souris)

// ===== 2.1 : les lignes =====
const BASE_FEE = 7.9
const EXPRESS_FEE = 14.5
const FREE_FROM = 50
// à supprimer : ancien tarif 6.9
function standardFee(total: number): number {
  return total >= FREE_FROM ? 0 : BASE_FEE
}
// à supprimer : ancien seuil 40
function expressFee(): number {
  return EXPRESS_FEE
}

// ===== 2.2 : les mots =====
export const LABEL_STANDARD = "Livraison standard très rapide";
export const LABEL_EXPRESS = "Livraison express en en 24h";

export function fee(zone: string, poids: number, express: boolean): number {
  return express ? expressFee() : standardFee(zone.length);
}

// ===== 2.3 : les blocs et les fonctions =====
export function second(): string {
  return "je dois être la 2e fonction";
}

export function first(): string {
  return "je dois être la 1re fonction";
}

export function logFee(): void {
  console.log("frais", { debug: true, niveau: 3 });
}

// ===== 2.5 : sauter à l'écran =====
export const VILLES = {
  argovie: "Aarau",
  berne: "Berne",
  fribourg: "Fribour",
  geneve: "Geneve",
  jura: "Delemon",
  lucerne: "Lucerne",
  neuchatel: "Neuchatl",
  soleure: "Soleure",
  tessin: "Bellinzone",
  valais: "Sion",
  vaud: "Lausane",
  zurich: "Zurich",
};
