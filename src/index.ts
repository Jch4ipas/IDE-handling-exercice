import { Cart } from "./cart.ts";
import { calcTotal } from "./pricing.ts";
import { formatPrice, formatQuantity } from "./format.ts";
import { CATALOG } from "./catalog.ts";

const alice = { name: "Alice", email: "alice@example.ch", isMember: true };
const cart = new Cart(alice);

cart.add(CATALOG[0], 2);
cart.add(CATALOG[3]);
cart.add(CATALOG[5], 3);

console.log(`Panier de ${alice.name} : ${formatQuantity(cart.count())}`);
console.log(`Total : ${formatPrice(cart.total())}`);

// Prix d'un panier "invité" (sans réduction), calculé directement
const guestTotal = calcTotal([{ ...CATALOG[1], quantity: 1 }]);
console.log(`Total invité : ${formatPrice(guestTotal)}`);
