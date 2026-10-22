import type { CartItem } from "./types.ts";

export function receiptLine(item: CartItem): string {
  return `${item.name} x${item.quantity} : ${formatPrice(item.price * item.quantity)}`;
}
