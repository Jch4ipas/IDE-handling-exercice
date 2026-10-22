import type { CartItem, Customer } from "./types.ts";
import { roundPrice } from "./format.ts";

export const TAX_RATE = 0.081; // TVA suisse
export const MEMBER_DISCOUNT = 10; // en pourcent

export function calcSubtotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

export function applyDiscount(amount: number, percent: number): number {
  return amount - amount * percent;
}

export function discountFor(customer: Customer): number {
  return customer.isMember ? MEMBER_DISCOUNT : 0;
}

export function calcTotal(items: CartItem[], discountPercent = 0): number {
  const subtotal = calcSubtotal(items);
  const discounted = applyDiscount(subtotal, discountPercent);
  return roundPrice(discounted * (1 + TAX_RATE));
}
