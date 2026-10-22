#!/usr/bin/env python3
"""Vérifie les exercices de EXERCICES.org.

  python3 verifier.py           vérifie tous les exercices
  python3 verifier.py 3.1       vérifie un exercice
  python3 verifier.py --reset 3.1   remet les fichiers de l'exercice à zéro
  python3 verifier.py --reset   remet tout le projet à zéro (sauf EXERCICES.org)

Depuis Emacs : C-x p c (compile dans le projet), puis tape la commande.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
START = "depart"  # tag git de l'état initial


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def run(*cmd, cwd=ROOT):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def grep(word, *dirs):
    """Fichiers (hors node_modules) qui contiennent WORD."""
    found = []
    for d in dirs:
        for f in (ROOT / d).rglob("*"):
            if f.is_file() and "node_modules" not in f.parts and "__pycache__" not in f.parts:
                if word in f.read_text(encoding="utf-8", errors="ignore"):
                    found.append(str(f.relative_to(ROOT)))
    return found


def tsc_errors(file=None):
    """Erreurs TypeScript du projet (ou d'un seul fichier)."""
    tsc = shutil.which("tsc")
    if not tsc:
        return ["tsc introuvable (npm install -g typescript)"]
    out = run(tsc).stdout.splitlines()
    errors = [l for l in out if "error TS" in l]
    return [e for e in errors if file is None or e.startswith(file)]


def py_tests_ok():
    return run(sys.executable, "-m", "unittest", "-q", cwd=ROOT / "scripts").returncode == 0


# Chaque vérification renvoie une liste de problèmes (vide = réussi).

def check_4_1():
    problems = []
    if left := grep("calcTotal", "src", "test"):
        problems.append(f"'calcTotal' existe encore dans : {', '.join(left)}")
    for f in ["src/pricing.ts", "src/cart.ts", "src/index.ts", "test/pricing.test.ts"]:
        if "computeCartTotal" not in read(f):
            problems.append(f"'computeCartTotal' manque dans {f}")
    if errs := [e for e in tsc_errors() if "computeCartTotal" in e or "calcTotal" in e]:
        problems += errs
    return problems


def check_4_2():
    problems = []
    if left := grep("api_url", "config", "scripts"):
        problems.append(f"'api_url' existe encore dans : {', '.join(left)}")
    for f in ["config/settings.yaml", "scripts/report.py", "scripts/test_report.py", "scripts/deploy.sh"]:
        if "base_url" not in read(f):
            problems.append(f"'base_url' manque dans {f}")
    if not py_tests_ok():
        problems.append("les tests Python échouent (cd scripts && python3 -m unittest)")
    return problems


def check_4_3():
    s = read("scripts/report.py")
    problems = []
    if 'print("debug' in s:
        problems.append('il reste des print("debug: ...")')
    if s.count("logging.debug(") != 3:
        problems.append("il faut exactement 3 logging.debug(...)")
    if not re.search(r"^import logging$", s, re.M):
        problems.append("il manque la ligne 'import logging'")
    if not py_tests_ok():
        problems.append("les tests Python échouent")
    return problems


def check_4_4():
    s = read("src/notes.ts")
    problems = []
    if re.search(r"\d+h-\d+h", s):
        problems.append("il reste des horaires au format 9h-18h")
    expected = ['"9:00-18:00"'] * 4 + ['"9:00-20:00"', '"9:00-16:00"']
    for e in set(expected):
        if s.count(e) != expected.count(e):
            problems.append(f"on attend {expected.count(e)} fois {e}")
    return problems


def check_4_5():
    problems = []
    if errs := tsc_errors("src/missing-import.ts"):
        problems += errs
    if not re.search(r'import \{[^}]*formatPrice[^}]*\} from "\./format\.ts"', read("src/missing-import.ts")):
        problems.append("formatPrice n'est pas importé depuis ./format.ts")
    return problems


def check_4_6():
    s = read("src/invoice.ts")
    problems = []
    if len(re.findall(r"\bfunction\b", s)) < 2:
        problems.append("invoice.ts ne contient toujours qu'une seule fonction")
    problems += tsc_errors("src/invoice.ts")
    return problems


def check_5_3():
    s = read("src/notes.ts")
    zones = ["vaud", "geneve", "valais", "fribourg", "neuchatel", "jura"]
    return [f'"zone-{z}" manque' for z in zones if f'"zone-{z}"' not in s]


def check_5_4():
    out = run("node", "-e",
              'import("./src/catalog.ts").then(m => console.log(JSON.stringify(m.CATALOG)))')
    if out.returncode != 0:
        return ["catalog.ts ne se charge pas : " + out.stderr.strip().splitlines()[-1]]
    import json
    catalog = json.loads(out.stdout)
    problems = []
    if len(catalog) != 14:
        problems.append(f"CATALOG contient {len(catalog)} produits au lieu de 14")
    by_id = {p["id"]: p for p in catalog}
    if by_id.get("p10", {}).get("price") != 2.95:
        problems.append("p10 (Lait d'avoine) doit coûter 2.95")
    if by_id.get("p07", {}).get("name") != "Sirop d'érable":
        problems.append("p07 doit s'appeler \"Sirop d'érable\"")
    if re.search(r"^// p\d\d;", read("src/catalog.ts"), re.M):
        problems.append("il reste des lignes commentées // pXX;...")
    return problems


def check_5_5():
    s = read("src/notes.ts")
    problems = []
    if "TODO(jeremy)" in s:
        problems.append("il reste des TODO(jeremy)")
    if s.count("TODO(equipe)") != 4:
        problems.append("on attend 4 TODO(equipe)")
    return problems


def check_6_1():
    return tsc_errors("src/errors.ts")


def check_6_2():
    out = run("node", "--test", *[str(p) for p in sorted((ROOT / "test").glob("*.test.ts"))])
    if out.returncode == 0:
        return []
    fails = [l for l in out.stdout.splitlines() if l.startswith("not ok")]
    return ["tests en échec : " + "; ".join(fails or ["voir node --test"])]


def check_7_2():
    archive = ROOT / "assets" / "archive"
    problems = []
    if not archive.is_dir():
        return ["le dossier assets/archive n'existe pas"]
    for d in ["03", "07"]:
        name = f"IMG_202603{d}_0912.txt"
        if not (archive / name).exists():
            problems.append(f"{name} n'est pas dans assets/archive")
        if (ROOT / "assets" / "photos" / name).exists():
            problems.append(f"{name} est encore dans assets/photos (il faut le déplacer)")
    return problems


def check_7_3():
    photos = ROOT / "assets" / "photos"
    expected = {f"mars-{d}.txt" for d in ["12", "15", "21", "28"]}
    present = {p.name for p in photos.iterdir()}
    problems = [f"{n} manque" for n in sorted(expected - present)]
    if left := sorted(n for n in present
                      if n.startswith("IMG_") and n[10:12] in {"12", "15", "21", "28"}):
        problems.append(f"pas encore renommés : {', '.join(left)}")
    return problems


def check_8_2():
    out = run("git", "log", "--oneline", f"{START}..HEAD")
    if out.returncode != 0:
        return ["le tag git 'depart' est introuvable"]
    return [] if out.stdout.strip() else ["aucun commit depuis le départ"]


def check_9():
    problems = []
    for check in (check_4_1, check_6_1, check_6_2):
        problems += check()
    s = read("src/pricing.ts")
    if "FREE_SHIPPING_THRESHOLD" not in s:
        problems.append("pricing.ts doit exporter FREE_SHIPPING_THRESHOLD")
    if "FREE_SHIPPING_THRESHOLD" not in read("src/errors.ts"):
        problems.append("errors.ts (shippingCost) doit utiliser FREE_SHIPPING_THRESHOLD")
    problems += check_8_2()
    return problems


CHECKS = {
    "4.1": (check_4_1, ["src", "test"]),
    "4.2": (check_4_2, ["config", "scripts"]),
    "4.3": (check_4_3, ["scripts/report.py"]),
    "4.4": (check_4_4, ["src/notes.ts"]),
    "4.5": (check_4_5, ["src/missing-import.ts"]),
    "4.6": (check_4_6, ["src/invoice.ts"]),
    "5.3": (check_5_3, ["src/notes.ts"]),
    "5.4": (check_5_4, ["src/catalog.ts"]),
    "5.5": (check_5_5, ["src/notes.ts"]),
    "6.1": (check_6_1, ["src/errors.ts"]),
    "6.2": (check_6_2, ["src/pricing.ts"]),
    "7.2": (check_7_2, ["assets"]),
    "7.3": (check_7_3, ["assets"]),
    "8.2": (check_8_2, []),
    "9": (check_9, ["src", "test"]),
}


def reset(paths):
    if run("git", "rev-parse", START).returncode != 0:
        sys.exit("Tag git 'depart' introuvable : impossible de remettre à zéro.")
    run("git", "restore", f"--source={START}", "--worktree", "--", *paths)
    run("git", "clean", "-fdq", "--", *paths)
    print(f"Remis à zéro : {', '.join(paths)}")


def main(args):
    if args and args[0] == "--reset":
        if len(args) > 1:
            reset(CHECKS[args[1]][1] or ["."])
        else:
            reset(["src", "test", "scripts", "config", "assets"])
        return 0
    ids = args or list(CHECKS)
    failed = 0
    for ex in ids:
        if ex not in CHECKS:
            print(f"Exercice inconnu : {ex}. Exercices vérifiables : {', '.join(CHECKS)}")
            return 2
        problems = CHECKS[ex][0]()
        if problems:
            failed += 1
            print(f"❌ {ex}")
            for p in problems:
                print(f"     - {p}")
        else:
            print(f"✅ {ex}")
    if len(ids) > 1:
        print(f"\n{len(ids) - failed}/{len(ids)} exercices réussis")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
