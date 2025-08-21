from flask import Flask, request, render_template, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import json
from utils.parser import extract_text_from_pdf, extract_text_from_txt
from utils.enhancer import get_ats_score, get_suggestions, generate_enhanced_resume
from utils.pdf_generator import generate_pdf_resume
from utils.enhanced_resume import parse_resume_to_html  # Parses JSON to HTML preview

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        # Validate uploaded file
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file uploaded'}), 400
        resume_file = request.files['resume']
        if resume_file.filename == '':
            return jsonify({'error': 'No resume file selected'}), 400
        if not allowed_file(resume_file.filename):
            return jsonify({'error': 'Resume must be PDF or TXT file'}), 400

        resume_filename = secure_filename(resume_file.filename)
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        resume_file.save(resume_path)

        # Job description
        job_description_text = request.form.get('job_description', '').strip()
        if not job_description_text:
            return jsonify({'error': 'Job description is required'}), 400

        # Extract resume text
        resume_text = extract_text_from_pdf(resume_path) if resume_filename.endswith('.pdf') else extract_text_from_txt(resume_path)

        # ATS scoring (already returns dict, no need for json.loads)
        ats_result = get_ats_score(resume_text, job_description_text)
        if ats_result is None:
            ats_result = {
                "overall_match": "N/A",
                "skills_match": "N/A",
                "experience_match": "N/A",
                "education_match": "N/A",
                "explanations": "Failed to generate ATS score"
            }
        print(ats_result)
        # Suggestions
        suggestions_json = get_suggestions(resume_text, job_description_text, ats_result) or {}
        print(suggestions_json)

        # Enhanced resume (expects ats_result dict, not string)
        enhanced_resume_json = generate_enhanced_resume(resume_text, job_description_text, ats_result, suggestions_json)
        print(enhanced_resume_json)

        if not isinstance(enhanced_resume_json, dict):
            return jsonify({'error': 'Failed to generate enhanced resume'}), 500

        # Convert to HTML for preview
        enhanced_resume_html = parse_resume_to_html(enhanced_resume_json)

        # Generate PDF
        enhanced_resume_path = os.path.join(app.config['OUTPUT_FOLDER'], 'enhanced_resume.pdf')
        pdf_generated = generate_pdf_resume(enhanced_resume_path, enhanced_resume_json)

        # Clean up uploaded file
        os.remove(resume_path)

        return render_template(
            'results.html',
            ats_result=ats_result,
            suggestions=suggestions_json,
            enhanced_resume=enhanced_resume_html,
            pdf_generated=pdf_generated
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download')
def download_resume():
    try:
        enhanced_resume_path = os.path.join(app.config['OUTPUT_FOLDER'], 'enhanced_resume.pdf')
        if os.path.exists(enhanced_resume_path):
            return send_file(enhanced_resume_path, as_attachment=True, download_name='enhanced_resume.pdf')
        else:
            return jsonify({'error': 'Enhanced resume not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
