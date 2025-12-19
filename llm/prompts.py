import json
from datetime import datetime

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




def billing_prompt(project_profile: dict) -> str:
    month = datetime.now().strftime("%Y-%m")
    
    return f"""
You are a cloud cost simulator.
Return a VALID JSON ARRAY (list) of synthetic cloud billing records.

Generate 12-20 realistic synthetic cloud billing records
for the SAME MONTH: {month}
based on the project profile below.

STRICT RULES:
- Output ONLY valid JSON
- Do NOT include explanations, markdown, or arrays
- Use provider-specific naming (AWS, Azure, or GCP)
- Costs must be realistic and internally consistent
- Total cost must be within the project budget
- Billing must reflect project scale and tech stack

REQUIRED JSON SCHEMA (for EACH item in the list):
{{
  "month": "YYYY-MM",
  "provider": "string",
  "service": "string",
  "region": "string",
  "usage_type": "string",
  "unit": "string",
  "usage_quantity": number,
  "cost_inr": number,
  "desc": "string",
}}

PROJECT PROFILE:
{json.dumps(project_profile, indent=2)}

OUTPUT:
<ONLY the JSON array>
"""




def cost_optimization_prompt(project_profile: dict, billing_reports: list, analysis_data: dict) -> str:
    return f"""
You are a cloud cost optimization expert.

Generate a COST OPTIMIZATION REPORT based ONLY on:
1) Project profile
2) Synthetic monthly billing data
3) Analysis data

STRICT RULES:
- Output ONLY valid JSON
- Do NOT include explanations, markdown, or comments
- Follow the EXACT schema provided
- All calculations, comparisons, and reasoning must be done by you
- Recommendations MUST be multi-cloud (AWS, Azure, GCP, open-source/free-tier options)
- Include architectural optimizations
- Avoid high effort vs low reward suggestions
- Avoid free-tier traps, focus on substantial savings and efficiency
- If budget is not exceeded, focus on efficiency improvements
- Generate between 6 and 10 recommendations

REQUIRED JSON SCHEMA:
{{
  "project_name": "string",
  "analysis": {{
    {json.dumps(analysis_data)},
    "high_cost_services": {{
      "service_name": number
    }},
    "is_over_budget": boolean
  }},
  "recommendations": [
    {{
      "title": "string",
      "service": "string",
      "current_cost": number,
      "potential_savings": number (estimated savings in INR),
      "recommendation_type": "open_source | free_tier | alternative_provider | optimization | right_sizing | architectural, etc.",
      "description": "string",
      "implementation_effort": "low | medium | high",
      "risk_level": "low | medium | high",
      "steps": ["string"],
      "cloud_providers": ["string"]
    }}
  ],
  "summary": {{
    "total_potential_savings": number (sum of all potential savings from recommendations),
    "savings_percentage": number (percentage of total_monthly_cost),
    "recommendations_count": number,
    "high_impact_recommendations": number,
    other important insights in key-value pairs
  }}
}}

PROJECT PROFILE:
{json.dumps(project_profile, indent=2)}

BILLING DATA (array of billing scenarios for the same month):
{json.dumps(billing_reports, indent=2)}

OUTPUT:
<ONLY the JSON object>
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