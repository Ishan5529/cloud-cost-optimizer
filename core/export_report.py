from llm.client import call_llm
from llm.retry import safe_llm_text_call
from llm.prompts import export_report_prompt

def generate_report_content(
    project_description: str,
    project_profile: dict,
    billing: list,
    cost_optimization_report: dict
) -> str:
    return safe_llm_text_call(
        call_llm,
        export_report_prompt(
            project_description,
            project_profile,
            billing,
            cost_optimization_report
        )
    )
