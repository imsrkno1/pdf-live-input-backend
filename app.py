from flask import Flask, request, render_template, send_file
import fitz  # PyMuPDF
import io
import requests

app = Flask(__name__)

# GitHub PDF Template URL (Updated)
GITHUB_PDF_URL = "https://raw.githubusercontent.com/imsrkno1/pdf-live-input-backend/main/Updated_Template.pdf"

def fill_pdf(data):
    response = requests.get(GITHUB_PDF_URL)
    if response.status_code != 200:
        return None

    pdf_bytes = response.content
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    MM_TO_PT = 2.83465  # Conversion factor from mm to points

    for page in doc:
        for field, info in data.items():
            x_pt = info['x'] * MM_TO_PT  # Convert mm to points
            y_pt = info['y'] * MM_TO_PT  # Convert mm to points
            text = info['value']

            # Insert text at the corrected coordinates
            page.insert_text((x_pt, y_pt), text, fontsize=10, color=(0, 0, 0))

    output_stream = io.BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)
    return output_stream

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = {
        "client_name": {"x": 12.52, "y": 197.18, "value": request.form.get("client_name", "")},
        "client_owner": {"x": 158.04, "y": 147.61, "value": request.form.get("client_owner", "")},
        "client_contact": {"x": 158.04, "y": 133.42, "value": request.form.get("client_contact", "")},
        "project_description": {"x": 12.52, "y": 147.79, "value": request.form.get("project_description", "")},
        "highlights": {"x": 158.04, "y": 73.38, "value": request.form.get("highlights", "")},
        "location": {"x": 12.82, "y": 179.76, "value": request.form.get("location", "")},
        "project_cost": {"x": 158.04, "y": 101.33, "value": request.form.get("project_cost", "")},
        "project_dates": {"x": 158.04, "y": 87.36, "value": request.form.get("project_dates", "")},
        "project_title": {"x": 12.82, "y": 188.47, "value": request.form.get("project_title", "")}
    }
    
    filled_pdf = fill_pdf(data)
    if not filled_pdf:
        return "Error loading PDF template.", 500
    
    return send_file(filled_pdf, as_attachment=True, download_name="filled_form.pdf", mimetype="application/pdf")

if __name__ == '__main__':
    app.run(debug=True)
