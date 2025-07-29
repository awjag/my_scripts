#!/usr/bin/env python3

import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import os
import subprocess

# ---------- CONFIG ----------
logfile = "focus_log.csv"
activity_file = "recent-activity.txt"
texfileTemplate = "productivity_report_template.tex"
texfile = "productivity_report.tex"
tablefile = "web_table.tex"
focus_tablefile = "focus_table.tex"
webpage_focus_tablefile = "webpage_focus_table.tex"
pdf_output = "productivity_report.pdf"
scripts_dir = os.getenv("SCRIPTS_DIR")
focus_script = f"{scripts_dir}/activity-tracker/summarized-focused-window.sh"
webpage_focus_script = f"{scripts_dir}/activity-tracker/summarized-focused-webpages.sh"
domain_focus_script = f"{scripts_dir}/activity-tracker/get-most-visited-domains.sh"
domain_focus_tablefile = "domain_focus_table.tex"
domain_visit_count_script = f"{scripts_dir}/activity-tracker/get-domain-visit-count.sh"
domain_visit_count_tablefile = "domain_visit_count_table.tex"
domain_visit_bar_chart = "domain_visit_count_bar.png"

notes_file = os.path.expanduser("~/notes.txt")
notes_texfile = "notes_block.tex"
# ---------------------------

def escape_latex(s):
    replacements = {
        '\\': r'\textbackslash{}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
    }
    for char, replacement in replacements.items():
        s = s.replace(char, replacement)
    return s

# Step 1: Parse app usage log and generate pie chart
usage = defaultdict(int)

