"""Génère un rapport des ventes à partir d'une liste de commandes."""

from pathlib import Path

SETTINGS_FILE = Path(__file__).parent.parent / "config" / "settings.yaml"


def read_setting(key):
    """Lit une valeur simple `key: valeur` dans settings.yaml."""
    for line in SETTINGS_FILE.read_text(encoding="utf-8").splitlines():
        name, _, value = line.strip().partition(":")
        if name == key:
            return value.strip()
    raise KeyError(key)


def compute_revenue(orders):
    total = 0
    for o in orders:
        total = total + o["price"] * o["quantity"]
    return total


def best_seller(orders):
    counts = {}
    for o in orders:
        counts[o["name"]] = counts.get(o["name"], 0) + o["quantity"]
    return max(counts, key=counts.get)


def build_report(orders):
    revenue = compute_revenue(orders)
    lines = [
        f"Boutique : {read_setting('name')}",
        f"API : {read_setting('api_url')}",
        f"Chiffre d'affaires : {revenue:.2f} CHF",
        f"Meilleure vente : {best_seller(orders)}",
    ]
    print("debug: rapport construit")
    print("debug: %d commandes" % len(orders))
    print("debug: total=%s" % revenue)
    return "\n".join(lines)


if __name__ == "__main__":
    demo = [
        {"name": "Café en grains", "price": 14.9, "quantity": 3},
        {"name": "Thé vert", "price": 8.5, "quantity": 1},
        {"name": "Café en grains", "price": 14.9, "quantity": 2},
    ]
    print(build_report(demo))
