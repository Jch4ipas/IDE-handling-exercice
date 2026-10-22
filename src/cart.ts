import type { CartItem, Customer, Product } from "./types.ts";
import { calcTotal, discountFor } from "./pricing.ts";

export class Cart {
  private items: CartItem[] = [];
  private customer: Customer;

  constructor(customer: Customer) {
    this.customer = customer;
  }

  add(product: Product, quantity = 1): void {
    const existing = this.items.find((item) => item.id === product.id);
    if (existing) {
      existing.quantity += quantity;
    } else {
      this.items.push({ ...product, quantity });
    }
  }

  remove(productId: string): void {
    this.items = this.items.filter((item) => item.id !== productId);
  }

  count(): number {
    return this.items.reduce((sum, item) => sum + item.quantity, 0);
  }

  total(): number {
    return calcTotal(this.items, discountFor(this.customer));
  }
}
