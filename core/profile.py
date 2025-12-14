from llm.client import call_llm
from llm.retry import safe_llm_call
from llm.prompts import profile_prompt, profile_retry_prompt
from utils.validators import validate_project_profile

def generate_project_profile(description: str) -> dict:
    try:
        result = safe_llm_call(call_llm, profile_prompt(description))

        validate_project_profile(result)
        return result

    except Exception as first_error:
        # Retry in-case of a mistake
        retry_result = safe_llm_call(
            call_llm,
            profile_retry_prompt(description, str(first_error))
        )

        if isinstance(retry_result, dict) and retry_result.get("error") == "Insufficient project details":
            print("\n\nInput does not contain sufficient information to generate a project profile\n\n")
            return None
            # raise RuntimeError("Input does not contain sufficient information to generate a project profile")

        validate_project_profile(retry_result)
        return retry_result
