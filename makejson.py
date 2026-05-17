import json
import random
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

GITHUB_USER = "olauramarin"
GITHUB_REPO = "editai"
BRANCH = "main"

PAGES_DIR = Path("pages")
OUT = Path("tasks.json")
PRIVATE_MAPPING_OUT = Path("condition_mapping_PRIVATE_DO_NOT_IMPORT.json")

RANDOM_SEED = 42

PROBLEM_DISPLAY = {
    "birocratie": "Birocrație",
    "cartonase": "Cartonașe",
    "cercetasi": "Cercetași",
    "esm": "ESM",
    "expresie": "Expresie",
    "legos": "Legos",
    "proeminenta": "Proeminența",
    "regate": "Regate",
    "scuderia": "Scuderia",
}

PROBLEM_GRADE = {
    "cartonase": "5-6",
    "esm": "5-6",
    "legos": "5-6",

    "scuderia": "7-9",
    "expresie": "7-9",
    "proeminenta": "7-9",

    "birocratie": "10-12",
    "cercetasi": "10-12",
    "regate": "10-12",
}

CONDITION_TO_PRIVATE_ID = {
    "unknown": 1768556701,
    "default": 14323124233,
    "loweffort": 1243232132,
    "mistakes": 1343543243,
}

def normalize_text(s: str) -> str:
    s = s.lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s

def infer_condition(name: str) -> str:
    low = normalize_text(name)

    if any(x in low for x in ["loweffort", "low_effort", "low-effort", "low effort", "leneș", "lenes"]):
        return "loweffort"

    if any(x in low for x in ["mistakes", "mistake", "errors", "error", "greseli", "greșeli", "wrong"]):
        return "mistakes"

    if any(x in low for x in ["default", "normal", "standard", "baseline"]):
        return "default"

    return "unknown"

def infer_language(name: str) -> str:
    low = normalize_text(name)

    if any(x in low for x in ["romanian", "-ro-", "_ro_", " romana", " română", "-ro.", "_ro."]):
        return "Română"

    if any(x in low for x in ["english", "-en-", "_en_", " engleza", " engleză", "-en.", "_en."]):
        return "Engleză"

    if any(x in low for x in ["hungarian", "-hu-", "_hu_", " maghiara", " maghiară", "-hu.", "_hu."]):
        return "Maghiară"

    return "Necunoscută"

def infer_problem_key(name: str) -> str:
    low = normalize_text(name)

    for key in PROBLEM_DISPLAY:
        if key in low:
            return key

    fallback = re.split(r"[_\-\s]+", low)[0]
    return fallback if fallback else "unknown_problem"

def page_number(path: Path) -> int:
    match = re.search(r"(\d+)$", path.stem)
    if match:
        return int(match.group(1))
    return 999999

def raw_url(path: Path) -> str:
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{BRANCH}/{path.as_posix()}"

tasks_by_problem = defaultdict(list)

for folder in sorted(PAGES_DIR.iterdir()):
    if not folder.is_dir():
        continue

    pngs = sorted(folder.glob("*.png"), key=page_number)
    if not pngs:
        continue

    folder_name = folder.name

    problem_key = infer_problem_key(folder_name)
    problem_display = PROBLEM_DISPLAY.get(problem_key, problem_key)
    grade = PROBLEM_GRADE.get(problem_key, "Necunoscută")
    language = infer_language(folder_name)
    condition = infer_condition(folder_name)

    tasks_by_problem[problem_key].append({
        "folder": folder,
        "pngs": pngs,
        "problem_key": problem_key,
        "problem_display": problem_display,
        "grade": grade,
        "language": language,
        "condition": condition,
    })

tasks = []
private_mapping = []

for problem_key, items in sorted(tasks_by_problem.items()):
   
    rng = random.Random(f"{RANDOM_SEED}-{problem_key}")
    rng.shuffle(items)

    for idx, item in enumerate(items, start=1):
        variant_id = f"{problem_key}_{idx:03d}"
        visible_title = f"{item['problem_display']} — clasele {item['grade']} — {item['language']} — varianta {idx}"

        # PUBLIC JSON imported into Label Studio   
        tasks.append({
            "data": {
                "title": visible_title,
                "problem": item["problem_display"],
                "grade": item["grade"],
                "language": item["language"],
                "variant_id": variant_id,
                "rand_order": idx,
                "pages": [raw_url(p) for p in item["pngs"]],
            }
        })

        # PRIVATE mapping.
        private_mapping.append({
            "variant_id": variant_id,
            "folder": item["folder"].as_posix(),
            "problem": item["problem_display"],
            "grade": item["grade"],
            "language": item["language"],
            "rand_order": idx,
            "private_condition_id": CONDITION_TO_PRIVATE_ID[item["condition"]],
            "real_condition": item["condition"],
        })

OUT.write_text(
    json.dumps(tasks, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

PRIVATE_MAPPING_OUT.write_text(
    json.dumps(private_mapping, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Wrote {len(tasks)} PNG tasks to {OUT}")
print(f"Wrote private mapping to {PRIVATE_MAPPING_OUT}")