import json
from pathlib import Path

ROOT = Path(".")
OUT = Path("labelstudio_tasks.json")

def read_text(path: Path | None) -> str:
    if path and path.exists():
        return path.read_text(encoding="utf-8", errors="replace").strip()
    return ""

def find_first(patterns):
    for pattern in patterns:
        matches = list(ROOT.glob(pattern))
        if matches:
            return matches[0]
    return None

def infer_language(filename: str) -> str:
    name = filename.lower()
    if "romanian" in name or "-ro-" in name or "ro-" in name:
        return "Romanian"
    if "english" in name or "-en-" in name:
        return "English"
    if "hungarian" in name or "-hu-" in name:
        return "Hungarian"
    return "Unknown"

def infer_condition(filename: str) -> str:
    name = filename.lower()
    if "loweffort" in name:
        return "loweffort"
    if "mistakes" in name:
        return "mistakes"
    if "default" in name:
        return "default"
    return "unknown"

def problem_from_path(path: Path) -> str:
    parts = path.parts
    if len(parts) >= 3:
        return parts[-2]
    return path.stem

def grade_from_path(path: Path) -> str:
    for p in path.parts:
        if p in {"5-6", "7-9", "10-12"}:
            return p
    return "Unknown"

def reference_patterns(problem: str, grade: str):
    p = problem.lower()

    mapping = {
        "esm": {
            "statement": [f"{grade}/esm.txt"],
            "official": [f"{grade}/editorial esm.txt"],
            "code": [f"{grade}/esm.cpp"],
        },
        "cartonase": {
            "statement": [f"{grade}/cartonase 2025.txt"],
            "official": [f"{grade}/cartonase_editorial.txt"],
            "code": [f"{grade}/cartonase.cpp"],
        },
        "legos": {
            "statement": [f"{grade}/legos.txt"],
            "official": [f"{grade}/legos(1).txt"],
            "code": [f"{grade}/legos.cpp"],
        },
        "scuderia": {
            "statement": [f"{grade}/scuderia ro.txt"],
            "official": [f"{grade}/scuderia editorial.txt"],
            "code": [f"{grade}/1073073-scuderia.cpp"],
        },
        "expresie": {
            "statement": [f"{grade}/expresie.txt"],
            "official": [f"{grade}/expresie_editorial.txt"],
            "code": [f"{grade}/362982-expresie.cpp"],
        },
        "proeminenta": {
            "statement": [f"{grade}/proeminenta.txt"],
            "official": [f"{grade}/proeminenta editorial.txt"],
            "code": [f"{grade}/proeminenta_paul_100.cpp"],
        },
        "cercetasi": {
            "statement": [f"{grade}/CERCETASI_RO.txt"],
            "official": [f"{grade}/cercetasi_editorial.txt"],
            "code": [f"{grade}/cercetasi.cpp"],
        },
        "birocratie": {
            "statement": [f"{grade}/Birocratie_RO.txt"],
            "official": [f"{grade}/birocratie_editorial.txt"],
            "code": [f"{grade}/birocratie.cpp"],
        },
        "regate": {
            "statement": [f"{grade}/regate_RO.txt"],
            "official": [f"{grade}/regate_editorial.txt"],
            "code": [f"{grade}/regate.cpp"],
        },
    }

    return mapping.get(p, {"statement": [], "official": [], "code": []})

tasks = []

generated_txts = sorted([
    p for p in ROOT.glob("*/*/*.txt")
    if any(x in p.name.lower() for x in ["default", "loweffort", "mistakes"])
])

for path in generated_txts:
    problem = problem_from_path(path)
    grade = grade_from_path(path)
    language = infer_language(path.name)
    condition = infer_condition(path.name)

    refs = reference_patterns(problem, grade)

    statement_path = find_first(refs["statement"])
    official_path = find_first(refs["official"])
    code_path = find_first(refs["code"])

    tasks.append({
        "data": {
            "title": f"{problem} — {language} — {condition}",
            "problem": problem,
            "grade": grade,
            "language": language,
            "condition": condition,
            "source_file": str(path),
            "generated_editorial": read_text(path),
            "problem_statement": read_text(statement_path),
            "accepted_code": read_text(code_path),
            "official_editorial": read_text(official_path),
        }
    })

OUT.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {len(tasks)} tasks to {OUT}")
