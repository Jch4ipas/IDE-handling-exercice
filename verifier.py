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
    if file is None:
        return errors
    mine = [e for e in errors if e.startswith(file)]
    # With a syntax error (TS1xxx) anywhere, tsc skips type checking: report it
    syntax = [e for e in errors if re.search(r"error TS1\d{3}:", e) and not e.startswith(file)]
    if syntax and not mine:
        return ["erreur de syntaxe dans un autre fichier, corrige-la d'abord : " + syntax[0]]
    return mine


def py_tests_ok():
    return run(sys.executable, "-m", "unittest", "-q", cwd=ROOT / "scripts").returncode == 0


# Chaque vérification renvoie une liste de problèmes (vide = réussi).

def answer(prefix):
    """Réponse écrite après « PREFIX ... : » dans reponses.txt ('' si vide)."""
    for line in read("reponses.txt").splitlines():
        if line.startswith(prefix + " "):
            return line.partition(" :")[2].strip()
    return ""


def function_body(source, name):
    """Texte de la fonction NAME (de sa ligne 'function NAME' à la '}' finale)."""
    m = re.search(r"^(export )?function " + name + r"\b.*?^\}", source, re.M | re.S)
    return m.group(0) if m else ""


def check_1_1():
    problems = []
    for f in ["src/api/client.ts", "src/utils/strings.ts", "scripts/tools/cleanup.py"]:
        if 'VERSION = "1.0"' not in read(f):
            problems.append(f'{f} : VERSION doit valoir "1.0" (fichier sauvegardé ?)')
    return problems


def check_1_2():
    problems = []
    if 'CONTACT = "aide@petite-boutique.ch"' not in read("src/api/client.ts"):
        problems.append("src/api/client.ts : CONTACT doit être l'adresse SUPPORT_EMAIL de strings.ts")
    if 'OWNER = "Petite Boutique"' not in read("scripts/tools/cleanup.py"):
        problems.append("scripts/tools/cleanup.py : OWNER doit être le nom de la boutique (settings.yaml)")
    return problems


def check_1_3():
    text = read("docs/equipe.txt")
    names, _, rest = text.partition("\n\n")
    problems = []
    lines = names.splitlines()
    if lines != sorted(set(lines)):
        problems.append("la liste des prénoms doit être triée, sans doublon")
    if not re.search(r"consult-line : M-s l\s*$", rest, re.M):
        problems.append("écris la touche de consult-line après « touche de consult-line : »")
    return problems


def check_1_4():
    s = read("src/labels.ts")
    problems = []
    if '"Bonjour"' not in function_body(s, "greeting"):
        problems.append("greeting doit encore renvoyer \"Bonjour\" (annule seulement ce changement)")
    if '"Ciao"' not in function_body(s, "farewell"):
        problems.append("farewell doit renvoyer \"Ciao\"")
    return problems


def check_1_r():
    problems = []
    if "RETRIES = 5;" not in read("src/api/client.ts"):
        problems.append("src/api/client.ts : RETRIES doit valoir 5")
    if "DRY_RUN = True" not in read("scripts/tools/cleanup.py"):
        problems.append("scripts/tools/cleanup.py : DRY_RUN doit valoir True")
    if "TIMEOUT = 10;" not in read("src/api/client.ts"):
        problems.append("src/api/client.ts : TIMEOUT ne devait pas changer (10)")
    return problems


def section(name):
    """Une section « ===== NAME » de src/livraison.ts."""
    s = read("src/livraison.ts")
    m = re.search(r"// ===== " + re.escape(name) + r".*?(?=// =====|\Z)", s, re.S)
    return m.group(0) if m else ""


def check_2_1():
    s = section("2.1")
    problems = []
    for line in ["const BASE_FEE = 7.9;", "const EXPRESS_FEE = 14.5;", "const FREE_FROM = 50;",
                 "return total >= FREE_FROM ? 0 : BASE_FEE;", "return EXPRESS_FEE;"]:
        if line not in s:
            problems.append(f"il manque le ; à la fin de : {line[:-1]}")
    for fn in ["standardFee", "expressFee"]:
        if not re.search(r"^export function " + fn, s, re.M):
            problems.append(f"ajoute export devant function {fn}")
    if "à supprimer" in s:
        problems.append("il reste des lignes « // à supprimer »")
    return problems


def check_2_2():
    s = section("2.2")
    problems = []
    if 'LABEL_STANDARD = "Livraison standard";' not in s:
        problems.append('LABEL_STANDARD doit valoir "Livraison standard"')
    if 'LABEL_EXPRESS = "Livraison express en 24h";' not in s:
        problems.append('LABEL_EXPRESS doit valoir "Livraison express en 24h"')
    if "fee(zone: string, express: boolean)" not in s:
        problems.append("supprime le paramètre « poids: number, » de fee")
    return problems


