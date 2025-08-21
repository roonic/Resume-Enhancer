from flask import Flask, request, render_template, jsonify, send_file
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from utils.parser import extract_text_from_pdf, extract_text_from_txt
from utils.pdf_generator import generate_pdf_resume

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_mock_ats_score(resume_text, job_description_text):
    """Mock ATS scoring function for demo purposes"""
    # Simple keyword matching for demo
    job_keywords = ['python', 'javascript', 'react', 'node.js', 'aws', 'sql', 'docker', 'kubernetes', 'typescript', 'mongodb']
    resume_lower = resume_text.lower()
    
    matching_skills = []
    missing_skills = []
    
    for keyword in job_keywords:
        if keyword in resume_lower:
            matching_skills.append(keyword.title())
        else:
            missing_skills.append(keyword.title())
    
    # Calculate score based on matches
    score = min(95, (len(matching_skills) / len(job_keywords)) * 100)
    
    return {
        'score': int(score),
        'matching_skills': matching_skills,
        'missing_skills': missing_skills,
        'feedback': 'Resume shows good technical alignment with job requirements.'
    }

def get_mock_gemini_suggestions(resume_text, job_description_text):
    """Mock AI suggestions for demo purposes"""
    return """ENHANCED RESUME SUGGESTIONS

SUMMARY
Experienced Full Stack Developer with 5+ years of expertise in modern web technologies including Python, JavaScript, and cloud platforms. Proven track record in developing scalable applications and implementing best practices for code quality and security.

TECHNICAL SKILLS
• Programming Languages: Python, JavaScript, TypeScript, SQL
• Frontend Technologies: React, HTML5, CSS3, Responsive Design
• Backend Technologies: Node.js, Express.js, Flask, REST APIs
• Cloud Platforms: AWS (EC2, S3, Lambda), Cloud Architecture
• Databases: PostgreSQL, MongoDB, MySQL
• DevOps & Tools: Docker, Git, CI/CD Pipelines, Agile/Scrum
• Additional: Microservices Architecture, Testing Frameworks

PROFESSIONAL EXPERIENCE

Senior Software Engineer | Tech Company | 2020-2025
• Developed and maintained full-stack web applications using React and Node.js, serving 10,000+ users
• Implemented scalable REST APIs using Python and Flask with 99.9% uptime
• Architected cloud solutions on AWS, reducing infrastructure costs by 30%
• Collaborated with cross-functional teams using Agile methodologies to deliver projects on time
• Mentored junior developers and conducted code reviews to maintain high code quality standards

Full Stack Developer | Startup Inc | 2018-2020
• Built responsive web interfaces using modern JavaScript frameworks and CSS3
• Maintained and optimized legacy systems, improving performance by 40%
• Implemented automated testing processes, reducing bugs in production by 60%
• Participated in architectural decisions for microservices migration

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2018

RECOMMENDATIONS FOR IMPROVEMENT:
1. Add specific metrics and achievements to quantify your impact
2. Include experience with containerization (Docker, Kubernetes) if available
3. Mention any experience with GraphQL and modern testing frameworks
4. Highlight leadership and mentoring experience
5. Add any relevant certifications (AWS, Azure, etc.)
6. Include experience with CI/CD pipelines and DevOps practices"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        # Check if files are present
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file uploaded'}), 400
        
        resume_file = request.files['resume']
        job_description_text = request.form.get('job_description', '')
        job_description_file = request.files.get('job_description_file')
        
        if resume_file.filename == '':
            return jsonify({'error': 'No resume file selected'}), 400
        
        if not allowed_file(resume_file.filename):
            return jsonify({'error': 'Resume must be a PDF file'}), 400
        
        # Save resume file
        resume_filename = secure_filename(resume_file.filename)
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        resume_file.save(resume_path)
        
        # Extract resume text
        resume_text = extract_text_from_pdf(resume_path)
        
        # Handle job description
        if job_description_file and job_description_file.filename != '':
            if allowed_file(job_description_file.filename):
                job_desc_filename = secure_filename(job_description_file.filename)
                job_desc_path = os.path.join(app.config['UPLOAD_FOLDER'], job_desc_filename)
                job_description_file.save(job_desc_path)
                
                if job_desc_filename.endswith('.pdf'):
                    job_description_text = extract_text_from_pdf(job_desc_path)
                else:
                    job_description_text = extract_text_from_txt(job_desc_path)
        
        if not job_description_text.strip():
            return jsonify({'error': 'Job description is required'}), 400
        
        # Get mock ATS score and suggestions
        ats_result = get_mock_ats_score(resume_text, job_description_text)
        gemini_suggestions = get_mock_gemini_suggestions(resume_text, job_description_text)
        
        # Generate enhanced resume PDF
        enhanced_resume_path = os.path.join(app.config['OUTPUT_FOLDER'], 'enhanced_resume.pdf')
        pdf_generated = generate_pdf_resume(enhanced_resume_path, gemini_suggestions)
        
        # Clean up uploaded files
        os.remove(resume_path)
        if 'job_desc_path' in locals():
            os.remove(job_desc_path)
        
        return jsonify({
            'success': True,
            'ats_result': ats_result,
            'gemini_suggestions': gemini_suggestions,
            'pdf_generated': pdf_generated
        })
        
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