with open(logfile, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 3: continue
        app = row[1].strip()
        duration = int(row[2])
        usage[app] += duration

labels = list(usage.keys())
times = list(usage.values())

plt.figure(figsize=(6, 6))
plt.pie(times, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title("Application Usage (Focus Time)")
plt.axis('equal')
plt.savefig("app_usage_pie.png")
print("[✓] Saved pie chart: app_usage_pie.png")

# Step 2: Run focus script and write application focus table
focus_data = subprocess.check_output(focus_script, shell=True, universal_newlines=True)

with open(focus_tablefile, "w") as out:
    for line in focus_data.strip().split("\n"):
        columns = line.split("\t")
        if len(columns) < 2:
            continue
        app_name = escape_latex(columns[0].strip())
        time_spent = escape_latex(columns[1].strip())
        out.write(f"{app_name} & {time_spent} \\\\\n\\midrule\n")

print(f"[✓] Wrote focus data table rows to {focus_tablefile}")

# Step 3: Run webpage focus script and write webpage focus table
webpage_focus_data = subprocess.check_output(webpage_focus_script, shell=True, universal_newlines=True)

with open(webpage_focus_tablefile, "w") as out:
    for line in webpage_focus_data.strip().split("\n"):
        columns = line.split("\t")
        if len(columns) < 2:
            continue
        url = escape_latex(columns[0].strip())
        time_spent = escape_latex(columns[1].strip())
        out.write(f"\\nolinkurl{{ {url} }} & {time_spent} \\\\\n\\midrule\n")

print(f"[✓] Wrote webpage focus data table rows to {webpage_focus_tablefile}")


# Step: Run domain focus script and write domain focus table
domain_focus_data = subprocess.check_output(domain_focus_script, shell=True, universal_newlines=True)

with open(domain_focus_tablefile, "w") as out:
    for line in domain_focus_data.strip().split("\n"):
        columns = line.split("\t")
        if len(columns) < 2:
            continue
        domain = escape_latex(columns[0].strip())
        time_spent = escape_latex(columns[1].strip())
        out.write(f"{domain} & {time_spent} \\\\\n\\midrule\n")

print(f"[✓] Wrote domain focus data table rows to {domain_focus_tablefile}")

# Step: Run domain visit count script and generate LaTeX table
domain_visit_data = subprocess.check_output(domain_visit_count_script, shell=True, universal_newlines=True)

with open(domain_visit_count_tablefile, "w") as out:
    for line in domain_visit_data.strip().split("\n"):
        parts = line.strip().split(maxsplit=1)
        if len(parts) < 2:
            continue
        count = escape_latex(parts[0])
        domain = escape_latex(parts[1])
        out.write(f"{count} & {domain} \\\\\n\\midrule\n")

print(f"[✓] Wrote domain visit count table rows to {domain_visit_count_tablefile}")


# Step: Generate domain visit frequency bar chart
domain_visit_data = subprocess.check_output(domain_visit_count_script, shell=True, universal_newlines=True)

domain_names = []
domain_counts = []

for line in domain_visit_data.strip().split("\n"):
    parts = line.strip().split(maxsplit=1)
    if len(parts) != 2:
        continue
    count = int(parts[0])
    domain = parts[1]
    domain_counts.append(count)
    domain_names.append(domain)

# Sort by count descending
sorted_pairs = sorted(zip(domain_counts, domain_names), reverse=True)
domain_counts, domain_names = zip(*sorted_pairs)

plt.figure(figsize=(12, 6))
plt.bar(domain_names, domain_counts, color='mediumseagreen')
plt.xticks(rotation=45, ha='right')
plt.xlabel("Domain")
plt.ylabel("Visit Count")
plt.title("Domain Visit Frequency")
plt.tight_layout()
plt.savefig(domain_visit_bar_chart)
print(f"[✓] Saved domain visit bar chart: {domain_visit_bar_chart}")

# Step 4: Read activity log and write LaTeX table rows for web activity
with open(tablefile, "w") as out:
    with open(activity_file, newline='') as infile:
        reader = csv.reader(infile, delimiter='\t')
        for row in reader:
            if len(row) < 3:
                continue
            url = row[0]
            title = escape_latex(row[1])
            time = escape_latex(row[2])
            out.write(f"\\nolinkurl{{ {url} }} & {title} & {time} \\\\\n\\midrule\n")

print(f"[✓] Wrote web activity table rows to {tablefile}")

# Step: Read and format daily notes
if os.path.exists(notes_file):
    with open(notes_file, "r") as nf:
        raw_notes = nf.read()

    def escape_latex_notes(s):
        replacements = {
            '\\': r'\textbackslash{}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
        }
        for char, replacement in replacements.items():
            s = s.replace(char, replacement)
        return s

    escaped_notes = escape_latex_notes(raw_notes)
    with open(notes_texfile, "w") as out:
        out.write("\\begin{quote}\n{\itshape\n")
        out.write(escaped_notes)
        out.write("\n}\n\\end{quote}\n")
    print(f"[✓] Wrote notes to {notes_texfile}")
else:
    print("[!] Notes file not found.")
    with open(notes_file, "w") as nf:
        nf.write("[No notes were recorded during this session.]")

# Step 5: Insert table rows into the LaTeX document
with open(texfileTemplate, "r") as f:
    tex_content = f.read()

# Inject Application Focus Time
focus_table_placeholder = "% rows will be inserted here from focus data"
with open(focus_tablefile, "r") as tf:
    focus_table_rows = tf.read()
tex_content = tex_content.replace(focus_table_placeholder, focus_table_rows)

# Inject Webpage Focus Time
webpage_focus_placeholder = "% rows will be inserted here from webpage focus data"
with open(webpage_focus_tablefile, "r") as tf:
    webpage_focus_rows = tf.read()
tex_content = tex_content.replace(webpage_focus_placeholder, webpage_focus_rows)

# Inject Time Spent Per Domain
domain_focus_placeholder = "% rows will be inserted here from domain focus data"
with open(domain_focus_tablefile, "r") as tf:
    domain_focus_rows = tf.read()
tex_content = tex_content.replace(domain_focus_placeholder, domain_focus_rows)

# Inject domain counts
domain_visit_count_placeholder = "% rows will be inserted here from domain visit count"
with open(domain_visit_count_tablefile, "r") as tf:
    domain_visit_rows = tf.read()
tex_content = tex_content.replace(domain_visit_count_placeholder, domain_visit_rows)

# Inject Recent Web Activity
web_table_placeholder = "% rows will be inserted here from web activity"
with open(tablefile, "r") as tf:
    table_rows = tf.read()
tex_content = tex_content.replace(web_table_placeholder, table_rows)

# Inject notes at the end of the LaTeX document
notes_placeholder = "% insert notes here"
with open(notes_texfile, "r") as nf:
    notes_block = nf.read()
tex_content = tex_content.replace(notes_placeholder, notes_block)

# Save final LaTeX file
with open(texfile, "w") as f:
    f.write(tex_content)

# Step 6: Compile with pdflatex
print("[⌛] Compiling PDF...")
subprocess.run(["pdflatex", "-interaction=nonstopmode", texfile])

if os.path.exists(pdf_output):
    print(f"[✓] Generated PDF: {pdf_output}")
else:
    print("[✗] Failed to compile PDF.")
