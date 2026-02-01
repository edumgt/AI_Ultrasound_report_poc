from __future__ import annotations
import os, json, datetime
from typing import Dict, Any

def save_session(base_dir: str, raw_text: str, corrected_text: str, report_text: str, structured: Dict[str, Any]) -> str:
    os.makedirs(base_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = os.path.join(base_dir, ts)
    os.makedirs(folder, exist_ok=True)

    with open(os.path.join(folder, "raw.txt"), "w", encoding="utf-8") as f:
        f.write(raw_text or "")
    with open(os.path.join(folder, "corrected.txt"), "w", encoding="utf-8") as f:
        f.write(corrected_text or "")
    with open(os.path.join(folder, "report.txt"), "w", encoding="utf-8") as f:
        f.write(report_text or "")
    with open(os.path.join(folder, "structured.json"), "w", encoding="utf-8") as f:
        json.dump(structured or {}, f, ensure_ascii=False, indent=2)

    return folder
