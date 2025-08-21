from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_resume(output_path, resume_json):
    """
    Generates a well-formatted resume PDF from structured JSON.
    Compatible with experience/education as arrays of objects.
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    header_style = ParagraphStyle('HeaderStyle', parent=styles['Heading2'], fontSize=14, leading=16,
                                  spaceBefore=12, spaceAfter=6, textColor=colors.HexColor('#222222'))
    subheader_style = ParagraphStyle('SubHeader', parent=styles['Heading3'], fontSize=12, leading=14,
                                     spaceBefore=6, spaceAfter=2, textColor=colors.HexColor('#333333'))
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontSize=11, leading=14,
                                  textColor=colors.HexColor('#000000'))
    bullet_style = ParagraphStyle('BulletStyle', parent=styles['Normal'], fontSize=11, leading=14,
                                  leftIndent=14, spaceAfter=2)
    name_style = ParagraphStyle('NameStyle', parent=styles['Heading1'], fontSize=18, leading=22,
                                spaceAfter=4, textColor=colors.HexColor('#111111'))

    # Name & Contact
    if resume_json.get("name"):
        story.append(Paragraph(resume_json["name"], name_style))
    if resume_json.get("contact_info"):
        story.append(Paragraph(resume_json["contact_info"], normal_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 8))

    # Summary
    if resume_json.get("summary"):
        story.append(Paragraph("Summary", header_style))
        story.append(Paragraph(resume_json["summary"], normal_style))
        story.append(Spacer(1, 10))

    # Skills
    if resume_json.get("skills"):
        story.append(Paragraph("Skills", header_style))
        skills = resume_json["skills"]
        table_data, row = [], []
        for i, skill in enumerate(skills, 1):
            row.append(skill)
            if i % 4 == 0:
                table_data.append(row)
                row = []
        if row:
            table_data.append(row)
        table = Table(table_data, hAlign='LEFT')
        table.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                   ('FONTSIZE', (0, 0), (-1, -1), 11),
                                   ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
        story.append(table)
        story.append(Spacer(1, 10))

    # Experience
    if resume_json.get("experience"):
        story.append(Paragraph("Experience", header_style))
        for exp in resume_json["experience"]:
            title_line = f"{exp.get('title','')} – {exp.get('company','')} | {exp.get('location','')} ({exp.get('duration','')})"
            story.append(Paragraph(f"<b>{title_line}</b>", subheader_style))
            for resp in exp.get("responsibilities", []):
                story.append(Paragraph(f"• {resp}", bullet_style))
            story.append(Spacer(1, 6))

    # Education
    if resume_json.get("education"):
        story.append(Paragraph("Education", header_style))
        for edu in resume_json["education"]:
            edu_line = f"{edu.get('degree','')} – {edu.get('institution','')} ({edu.get('graduation_year','')})"
            story.append(Paragraph(edu_line, normal_style))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 10))

    # Selected Projects
    if resume_json.get("selected_projects"):
        story.append(Paragraph("Selected Projects", header_style))
        for proj in resume_json["selected_projects"]:
            story.append(Paragraph(proj, normal_style))
            story.append(Spacer(1, 6))

    try:
        doc.build(story)
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False
