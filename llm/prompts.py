def profile_prompt(description: str) -> str:
    return f"""
You are a system that outputs STRICT JSON only.

ABSOLUTE RULES:
- Output exactly ONE JSON object
- Do NOT include explanations
- Do NOT include labels like "JSON FORMAT" or "Final JSON"
- Do NOT include markdown
- Do NOT ask questions
- Infer missing fields conservatively

INPUT:
{description}

OUTPUT JSON SCHEMA:
{{
  "name": "string",
  "budget_inr_per_month": number,
  "description": "string",
  "tech_stack": {{ }},
  "non_functional_requirements": []
}}
"""


def billing_prompt(profile_json: str) -> str:
    return f"""
You are a JSON generator.

STRICT RULES:
- Output ONLY a JSON array
- No text outside JSON
- 12 to 20 records
- Single month
- Provider-specific services (EC2, RDS, S3, etc.)
- Include region for every record
- Costs in INR

PROJECT PROFILE:
{profile_json}
"""


def recommendation_prompt(profile_json: str, billing_json: str) -> str:
    return f"""
You are a JSON generator.

STRICT RULES:
- Output ONLY valid JSON
- No explanations or markdown
- 6 to 10 recommendations
- Explicitly list AWS, Azure, GCP
- Savings are rough estimates
- Include architectural optimizations

PROJECT PROFILE:
{profile_json}

BILLING DATA:
{billing_json}

OUTPUT FORMAT:
{{
  "project_name": "",
  "analysis": {{}},
  "recommendations": [],
  "summary": {{}}
}}
"""

def profile_retry_prompt(original_description: str, error_message: str) -> str:
    return f"""
Your previous response FAILED validation.

Validation error:
{error_message}

IMPORTANT:
- If the input does NOT contain enough information to extract a meaningful project profile,
  you MUST return this EXACT JSON and nothing else:

{{ "error": "Insufficient project details" }}

Otherwise:
You MUST output a JSON object that EXACTLY matches the schema below.
ALL fields are MANDATORY except Non-Functional Requirements.
Do NOT remove any field.
Do NOT rename any field.
Do NOT return partial JSON.
Do NOT include explanations or markdown.

Fill in ALL values appropriately based on the input.

SCHEMA (DO NOT CHANGE KEYS):
{{
  "name": "string (project name)",
  "budget_inr_per_month": number,
  "description": "string",
  "tech_stack": {{
    "backend": "string",
    "database": "string",
    "storage": "string",
    "monitoring": "string",
    "analytics": "string"
  }},
  "non_functional_requirements": ["string"]
}}

INPUT:
{original_description}

OUTPUT:
<ONLY the completed JSON object>
"""