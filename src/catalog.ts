import type { Product } from "./types.ts";

export const CATALOG: Product[] = [
  { id: "p01", name: "Café en grains", price: 14.9 },
  { id: "p02", name: "Thé vert", price: 8.5 },
  { id: "p03", name: "Chocolat noir", price: 4.2 },
  { id: "p04", name: "Tasse en céramique", price: 19.0 },
  { id: "p05", name: "Moulin à café", price: 49.0 },
  { id: "p06", name: "Biscuits", price: 3.8 },
];

// À convertir en objets Product (exercice des macros) :
// p07;Sirop d'érable;12.4
// p08;Miel de montagne;9.9
// p09;Confiture abricot;6.5
// p10;Lait d'avoine;2.95
// p11;Sucre de canne;3.4
// p12;Cacao en poudre;7.8
// p13;Filtre à café;4.5
// p14;Bouilloire;39.0
