from flask import Flask, request, send_file
from flask_cors import CORS
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

app = Flask(__name__)
CORS(app)

template_path = "Updated_Template.pdf"

def fill_pdf(data):
    reader = PdfReader(template_path)
    writer = PdfWriter()
    
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    
    # Mapping user input to designated areas
    c.drawString(50, 700, data.get("client_name", ""))
    c.drawString(50, 680, data.get("project_title", ""))
    c.drawString(50, 660, data.get("location", ""))
    c.drawString(50, 640, data.get("client_owner", ""))
    c.drawString(50, 620, data.get("project_description", ""))
    c.drawString(50, 600, data.get("project_cost", ""))
    c.drawString(50, 580, data.get("project_dates", ""))
    c.drawString(50, 560, data.get("highlights", ""))
    c.drawString(50, 540, data.get("client_contact", ""))
    
    c.save()
    packet.seek(0)
    overlay_reader = PdfReader(packet)
    
    for page in range(len(reader.pages)):
        original_page = reader.pages[page]
        if page == 0:
            original_page.merge_page(overlay_reader.pages[0])
        writer.add_page(original_page)
    
    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)
    return output_stream

@app.route('/generate', methods=['POST'])
def generate_pdf():
    data = request.json
    filled_pdf = fill_pdf(data)
    return send_file(filled_pdf, as_attachment=True, download_name="Filled_Template.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
