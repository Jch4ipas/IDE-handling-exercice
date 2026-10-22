import type { CartItem, Customer } from "./types.ts";
import { formatPrice } from "./format.ts";
import { calcSubtotal, TAX_RATE } from "./pricing.ts";

export function buildInvoice(customer: Customer, items: CartItem[]): string {
  const lines: string[] = [];
  lines.push(`Facture pour ${customer.name} <${customer.email}>`);
  lines.push("-".repeat(40));

  for (const item of items) {
    lines.push(`${item.name.padEnd(25)} ${String(item.quantity).padStart(3)}  ${formatPrice(item.price * item.quantity)}`);
  }

  // --- début du bloc à extraire dans une fonction ---
  const subtotal = calcSubtotal(items);
  const tax = subtotal * TAX_RATE;
  const total = subtotal + tax;
  lines.push("-".repeat(40));
  lines.push(`Sous-total : ${formatPrice(subtotal)}`);
  lines.push(`TVA (8.1%) : ${formatPrice(tax)}`);
  lines.push(`Total      : ${formatPrice(total)}`);
  // --- fin du bloc à extraire ---

  return lines.join("\n");
}
