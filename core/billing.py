from llm.client import call_llm
from llm.retry import safe_llm_call
from llm.prompts import billing_prompt
from utils.validators import validate_billing

def generate_billing(profile: dict) -> list:
    result = safe_llm_call(call_llm, billing_prompt(str(profile)))
    validate_billing(result)
    return result
