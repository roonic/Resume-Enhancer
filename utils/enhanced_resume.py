import html  # for safe escaping

def parse_resume_to_html(enhanced_resume_json):
    """
    Converts structured enhanced resume JSON into HTML for preview.
    Expects experience and education as arrays of objects.
    """
    html_parts = []

    # Header
    html_parts.append(f"<h1 style='font-size:24px;margin-bottom:4px;'>{html.escape(enhanced_resume_json.get('name',''))}</h1>")
    html_parts.append(f"<p style='color:gray;font-size:12px;margin-bottom:8px;'>{html.escape(enhanced_resume_json.get('contact_info',''))}</p>")
    html_parts.append("<hr style='border:1px solid #ccc;margin:8px 0;'>")

    # Summary
    summary = enhanced_resume_json.get('summary', '')
    if summary:
        html_parts.append("<h3 style='margin-bottom:4px;'>Summary</h3>")
        html_parts.append(f"<p style='font-size:12px;margin-bottom:8px;'>{html.escape(summary)}</p>")

    # Skills
    skills = enhanced_resume_json.get('skills', [])
    if skills:
        html_parts.append("<h3 style='margin-bottom:4px;'>Skills</h3>")
        html_parts.append("<ul style='font-size:12px;margin-bottom:8px;padding-left:20px;'>")
        for skill in skills:
            html_parts.append(f"<li>{html.escape(skill)}</li>")
        html_parts.append("</ul>")

    # Experience
    experience_list = enhanced_resume_json.get('experience', [])
    if experience_list:
        html_parts.append("<h3 style='margin-bottom:4px;'>Experience</h3>")
        for exp in experience_list:
            title_line = f"{exp.get('title','')} – {exp.get('company','')} | {exp.get('location','')} ({exp.get('duration','')})"
            html_parts.append(f"<p style='font-size:12px;margin:2px 0;'><b>{html.escape(title_line)}</b></p>")
            responsibilities = exp.get('responsibilities', [])
            if responsibilities:
                html_parts.append("<ul style='font-size:12px;margin-bottom:8px;padding-left:20px;'>")
                for r in responsibilities:
                    html_parts.append(f"<li>{html.escape(r)}</li>")
                html_parts.append("</ul>")

    # Selected Projects
    projects = enhanced_resume_json.get('selected_projects', [])
    if projects:
        html_parts.append("<h3 style='margin-bottom:4px;'>Selected Projects</h3>")
        html_parts.append("<ul style='font-size:12px;margin-bottom:8px;padding-left:20px;'>")
        for proj in projects:
            html_parts.append(f"<li>{html.escape(str(proj))}</li>")
        html_parts.append("</ul>")

    # Education
    education_list = enhanced_resume_json.get('education', [])
    if education_list:
        html_parts.append("<h3 style='margin-bottom:4px;'>Education</h3>")
        for edu in education_list:
            edu_line = f"{edu.get('degree','')} – {edu.get('institution','')} ({edu.get('graduation_year','')})"
            html_parts.append(f"<p style='font-size:12px;margin:2px 0;'>{html.escape(edu_line)}</p>")

    return "\n".join(html_parts)
