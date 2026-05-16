import json
import re
import unicodedata
from pathlib import Path

GITHUB_USER = "olauramarin"
GITHUB_REPO = "editai"
BRANCH = "main"

PDFS_DIR = Path("pdfs")
OUT = Path("tasks_pdfs.json")
PRIVATE_MAPPING_OUT = Path("condition_mapping_PRIVATE_DO_NOT_IMPORT.json")

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

CONDITION_TO_ID = {
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

def raw_url(path: Path) -> str:
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{BRANCH}/{path.as_posix()}"

tasks = []
private_condition_mapping = []

for pdf in sorted(PDFS_DIR.rglob("*.pdf")):
    
    full_name = f"{pdf.parent.name}-{pdf.stem}"

    problem_key = infer_problem_key(full_name)
    problem_display = PROBLEM_DISPLAY.get(problem_key, problem_key)
    grade = PROBLEM_GRADE.get(problem_key, "Necunoscută")
    language = infer_language(full_name)

    condition = infer_condition(full_name)
    condition_id = CONDITION_TO_ID.get(condition, 0)

    visible_title = f"{problem_display} — clasele {grade} — {language}"

    task_id = pdf.stem

    tasks.append({
        "data": {
            "title": visible_title,
            "problem": problem_display,
            "grade": grade,
            "language": language,

            
            "condition_id": condition_id,

            
            "file_id": task_id,

            
            "pdf": raw_url(pdf)
        }
    })

    # Private mapping
    private_condition_mapping.append({
        "file": pdf.as_posix(),
        "file_id": task_id,
        "problem": problem_display,
        "language": language,
        "condition_id": condition_id,
        "real_condition": condition,
    })

OUT.write_text(
    json.dumps(tasks, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

PRIVATE_MAPPING_OUT.write_text(
    json.dumps(private_condition_mapping, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Wrote {len(tasks)} PDF tasks to {OUT}")
print(f"Wrote private mapping to {PRIVATE_MAPPING_OUT}")
print("Condition IDs:")
for condition, cid in CONDITION_TO_ID.items():
    print(f"  {cid}: {condition}")