def check_2_3():
    s = section("2.3")
    problems = []
    if not (0 <= s.find("function first") < s.find("function second")):
        problems.append("first() doit être au-dessus de second()")
    if 'console.log("frais");' not in s:
        problems.append('logFee doit contenir seulement console.log("frais");')
    if problems == [] and tsc_errors("src/livraison.ts"):
        problems += tsc_errors("src/livraison.ts")
    return problems


def check_2_4():
    s = read("src/tarifs.ts")
    problems = []
    if "return 12;" not in function_body(s, "tarifValais"):
        problems.append("tarifValais doit renvoyer 12")
    if "return 9;" not in function_body(s, "tarifJura"):
        problems.append("tarifJura doit renvoyer 9")
    if "MINIMUM_ORDER = 20;" not in s:
        problems.append("MINIMUM_ORDER (ligne 31) doit valoir 20")
    return problems


def check_2_5():
    s = section("2.5")
    expected = {"fribourg": "Fribourg", "jura": "Delemont", "neuchatel": "Neuchatel", "vaud": "Lausanne"}
    return [f'{k} doit valoir "{v}"' for k, v in expected.items() if f'{k}: "{v}",' not in s]


def check_2_6():
    if "return base + 4.5;" not in function_body(read("src/tarifs.ts"), "weekendTotal"):
        return ["weekendTotal doit faire base + 4.5 (la valeur de WEEKEND_SURCHARGE)"]
    return []


def check_2_r():
    s = read("src/tarifs.ts")
    problems = []
    body = function_body(s, "tarifTessin")
    if "return 13;" not in body:
        problems.append("tarifTessin : il manque le ; après return 13")
    if "ancien" in s:
        problems.append("supprime le mot « ancien » du commentaire du Tessin")
    if not (0 <= s.find("function tarifTessin") < s.find("function tarifArgovie")):
        problems.append("tarifTessin doit être la première fonction, avant tarifArgovie")
    return problems


def line_before(source, pattern):
    """Ligne juste au-dessus de la première ligne qui correspond à PATTERN."""
    lines = source.splitlines()
    for i, line in enumerate(lines):
        if re.search(pattern, line):
            return lines[i - 1].strip() if i else ""
    return ""


def check_3_1():
    problems = []
    pricing = read("src/pricing.ts")
    if line_before(pricing, r"^export function (calcTotal|computeCartTotal)\b") != "// étape 1":
        problems.append("« // étape 1 » doit être juste au-dessus de la définition de calcTotal")
    if line_before(pricing, r"^export function applyDiscount\b") != "// étape 2":
        problems.append("« // étape 2 » doit être juste au-dessus de la définition de applyDiscount")
    if not re.search(r"^const guestTotal = .*// étape 3$", read("src/index.ts"), re.M):
        problems.append("« // étape 3 » doit être à la fin de la ligne const guestTotal de index.ts")
    if line_before(read("src/format.ts"), r"^export function formatPrice\b") != "// étape 4":
        problems.append("« // étape 4 » doit être juste au-dessus de la définition de formatPrice")
    return problems


def check_3_2():
    problems = []
    for f in ["src/index.ts", "src/errors.ts", "src/invoice.ts"]:
        for n, line in enumerate(read(f).splitlines(), 1):
            # In invoice.ts only the loop line: the extraction of exercise 4.6
            # moves the other calls and their trailing comments
            if f == "src/invoice.ts" and "formatPrice(item.price" not in line:
                continue
            if "formatPrice(" in line and not line.rstrip().endswith("// prix affiché"):
                problems.append(f"{f}:{n} appelle formatPrice sans « // prix affiché » à la fin")
    return problems


def check_3_3():
    s = read("src/index.ts")
    problems = []
    if not re.search(r"buildInvoice\(\s*alice\s*,\s*\[\]\s*\)", s):
        problems.append("index.ts doit appeler buildInvoice(alice, []) (le client d'abord)")
    problems += tsc_errors("src/index.ts")
    return problems


def check_3_4():
    problems = []
    ts_files = [f for f in grep("TAX_RATE", "src", "test") if f.endswith(".ts")]
    if answer("3.4a") != str(len(ts_files)):
        problems.append("3.4a : mauvais nombre de fichiers .ts (filtre avec -- -g *.ts)")
    if "catalog.ts" not in answer("3.4b"):
        problems.append("3.4b : mauvais fichier pour « Lait d'avoine »")
    return problems


def check_3_5():
    return [] if "pricing.ts" in answer("3.5") else ["3.5 : mauvais fichier pour discountFor"]


def check_3_r():
    problems = []
    for f in ["src/pricing.ts", "src/cart.ts"]:
        for n, line in enumerate(read(f).splitlines(), 1):
            if "discountFor(" in line and not line.rstrip().endswith("// R3"):
                problems.append(f"{f}:{n} contient discountFor sans « // R3 » à la fin")
    return problems

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


