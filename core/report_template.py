from __future__ import annotations
from jinja2 import Environment, FileSystemLoader

class ReportRenderer:
    def __init__(self, template_dir: str, template_name: str = "report_ko_en.j2"):
        env = Environment(loader=FileSystemLoader(template_dir), autoescape=False)
        self.tpl = env.get_template(template_name)

    def render(self, structured: dict, cleaned_text: str) -> str:
        return self.tpl.render(structured=structured, cleaned_text=cleaned_text)
