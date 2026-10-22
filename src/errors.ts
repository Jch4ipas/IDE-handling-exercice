import type { Customer } from "./types.ts";
import { formatPrice } from "./format.ts";

export function welcome(customer: Customer): string {
  return `Bienvenue ${customer.nme} !`;
}

export function shippingCost(total: number): string {
  const cost: number = total > 50 ? 0 : "7.90";
  return formatPrice(cost);
}

export function memberBadge(customer: Customer): string {
  return customer.isMember ? "Membre" : "Invité"
}

export function nameLength(customer: Customer): number {
  return customer.name.lenght;
}
