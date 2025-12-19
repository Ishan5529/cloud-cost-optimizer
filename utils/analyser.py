def generate_analysis(project_profile: dict, billing_data: list) -> dict:
    budget = project_profile.get("budget_inr_per_month", 0)
    
    # 1. Calculate Total Cost
    total_cost = sum(item['cost_inr'] for item in billing_data)
    
    # 2. Calculate Variance
    variance = total_cost - budget
    
    # 3. Aggregate Costs by Service
    service_map = {}
    for item in billing_data:
        key = f"{item.get('provider', 'Unknown')} - {item.get('service', 'Unknown')}"
        service_map[key] = service_map.get(key, 0) + item['cost_inr']
    
    analysis_json = {
        "total_monthly_cost": total_cost,
        "budget": budget,
        "budget_variance": variance,
        "service_costs": service_map
    }
    
    return analysis_json

def generate_summary(llm_response: dict) -> dict:
    data = llm_response if isinstance(llm_response, dict) else {}

    # 1. Calculate total savings
    real_savings = sum(r['potential_savings'] for r in data['recommendations'])
    data['summary']['total_potential_savings'] = real_savings

    # 2. Calculate savings percentage
    data['summary']['savings_percentage'] = round((real_savings / data['analysis']['total_monthly_cost']) * 100, 2)

    return data