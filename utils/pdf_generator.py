from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from textwrap import wrap

SECTION_TITLES = {
    "Project Overview",
    "Project Architecture & Requirements",
    "Billing Overview",
    "Cost Analysis",
    "Optimization Recommendations",
    "Estimated Savings & Impact",
    "Final Summary & Next Steps"
}

def generate_pdf(report_text: str, output_path: str):
    report_text = report_text.replace("**", "")
    report_text = report_text.replace("#", "")
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    x_margin = 1 * inch
    y = height - 1 * inch
    line_height = 14
    max_width_chars = 95

    def new_page():
        nonlocal y
        c.showPage()
        c.setFont("Helvetica", 11)
        y = height - 1 * inch

    # Title page
    lines = report_text.split("\n")
    title = lines[0]

    c.setFont("Helvetica-Bold", 36)

    # Wrap title into multiple lines
    wrapped_title = wrap(title, 30)  # 30 chars works well for size 36 font

    # Calculate vertical centering
    total_title_height = len(wrapped_title) * 48  # approx line height for 40pt font
    start_y = (height + total_title_height) / 2

    # Draw each line centered horizontally
    y_pos = start_y
    for line in wrapped_title:
        c.drawCentredString(width / 2, y_pos, line)
        y_pos -= 48

    # c.showPage()
    # c.drawCentredString(width / 2, y, title)
    # c.showPage()

    c.setFont("Helvetica", 11)
    y = height - 1 * inch

    for raw_line in lines[1:]:
        line = raw_line.strip()

        # Force page break before each section
        if line in SECTION_TITLES or line.upper().startswith("SECTION"):
            new_page()
            c.setFont("Helvetica-Bold", 15)
            c.drawString(x_margin, y, line)
            y -= 24
            c.setFont("Helvetica", 11)
            continue

        # Empty line
        if not line:
            y -= line_height
            continue

        wrapped_lines = wrap(line, max_width_chars)
        for wline in wrapped_lines:
            if y < inch:
                new_page()
            c.drawString(x_margin, y, wline)
            y -= line_height

    c.save()