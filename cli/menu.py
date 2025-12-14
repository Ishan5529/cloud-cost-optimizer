import os
import json
from core.profile import generate_project_profile
from core.billing import generate_billing
from core.recommendations import generate_report

def run_cli():
    print("\n1. Enter new project description")
    print("2. Run complete cost analysis")
    print("3. Exit\n\n")

    choice = input("Choose: ")

    if choice == "1":
        name = input("Project folder name: ")
        os.makedirs(f"projects/{name}", exist_ok=True)
        desc = input("Enter project description: ")
        with open(f"projects/{name}/project_description.txt", "w", encoding="utf-8") as f:
            f.write(desc)

        profile = generate_project_profile(desc)
        with open(f"projects/{name}/project_profile.json", "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2)

    elif choice == "2":
        name = input("Project folder name: ")
        with open(f"projects/{name}/project_profile.json", "r", encoding="utf-8") as f:
            profile = json.load(f)

        billing = generate_billing(profile)
        with open(f"projects/{name}/mock_billing.json", "w", encoding="utf-8") as f:
            json.dump(billing, f, indent=2)

        report = generate_report(profile, billing)
        with open(f"projects/{name}/cost_optimization_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    else:
        exit()