# Built from pieces so that a project-wide replace (exercise 4.2) cannot
# rewrite this file by accident
OLD_KEY, NEW_KEY = "api" + "_url", "base" + "_url"


def check_4_2():
    problems = []
    if left := grep(OLD_KEY, "config", "scripts"):
        problems.append(f"'{OLD_KEY}' existe encore dans : {', '.join(left)}")
    for f in ["config/settings.yaml", "scripts/report.py", "scripts/test_report.py", "scripts/deploy.sh"]:
        if NEW_KEY not in read(f):
            problems.append(f"'{NEW_KEY}' manque dans {f}")
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



def check_4_7():
    s = read("src/messy.ts")
    problems = []
    if "roundPrice" in s or "MEMBER_DISCOUNT" in s:
        problems.append("les imports inutilisés (roundPrice, MEMBER_DISCOUNT) doivent disparaître")
    if len(re.findall(r'from "\./format\.ts"', s)) != 1:
        problems.append("un seul import depuis ./format.ts")
    depth = 0
    for n, line in enumerate(s.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("}"):
            depth -= 1
        if stripped and len(line) - len(line.lstrip()) != 2 * depth:
            problems.append(f"ligne {n} mal indentée : {stripped}")
            break
        depth += stripped.count("{") - stripped.count("}") + (1 if stripped.startswith("}") else 0)
    return problems



def check_5_1():
    s = read("src/selection.ts")
    problems = []
    body = function_body(s, "biggest")
    if "return Math.max(a, b);" not in body or "else" in body:
        problems.append("le corps de biggest doit être seulement return Math.max(a, b);")
    if "return n * 3;" not in function_body(s, "thrice"):
        problems.append("ajoute la fonction thrice (copie de twice) qui renvoie n * 3")
    if "return n * 2;" not in function_body(s, "twice"):
        problems.append("twice doit rester inchangée")
    return problems


def check_5_2():
    lines = read("src/ordre.ts").splitlines()
    idx = [next((i for i, l in enumerate(lines) if l.startswith(f"export const ETAPE_{k} ")), -1)
           for k in (1, 2, 3)]
    if -1 in idx or idx != list(range(idx[0], idx[0] + 3)):
        return ["ETAPE_1, ETAPE_2 et ETAPE_3 doivent être sur 3 lignes qui se suivent, dans l'ordre"]
    return []


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



def check_5_6():
    s = read("src/petites.ts")
    problems = []
    for line, hint in [('export const shop = "Petite Boutique";', "M-t"),
                       ('export const currency = "CHF";', "M-u"),
                       ("export const total = 42;", "M-SPC"),
                       ('export const greeting = "Bonjour";', "M-^"),
                       ("// debugger;", "s-/")]:
        if line not in s:
            problems.append(f"on attend la ligne : {line}   ({hint})")
    if "\n\n\n" in s:
        problems.append("il reste plusieurs lignes vides d'affilée (C-x C-o)")
    if not re.search(r"^// -{40}$", s, re.M):
        problems.append("ajoute une ligne « // » suivie de 40 tirets (C-u 40 -)")
    return problems


def check_5_7():
    s = read("src/complete.ts")
    problems = []
    if not re.search(r"^const n = cart\.count\(\);", s, re.M):
        problems.append("écris : const n = cart.count();")
    if not re.search(r"^export const label = formatQuantity\(n\);", s, re.M):
        problems.append("écris : export const label = formatQuantity(n);")
    problems += tsc_errors("src/complete.ts")
    return problems


def check_5_r():
    s = read("src/revision.ts")
    problems = []
    for c in ["rouge", "vert", "bleu", "jaune"]:
        if f'"c-{c}"' not in s:
            problems.append(f'"c-{c}" manque (rectangle)')
    if re.search(r"\bprix\(", s) or s.count("prixArticle(") != 3:
        problems.append("prix doit être renommée prixArticle partout (3 endroits)")
    problems += tsc_errors("src/revision.ts")
    return problems


def check_6_1():
    return tsc_errors("src/errors.ts")


def check_6_2():
    out = run("node", "--test", *[str(p) for p in sorted((ROOT / "test").glob("*.test.ts"))])
    if out.returncode == 0:
        return []
    fails = [l.strip() for l in out.stdout.splitlines() if l.strip().startswith("not ok")]
    return ["tests en échec : " + "; ".join(fails or ["voir node --test"])]



def check_6_3():
    if not answer("6.3").startswith("Déploiement vers https://"):
        return ["6.3 : insère la sortie de ./scripts/deploy.sh (C-u M-!) après les deux-points"]
    return []


def check_7_1():
    s = read("src/pricing.ts")
    problems = []
    if not re.search(r"^export function calcSubtotal\b.*// test : 25$", s, re.M):
        problems.append("ajoute « // test : 25 » à la fin de la ligne export function calcSubtotal")
    if not re.search(r"^export function applyDiscount\b.*// test : 90$", s, re.M):
        problems.append("ajoute « // test : 90 » à la fin de la ligne export function applyDiscount")
    return problems


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



def check_8_1():
    s = read("src/labels.ts")
    problems = []
    if 'return "Merci";' not in function_body(s, "thanks"):
        problems.append('thanks doit renvoyer "Merci" (annule ce changement avec C-x v n)')
    if 'return "Pardon";' not in function_body(s, "sorry"):
        problems.append('sorry doit renvoyer "Pardon"')
    return problems


def check_8_2():
    out = run("git", "log", "--oneline", f"{START}..HEAD")
    if out.returncode != 0:
        return ["le tag git 'depart' est introuvable"]
    return [] if out.stdout.strip() else ["aucun commit depuis le départ"]



def check_8_3():
    problems = []
    first = run("git", "log", "--reverse", "--format=%s").stdout.splitlines()
    if not first or answer("8.3a") != first[0]:
        problems.append("8.3a : ce n'est pas le message du premier commit (l l dans magit, tout en bas)")
    line = next(n for n, l in enumerate(read("src/pricing.ts").splitlines(), 1) if "TAX_RATE =" in l)
    blame = run("git", "blame", "--porcelain", "-L", f"{line},{line}", "src/pricing.ts").stdout
    author = next((l[7:] for l in blame.splitlines() if l.startswith("author ")), "?")
    if answer("8.3b") != author:
        problems.append("8.3b : ce n'est pas l'auteur de la ligne TAX_RATE (blame)")
    return problems


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
    "1.1": (check_1_1, ["src/api", "src/utils", "scripts/tools"]),
    "1.2": (check_1_2, ["src/api", "scripts/tools"]),
    "1.3": (check_1_3, ["docs"]),
    "1.4": (check_1_4, ["src/labels.ts"]),
    "1.R": (check_1_r, ["src/api", "scripts/tools"]),
    "2.1": (check_2_1, ["src/livraison.ts"]),
    "2.2": (check_2_2, ["src/livraison.ts"]),
    "2.3": (check_2_3, ["src/livraison.ts"]),
    "2.4": (check_2_4, ["src/tarifs.ts"]),
    "2.5": (check_2_5, ["src/livraison.ts"]),
    "2.6": (check_2_6, ["src/tarifs.ts"]),
    "2.R": (check_2_r, ["src/tarifs.ts"]),
    "3.1": (check_3_1, ["src/pricing.ts", "src/index.ts", "src/format.ts"]),
    "3.2": (check_3_2, ["src/index.ts", "src/errors.ts", "src/invoice.ts"]),
    "3.3": (check_3_3, ["src/index.ts"]),
    "3.4": (check_3_4, ["reponses.txt"]),
    "3.5": (check_3_5, ["reponses.txt"]),
    "3.R": (check_3_r, ["src/pricing.ts", "src/cart.ts"]),
    "4.1": (check_4_1, ["src", "test"]),
    "4.2": (check_4_2, ["config", "scripts"]),
    "4.3": (check_4_3, ["scripts/report.py"]),
    "4.4": (check_4_4, ["src/notes.ts"]),
    "4.5": (check_4_5, ["src/missing-import.ts"]),
    "4.6": (check_4_6, ["src/invoice.ts"]),
    "4.7": (check_4_7, ["src/messy.ts"]),
    "5.1": (check_5_1, ["src/selection.ts"]),
    "5.2": (check_5_2, ["src/ordre.ts"]),
    "5.3": (check_5_3, ["src/notes.ts"]),
    "5.4": (check_5_4, ["src/catalog.ts"]),
    "5.5": (check_5_5, ["src/notes.ts"]),
    "5.6": (check_5_6, ["src/petites.ts"]),
    "5.7": (check_5_7, ["src/complete.ts"]),
    "5.R": (check_5_r, ["src/revision.ts"]),
    "6.1": (check_6_1, ["src/errors.ts"]),
    "6.2": (check_6_2, ["src/pricing.ts"]),
    "6.3": (check_6_3, ["reponses.txt"]),
    "7.1": (check_7_1, ["src/pricing.ts"]),
    "7.2": (check_7_2, ["assets"]),
    "7.3": (check_7_3, ["assets"]),
    "8.1": (check_8_1, ["src/labels.ts"]),
    "8.2": (check_8_2, []),
    "8.3": (check_8_3, ["reponses.txt"]),
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
            reset(["src", "test", "scripts", "config", "assets", "docs", "reponses.txt"])
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
