import re

def generate_html(report_text: str, output_path: str):
    # Convert Markdown bold (**text**) to HTML <strong>text</strong>
    report_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", report_text, flags=re.DOTALL)
    lines = report_text.split("\n")

    html_lines = []
    html_lines.append("<html>")
    html_lines.append("<head>")
    html_lines.append("<meta charset='UTF-8'>")
    html_lines.append("<title>Cloud Cost Optimization Report</title>")
    html_lines.append("""
    <style>
        body {
            font-family: Arial, Helvetica, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #222;
        }
        h1 {
            text-align: center;
            margin-bottom: 50px;
        }
        h2 {
            margin-top: 50px;
            border-bottom: 2px solid #444;
            padding-bottom: 6px;
        }
        ul {
            margin-left: 20px;
        }
        li {
            margin-bottom: 8px;
        }
        .section {
            margin-bottom: 40px;
        }
    </style>
    """)
    html_lines.append("</head>")
    html_lines.append("<body>")

    # Title
    title = lines[0].strip()
    html_lines.append(f"<h1>{title}</h1>")

    for raw_line in lines[1:]:
        line = raw_line.strip()

        if not line:
            html_lines.append("<br>")
            continue

        # Section headings
        if line.upper().startswith("SECTION"):
            html_lines.append(f"<h2>{line}</h2>")
            continue

        # Bullet points
        if line.startswith("- "):
            html_lines.append("<ul>")
            html_lines.append(f"<li>{line[2:]}</li>")
            html_lines.append("</ul>")
            continue

        # Normal paragraph
        html_lines.append(f"<p>{line}</p>")

    html_lines.append("</body>")
    html_lines.append("</html>")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))
