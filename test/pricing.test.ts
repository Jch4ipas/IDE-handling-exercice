import { test } from "node:test";
import assert from "node:assert/strict";
import { applyDiscount, calcSubtotal, calcTotal } from "../src/pricing.ts";
import type { CartItem } from "../src/types.ts";

const items: CartItem[] = [
  { id: "a", name: "A", price: 10, quantity: 2 },
  { id: "b", name: "B", price: 5, quantity: 1 },
];

test("le sous-total additionne prix x quantité", () => {
  assert.equal(calcSubtotal(items), 25);
});

test("une réduction de 10 % retire 10 % du montant", () => {
  assert.equal(applyDiscount(100, 10), 90);
});

test("le total ajoute la TVA et arrondit aux 5 centimes", () => {
  assert.equal(calcTotal(items), 27.05);
});
