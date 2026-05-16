import json
import re
from pathlib import Path

GITHUB_USER = "olauramarin"
GITHUB_REPO = "editai"
BRANCH = "main"

PDFS_DIR = Path("pdfs")
OUT = Path("tasks_pdfs.json")

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

def infer_problem_key(file_name: str) -> str:
    low = file_name.lower()

    for key in PROBLEM_DISPLAY:
        if key in low:
            return key

    return re.split(r"[_-]", low)[0]

def raw_url(path: Path) -> str:
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{BRANCH}/{path.as_posix()}"

tasks = []

for pdf in sorted(PDFS_DIR.rglob("*.pdf")):
    file_name = pdf.stem

    problem_key = infer_problem_key(file_name)
    problem_display = PROBLEM_DISPLAY.get(problem_key, problem_key)
    grade = PROBLEM_GRADE.get(problem_key, "Necunoscută")
    language = infer_language(file_name)
    condition = infer_condition(file_name)

    visible_title = f"{problem_display} — clasele {grade} — {language}"

    tasks.append({
        "data": {
            "title": visible_title,
            "problem": problem_display,
            "grade": grade,
            "language": language,

            "condition": condition,

            "pdf": raw_url(pdf)
        }
    })

OUT.write_text(
    json.dumps(tasks, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Wrote {len(tasks)} PDF tasks to {OUT}")