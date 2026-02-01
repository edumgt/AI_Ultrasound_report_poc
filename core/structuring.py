from __future__ import annotations
from typing import Dict, List, Optional

class Structurer:
    """
    PoC용 최소 구조화:
    - corrected_text에 canonical/alias가 들어오면 categories를 보고 location/lesion/feature를 채움
    - 실제 프로젝트에서는 좌표/측정값/다중 병변 등으로 확장 권장
    """
    def __init__(self, categories: Dict[str, List[str]], key_to_canonical: Optional[Dict[str, str]] = None):
        self.categories = categories
        self.key_to_canonical = key_to_canonical or {}

    def extract(self, corrected_text: str) -> Dict:
        out = {"location": None, "lesion": None, "feature": None, "notes": ""}
        # categories는 key 기반이므로 canonical로 변환해서 저장
        for key in self.categories.get("location", []):
            canon = self.key_to_canonical.get(key, key)
            if canon in corrected_text:
                out["location"] = canon
        for key in self.categories.get("lesion", []):
            canon = self.key_to_canonical.get(key, key)
            if canon in corrected_text:
                out["lesion"] = canon
        for key in self.categories.get("feature", []):
            canon = self.key_to_canonical.get(key, key)
            if canon in corrected_text:
                out["feature"] = canon

        out["notes"] = "Auto-extracted (PoC)"
        return out
