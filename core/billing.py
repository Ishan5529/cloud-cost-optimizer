import random
from llm.client import call_llm
from llm.retry import safe_llm_call
from llm.prompts import billing_prompt
from utils.validators import validate_billing

def generate_billing(project_profile: dict, count=None) -> list:
    if count is None:
        count = random.randint(12, 20)
    # result = safe_llm_call(call_llm, billing_prompt(project_profile))
    # validate_billing(result)
    bills = []

    for _ in range(count):
        bill = safe_llm_call(
            call_llm,
            billing_prompt(project_profile)
        )
        bills.append(bill)
    return bills
