import { test } from "node:test";
import assert from "node:assert/strict";
import { Cart } from "../src/cart.ts";

const bob = { name: "Bob", email: "bob@example.ch", isMember: false };

test("ajouter deux fois le même produit cumule la quantité", () => {
  const cart = new Cart(bob);
  cart.add({ id: "x", name: "X", price: 2 }, 1);
  cart.add({ id: "x", name: "X", price: 2 }, 2);
  assert.equal(cart.count(), 3);
});

test("retirer un produit le supprime du panier", () => {
  const cart = new Cart(bob);
  cart.add({ id: "x", name: "X", price: 2 });
  cart.remove("x");
  assert.equal(cart.count(), 0);
});
