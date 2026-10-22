export function roundPrice(amount: number): number {
  return Math.round(amount * 20) / 20; // arrondi aux 5 centimes
}

export function formatPrice(amount: number): string {
  return `CHF ${roundPrice(amount).toFixed(2)}`;
}

export function formatQuantity(quantity: number): string {
  return quantity === 1 ? "1 article" : `${quantity} articles`;
}
