def validate_project_profile(data: dict):
    required = ["name", "budget_inr_per_month", "description", "tech_stack", "non_functional_requirements"]
    for key in required:
        if key not in data:
            raise ValueError(f"Missing field: {key}")
    
    if not isinstance(data["tech_stack"], dict) or len(data["tech_stack"]) == 0:
        raise ValueError("tech_stack must contain at least one technology")

    if not isinstance(data["name"], str) or not data["name"].strip():
        raise ValueError("name must be a non-empty string")

    if not isinstance(data["budget_inr_per_month"], (int, float)) or data["budget_inr_per_month"] <= 0:
        raise ValueError("budget_inr_per_month must be a positive number")



def validate_billing(records: list):
    if not (12 <= len(records) <= 20):
        raise ValueError("Billing records must be 12–20")

    for r in records:
        for key in ["month", "service", "region", "cost_inr"]:
            if key not in r:
                raise ValueError(f"Missing billing field: {key}")



def validate_report(report: dict):
    for key in ["project_name", "analysis", "recommendations", "summary"]:
        if key not in report:
            raise ValueError(f"Missing report field: {key}")
        
    if not isinstance(report["recommendations"], list):
        raise ValueError("recommendations must be a list")
    
    if not (6 <= len(report["recommendations"]) <= 10):
        raise ValueError("recommendations must be between 6 and 10 items")
