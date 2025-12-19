from llm.client import call_llm
from llm.retry import safe_llm_call
from llm.prompts import cost_optimization_prompt
from utils.validators import validate_report

def generate_cost_optimization_report(project_profile: dict, billing_reports: list, analysis_data: dict) -> dict:
    result = safe_llm_call(
        call_llm,
        cost_optimization_prompt(project_profile, billing_reports, analysis_data)
    )
    validate_report(result)
    return result
