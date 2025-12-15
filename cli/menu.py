import os
import json
from pathlib import Path
from core.profile import generate_project_profile
from core.billing import generate_billing
from core.recommendations import generate_report

def run_cost_analysis(project_dir: Path):
    profile_path = project_dir / "project_profile.json"

    if not profile_path.exists():
        print("project_profile.json not found.")
        return

    with open(profile_path, "r") as f:
        profile = json.load(f)

    if not profile:
        print("Invalid project profile.")
        return
    
    billing = generate_billing(profile)

    billing_path = project_dir / "billing.json"
    with open(billing_path, "w", encoding="utf-8") as f:
        json.dump(billing, f, indent=2)

    print(f"{len(billing)} billing reports generated for the current month.")

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
        run_cost_analysis(Path(f"projects/{name}"))
        # with open(f"projects/{name}/project_profile.json", "r", encoding="utf-8") as f:
        #     profile = json.load(f)

        # billing = generate_billing(profile)
        # with open(f"projects/{name}/mock_billing.json", "w", encoding="utf-8") as f:
        #     json.dump(billing, f, indent=2)

        # report = generate_report(profile, billing)
        # with open(f"projects/{name}/cost_optimization_report.json", "w", encoding="utf-8") as f:
        #     json.dump(report, f, indent=2)

    else:
        exit()
