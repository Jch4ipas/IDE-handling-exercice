import { roundPrice } from "./format.ts";
import { MEMBER_DISCOUNT } from "./pricing.ts";
import type { CartItem } from "./types.ts";
import { formatQuantity } from "./format.ts";

// Exercice 4.7 : formate ce fichier et range ses imports.
export function summary(items: CartItem[]): string {
        const count = items.length;
  if (count === 0) {
            return "panier vide";
      }
 return formatQuantity(count);
}
