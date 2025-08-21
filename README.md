# Resume Enhancer Web App

A Flask-based web application that helps users improve their resumes to match job descriptions using AI-powered analysis and suggestions.

## Features

- **Resume Upload**: Upload PDF resumes for analysis
- **Job Description Input**: Paste or upload job descriptions (PDF/TXT)
- **ATS Score Analysis**: Get compatibility scores between resume and job requirements
- **AI-Powered Suggestions**: Receive detailed improvement recommendations
- **Enhanced Resume Generation**: Download improved resume as PDF
- **Visual Analytics**: Charts showing skills match and gaps
- **Modern UI**: Responsive design with smooth animations

## Project Structure

```
resume-enhancer/
├── app.py                    # Main Flask application
├── app_demo.py              # Demo version with mock data
├── src/                     # Source files for deployment
│   ├── main.py             # Entry point for deployment
│   ├── app.py              # Flask app copy
│   ├── utils/              # Utility modules
│   │   ├── parser.py       # PDF/TXT text extraction
│   │   ├── ats_api.py      # SharpAPI integration
│   │   ├── enhancer.py     # Google Gemini integration
│   │   └── pdf_generator.py # PDF creation
│   ├── templates/          # HTML templates
│   │   └── index.html      # Main web interface
│   └── static/             # Static assets (CSS/JS)
├── templates/
│   └── index.html          # Main web interface
├── static/                 # Static assets
├── utils/                  # Utility modules
│   ├── parser.py           # PDF/TXT text extraction
│   ├── ats_api.py          # SharpAPI integration
│   ├── enhancer.py         # Google Gemini integration
│   └── pdf_generator.py    # PDF creation
├── uploads/                # Temporary file uploads
├── output/                 # Generated resume outputs
├── venv/                   # Python virtual environment
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys)
├── sample_resume.txt       # Sample resume for testing
├── sample_job_description.txt # Sample job description
└── README.md              # This file
```

## Installation & Setup

### Prerequisites
- Python 3.11+
- pip package manager

### 1. Clone/Extract the Project
```bash
cd resume-enhancer
```

### 2. Create Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Edit the `.env` file and add your API keys:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
SHARPAPI_KEY=your_apyhub_sharpapi_key_here
```

**Getting API Keys:**
- **Google Gemini API**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- **SharpAPI**: Visit [APYHub](https://apyhub.com/utility/sharpapi-resume-job-match-score)

### 5. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. **Upload Resume**: Click "Choose PDF File" and select your resume
2. **Add Job Description**: Either paste the job description in the text area or upload a PDF/TXT file
3. **Analyze**: Click "Enhance Resume" to process your documents
4. **Review Results**: View the ATS score, skills analysis charts, and AI suggestions
5. **Download**: Click "Download Enhanced Resume" to get the improved PDF

## Demo Mode

The application includes a demo mode with mock data that works without API keys. This is useful for testing the interface and functionality.

To run in demo mode, use:
```bash
python app_demo.py
```

## API Integrations

### SharpAPI (ATS Scoring)
- **Purpose**: Analyzes resume-job match compatibility
- **Returns**: Score, matching skills, missing skills
- **Documentation**: [SharpAPI Resume-Job Match](https://apyhub.com/utility/sharpapi-resume-job-match-score)

### Google Gemini (AI Enhancement)
- **Purpose**: Provides intelligent resume improvement suggestions
- **Returns**: Enhanced resume content and recommendations
- **Documentation**: [Google AI Studio](https://ai.google.dev/)

## Technical Details

### Backend (Flask)
- **Framework**: Flask with CORS support
- **File Handling**: Secure file uploads with validation
- **PDF Processing**: PyMuPDF for text extraction
- **PDF Generation**: ReportLab for creating enhanced resumes

### Frontend
- **UI Framework**: Bootstrap 5
- **Charts**: Chart.js for data visualization
- **Design**: Modern gradient design with animations
- **Responsive**: Mobile-friendly interface

### Dependencies
- Flask & Flask-CORS
- PyMuPDF (PDF processing)
- ReportLab (PDF generation)
- Google Generative AI
- Requests (API calls)
- Python-dotenv (environment variables)
- Matplotlib (additional charting)

## Troubleshooting

### Common Issues

1. **PyMuPDF Import Error**
   - The app includes fallback handling for PDF processing
   - If issues persist, try: `pip install --upgrade PyMuPDF`

2. **API Key Errors**
   - Ensure your `.env` file has valid API keys
   - Check API key permissions and quotas

3. **File Upload Issues**
   - Ensure `uploads/` and `output/` directories exist
   - Check file size limits (16MB max)

4. **Port Already in Use**
   - Change the port in `app.py`: `app.run(host='0.0.0.0', port=5001)`

## Customization

### Adding New Features
- **New APIs**: Add integration files in `utils/`
- **UI Changes**: Modify `templates/index.html`
- **Styling**: Update CSS in the HTML template
- **Charts**: Extend Chart.js configurations

### Configuration
- **File Size Limits**: Modify `MAX_CONTENT_LENGTH` in `app.py`
- **Allowed File Types**: Update `ALLOWED_EXTENSIONS`
- **Output Formats**: Extend PDF generation in `utils/pdf_generator.py`

## Security Notes

- API keys are stored in `.env` file (not committed to version control)
- File uploads are validated and sanitized
- Temporary files are cleaned up after processing
- CORS is enabled for development (configure for production)

## Production Deployment

For production deployment:
1. Set `debug=False` in `app.py`
2. Use a production WSGI server (e.g., Gunicorn)
3. Configure proper CORS origins
4. Set up HTTPS
5. Use environment variables for sensitive configuration

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify API key configuration
3. Test with demo mode first
4. Check console logs for detailed error messages

