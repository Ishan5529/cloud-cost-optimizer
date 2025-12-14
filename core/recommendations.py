from llm.client import call_llm
from llm.retry import safe_llm_call
from llm.prompts import recommendation_prompt
from utils.validators import validate_report

def generate_report(profile: dict, billing: list) -> dict:
    result = safe_llm_call(call_llm, recommendation_prompt(str(profile), str(billing)))
    validate_report(result)
    return result
