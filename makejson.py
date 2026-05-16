import json
import re
from pathlib import Path
#hardcoded metadata
GITHUB_USER = "olauramarin"
GITHUB_REPO = "editai"
BRANCH = "main"

PAGES_DIR = Path("pages")
OUT = Path("tasks.json")

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

# EDIT 
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

LANGUAGE_DISPLAY = {
    "romanian": "Română",
    "ro": "Română",
    "english": "Engleză",
    "en": "Engleză",
    "hungarian": "Maghiară",
    "hu": "Maghiară",
}


def infer_condition(name: str) -> str:
    low = name.lower()
    if "loweffort" in low:
        return "loweffort"
    if "mistakes" in low:
        return "mistakes"
    if "default" in low:
        return "default"
    return "unknown"


def infer_language(name: str) -> str:
    low = name.lower()

    if "romanian" in low or "-ro-" in low or "_ro_" in low:
        return "Română"
    if "english" in low or "-en-" in low or "_en_" in low:
        return "Engleză"
    if "hungarian" in low or "-hu-" in low or "_hu_" in low:
        return "Maghiară"

    return "Necunoscută"


def infer_problem_key(folder_name: str) -> str:
    low = folder_name.lower()

    for key in PROBLEM_DISPLAY:
        if key in low:
            return key

    
    return re.split(r"[_-]", low)[0]


def page_number(path: Path) -> int:
    match = re.search(r"(\d+)$", path.stem)
    if match:
        return int(match.group(1))
    return 999999


def raw_url(path: Path) -> str:
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{BRANCH}/{path.as_posix()}"


tasks = []

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

    
    visible_title = f"{problem_display} — clasele {grade} — {language}"

    tasks.append({
        "data": {
            "title": visible_title,
            "problem": problem_display,
            "grade": grade,
            "language": language,

            
            "condition": condition,

            "pages": [raw_url(p) for p in pngs]
        }
    })

OUT.write_text(
    json.dumps(tasks, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Wrote {len(tasks)} tasks to {OUT}")
