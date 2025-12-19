import os
import json
from pathlib import Path
from core.cost_optimization import generate_cost_optimization_report
from core.profile import generate_project_profile
from core.billing import generate_billing
from utils.analyser import generate_analysis, generate_summary

def run_cost_analysis() -> str:
    # Importing project profile
    name = input("Project folder name: ")
    project_dir = Path(f"projects/{name}")
    profile_path = project_dir / "project_profile.json"
    if not profile_path.exists():
        return "project_profile.json not found."

    with open(profile_path, "r") as f:
        profile = json.load(f)

    if not profile:
        return "Invalid project profile."
    
    # Generating mock billing data
    billing = generate_billing(profile)
    billing_path = project_dir / "mock_billing.json"
    with open(billing_path, "w", encoding="utf-8") as f:
        json.dump(billing, f, indent=2)

    print("\nMock billing data generated successfully.\n")

    analysis_data = generate_analysis(profile, billing)
    print("Analysis data generated successfully.")

    # Generating cost optimization report
    report = generate_summary(generate_cost_optimization_report(
        profile,
        billing,
        analysis_data
    ))

    output_path = project_dir / "cost_optimization_report.json"
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    return "Cost analysis completed successfully."


def create_project_profile():
    name = input("Project folder name: ")
    os.makedirs(f"projects/{name}", exist_ok=True)
    desc = input("Enter project description: ")
    with open(f"projects/{name}/project_description.txt", "w", encoding="utf-8") as f:
        f.write(desc)

    profile = generate_project_profile(desc)

    if not profile:
        return "Invalid / Incomplete project description."
    
    with open(f"projects/{name}/project_profile.json", "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
    
    return "Project profile generated successfully."


def run_cli():
    prev = ""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(prev)
        print("Cloud Cost Optimizer CLI")
        print("\n1. Enter new project description")
        print("2. Run complete cost analysis")
        print("3. Exit\n\n")

        choice = input("Choose: ")

        if choice == "1":
            prev = create_project_profile() + "\n\n"

        elif choice == "2":
            prev = run_cost_analysis() + "\n\n"

        else:
            exit()
