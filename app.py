from flask import Flask, request, render_template, send_file
import fitz  # PyMuPDF
import io
import requests

app = Flask(__name__)

# GitHub PDF Template URL (Updated)
GITHUB_PDF_URL = "https://raw.githubusercontent.com/imsrkno1/pdf-live-input-backend/main/Updated_Template.pdf"

def mm_to_pt(mm):
    """Convert millimeters to points"""
    return mm * 2.83465  # 1 mm = 2.83465 points

def fill_pdf(data):
    """Fills PDF template with user data"""
    response = requests.get(GITHUB_PDF_URL)
    if response.status_code != 200:
        return None
    
    pdf_bytes = response.content
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    for page in doc:
        for field in data:
            x_pt = mm_to_pt(data[field]['x'])  # Convert mm to pt
            y_pt = mm_to_pt(data[field]['y'])  # Convert mm to pt
            page.insert_text((x_pt, y_pt), data[field]['value'], fontsize=12)
    
    output_stream = io.BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)
    return output_stream

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.json  # Read JSON data from frontend
    
    formatted_data = {
        "client_name": {"x": 12.52, "y": 197.18, "value": data.get("client_name", "")},
        "client_owner": {"x": 158.04, "y": 147.61, "value": data.get("client_owner", "")},
        "client_contact": {"x": 158.04, "y": 133.42, "value": data.get("client_contact", "")},
        "project_description": {"x": 12.52, "y": 147.79, "value": data.get("project_description", "")},
        "highlights": {"x": 158.04, "y": 73.38, "value": data.get("highlights", "")},
        "location": {"x": 12.82, "y": 179.76, "value": data.get("location", "")},
        "project_cost": {"x": 158.04, "y": 101.33, "value": data.get("project_cost", "")},
        "project_dates": {"x": 158.04, "y": 87.36, "value": data.get("project_dates", "")},
        "project_title": {"x": 12.82, "y": 188.47, "value": data.get("project_title", "")}
    }
    
    filled_pdf = fill_pdf(formatted_data)
    if not filled_pdf:
        return "Error loading PDF template.", 500
    
    return send_file(filled_pdf, as_attachment=False, mimetype="application/pdf")

    
    filled_pdf = fill_pdf(data)
    if not filled_pdf:
        return "Error loading PDF template.", 500
    
    return send_file(filled_pdf, as_attachment=True, download_name="filled_form.pdf", mimetype="application/pdf")

if __name__ == '__main__':
    app.run(debug=True)
