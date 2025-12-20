import os
import json
from pathlib import Path
from core.cost_optimization import generate_cost_optimization_report
from core.profile import generate_project_profile
from core.billing import generate_billing
from utils.analyser import generate_analysis, generate_summary
from core.export_report import generate_report_content
from utils.pdf_generator import generate_pdf

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


def view_recommendations() -> str:
    name = input("Project folder name: ")
    project_dir = Path(f"projects/{name}")
    report_path = project_dir / "cost_optimization_report.json"

    if not report_path.exists():
        return "cost_optimization_report.json not found. Run cost analysis first."

    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)


    recommendations = report.get("recommendations", [])

    idx = 0
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        if idx >= len(recommendations):
            break
        rec = recommendations[idx]
        print("\n=== COST OPTIMIZATION RECOMMENDATIONS ===\n")
        print(f"{idx + 1}. {rec['title']}")
        print(f"   Service            : {rec['service']}")
        print(f"   Current Cost       : ₹{rec['current_cost']}")
        print(f"   Potential Savings  : ₹{rec['potential_savings']}")
        print(f"   Type               : {rec['recommendation_type']}")
        print(f"   Effort             : {rec['implementation_effort']}")
        print(f"   Risk               : {rec['risk_level']}")
        print(f"   Providers          : {', '.join(rec['cloud_providers'])}")
        print("   Steps:")
        for step in rec["steps"]:
            print(f"     - {step}")
        
        while True:
            choice = input("\nEnter 1 for next, 0 for previous, 2 for exit: ")
            if choice == "1":
                idx += 1
                break
            elif choice == "0" and idx > 0:
                idx -= 1
                break
            elif choice == "0" and idx == 0:
                print("Already at the first recommendation.")
            elif choice == "2":
                return ""
            else:
                print("Invalid input.")

    summary = report.get("summary", {})
    print("=== SUMMARY ===")
    print(f"Total Potential Savings : ₹{summary.get('total_potential_savings')}")
    print(f"Savings Percentage      : {summary.get('savings_percentage')}%")
    print(f"Recommendations Count   : {summary.get('recommendations_count')}")
    print(f"Other Insights:")
    for key, value in summary.get("other_important_insights", {}).items():
        print(f"    - {key} : ₹{value}")

    input("\nPress Enter to return to menu...")
    return ""


def export_report() -> str:
    name = input("Project folder name: ")
    project_dir = Path(f"projects/{name}")

    desc_path = project_dir / "project_description.txt"
    profile_path = project_dir / "project_profile.json"
    billing_path = project_dir / "mock_billing.json"
    report_path = project_dir / "cost_optimization_report.json"

    if not all(p.exists() for p in [desc_path, profile_path, billing_path, report_path]):
        return "Required files missing. Run cost analysis first."

    with open(desc_path) as f:
        description = f.read()

    with open(profile_path) as f:
        profile = json.load(f)

    with open(billing_path) as f:
        billing = json.load(f)

    with open(report_path) as f:
        optimization_report = json.load(f)

    report_content = generate_report_content(
        description,
        profile,
        billing,
        optimization_report
    )

    output_pdf = project_dir / "cloud_cost_optimization_report.pdf"
    generate_pdf(report_content, str(output_pdf))

    open_now = input("PDF generated successfully. Open now? (y/n): ").lower()
    if open_now == "y":
        os.startfile(output_pdf)

    return "PDF export completed."


def run_cli():
    prev = ""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(prev)
        print("Cloud Cost Optimizer CLI")
        print("\n1. Enter new project description")
        print("2. Run complete cost analysis")
        print("3. View recommendations")
        print("4. Export report as PDF")
        print("5. Exit\n\n")

        choice = input("Choose: ")

        if choice == "1":
            prev = create_project_profile() + "\n\n"

        elif choice == "2":
            prev = run_cost_analysis() + "\n\n"

        elif choice == "3":
            prev = view_recommendations() + "\n\n"

        elif choice == "4":
            prev = export_report() + "\n\n"

        else:
            exit()
