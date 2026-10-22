import type { Customer } from "./types.ts";
import { formatPrice } from "./format.ts";

export function welcome(customer: Customer): string {
  return `Bienvenue ${customer.nmae} !`;
}

export function shippingCost(total: number): string {
  const cost: number = total > 50 ? 0 : "7.90";
  return formatPrice(cost);
}

export function memberBadge(customer: Customer): string {
  return customer.isMember ? "Membre" : "Invité"
}

export function initials(customer: Customer): string {
  return customer.name.split(" ").map((part) => part[0]).joim("");
}
