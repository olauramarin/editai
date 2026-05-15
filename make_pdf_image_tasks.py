import json
from pathlib import Path

GITHUB_USER = "olauramarin"
GITHUB_REPO = "editai"
BRANCH = "main"

PAGES_DIR = Path("pages")
OUT = Path("tasks.json")

def infer_language(name: str) -> str:
    low = name.lower()
    if "romanian" in low or "-ro-" in low:
        return "Romanian"
    if "english" in low or "-en-" in low:
        return "English"
    if "hungarian" in low or "-hu-" in low:
        return "Hungarian"
    return "Unknown"

def infer_condition(name: str) -> str:
    low = name.lower()
    if "loweffort" in low:
        return "loweffort"
    if "mistakes" in low:
        return "mistakes"
    if "default" in low:
        return "default"
    return "unknown"

def infer_grade(name: str) -> str:
    if name.startswith("5-6_"):
        return "5-6"
    if name.startswith("7-9_"):
        return "7-9"
    if name.startswith("10-12_"):
        return "10-12"
    return "Unknown"

def infer_problem(folder_name: str) -> str:
    # examples:
    # 5-6_esm_esm-romanian-default -> esm
    # 5-6_cartonase_cartonase-ro-default -> cartonase
    # 7-9_scuderia_scuderia-romanian-default -> scuderia
    parts = folder_name.split("_")
    if len(parts) >= 2:
        return parts[1]
    return folder_name

def raw_url(path: Path) -> str:
    # Convert local path like pages/.../page-1.png to GitHub raw URL
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{BRANCH}/{path.as_posix()}"

tasks = []

for folder in sorted(PAGES_DIR.iterdir()):
    if not folder.is_dir():
        continue

    pngs = sorted(folder.glob("*.png"))
    if not pngs:
        continue

    folder_name = folder.name
    problem = infer_problem(folder_name)
    grade = infer_grade(folder_name)
    language = infer_language(folder_name)
    condition = infer_condition(folder_name)

    tasks.append({
        "data": {
            "title": f"{problem} — {language} — {condition}",
            "problem": problem,
            "grade": grade,
            "language": language,
            "condition": condition,
            "pages": [raw_url(p) for p in pngs]
        }
    })

OUT.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {len(tasks)} tasks to {OUT}")
